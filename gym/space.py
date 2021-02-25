import abc
import dataclasses
import typing

import numpy


@dataclasses.dataclass
class Space(abc.ABC):
    shape: typing.Union[typing.Tuple[int, ...], int]

    dtype: numpy.dtype

    def __call__(self, buffer: memoryview = None) -> numpy.ndarray:
        return numpy.ndarray(self.shape, self.dtype, buffer)

    @abc.abstractmethod
    def sample(self, buffer: memoryview = None, random: numpy.random.RandomState = numpy.random) -> numpy.ndarray:
        pass


class Dict(Space):
    def __init__(self, **spaces: Space):
        super().__init__((1,), numpy.dtype([(name, space.dtype, space.shape) for name, space in spaces.items()]))

        self.spaces = spaces

    def sample(self, buffer: memoryview = None, random: numpy.random.RandomState = numpy.random) -> numpy.recarray:
        arrays = self(buffer)

        for name, space in self.spaces.items():
            space.sample(memoryview(arrays[name]), random)

        return arrays.view(numpy.recarray)


class Generic(Space, abc.ABC):
    def __init_subclass__(cls, dtype: numpy.dtype):
        cls.dtype = dtype

    def __init__(self, *shape: int):
        super().__init__(shape, self.dtype)


class Bool(Generic, dtype=numpy.bool_):
    def sample(self, buffer: memoryview = None, random: numpy.random.RandomState = numpy.random) -> numpy.ndarray:
        array = self(buffer)

        numpy.copyto(array, random.randint(0, 2, self.shape, self.dtype), 'no')

        return array


class BoundError(Exception):
    pass


class Number(Generic, abc.ABC, dtype=None):
    def __init__(self, *shape, lower: typing.Union[int, float], upper: typing.Union[int, float]):
        super().__init__(*shape)

        info = None

        if issubclass(self.dtype, numpy.integer):
            info = numpy.iinfo(self.dtype)
        elif issubclass(self.dtype, numpy.floating):
            info = numpy.finfo(self.dtype)

        if lower < info.min:
            raise BoundError(lower)
        if upper > info.max:
            raise BoundError(upper)

        self.lower = lower
        self.upper = upper


class Integer(Number, abc.ABC, dtype=None):
    def sample(self, buffer: memoryview = None, random: numpy.random.RandomState = numpy.random) -> numpy.ndarray:
        array = self(buffer)

        numpy.copyto(array, random.randint(self.lower, self.upper, self.shape, self.dtype), 'no')

        return array


class SignedInteger8(Integer, dtype=numpy.int8):
    pass


class SignedInteger16(Integer, dtype=numpy.int16):
    pass


class SignedInteger32(Integer, dtype=numpy.int32):
    pass


class SignedInteger64(Integer, dtype=numpy.int64):
    pass


class UnsignedInteger8(Integer, dtype=numpy.uint8):
    pass


class UnsignedInteger16(Integer, dtype=numpy.uint16):
    pass


class UnsignedInteger32(Integer, dtype=numpy.uint32):
    pass


class UnsignedInteger64(Integer, dtype=numpy.uint64):
    pass


class Float(Number, abc.ABC, dtype=None):
    def sample(self, buffer: memoryview = None, random: numpy.random.RandomState = numpy.random) -> numpy.ndarray:
        array = self(buffer)

        numpy.copyto(array, random.uniform(self.lower, self.upper, self.shape), 'same_kind')

        return array


class Float16(Float, dtype=numpy.float16):
    pass


class Float32(Float, dtype=numpy.float32):
    pass


class Float64(Float, dtype=numpy.float64):
    pass
