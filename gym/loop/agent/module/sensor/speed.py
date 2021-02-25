import abc

import numpy

from .. import sensor
from ..... import space


class Speed(sensor.Sensor, abc.ABC, space=None):
    def __init_subclass__(
            cls,
            car: str,
    ):
        super().__init_subclass__(
            space=space.Float32(1, lower=numpy.finfo(numpy.float32).min, upper=numpy.finfo(numpy.float32).max),
            car=car,
        )

    def __init__(self, agent):
        super().__init__(agent)

    def __call__(self, buffer: numpy.ndarray):
        buffer[:] = self.objects.car.localLinearVelocity.y
