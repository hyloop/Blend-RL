import abc

import numpy

from .. import actuator
from ..... import space


class Translation(actuator.Actuator, abc.ABC, space=None):
    def __init_subclass__(
            cls,
            lower: float,
            upper: float,
            object: str,
            local: bool,
    ):
        super().__init_subclass__(
            space=space.Float32(3, lower=lower, upper=upper),
            object=object,
        )

        cls.local = local

    def __init__(self, agent):
        super().__init__(agent)

    def __call__(self, buffer: numpy.ndarray):
        self.objects.object.applyMovement(buffer, self.local)
