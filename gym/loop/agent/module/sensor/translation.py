import abc

import numpy

from .. import sensor
from ..... import space


class Translation(sensor.Sensor, abc.ABC, space=None):
    def __init_subclass__(
            cls,
            object: str,
            local: bool,
    ):
        super().__init_subclass__(
            space=space.Float32(3, lower=numpy.finfo(numpy.float32).min, upper=numpy.finfo(numpy.float32).max),
            object=object,
        )

        cls.local = local

    def __init__(self, agent):
        super().__init__(agent)

    def __call__(self, buffer: numpy.ndarray):
        if self.local:
            buffer[:] = self.objects.object.localPosition
        else:
            buffer[:] = self.objects.object.worldPosition
