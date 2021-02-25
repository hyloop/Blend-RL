import abc
import collections

import bge
import numpy

from .. import sensor
from ..... import space


class LinearAcceleration3D(sensor.Sensor, abc.ABC, space=None):
    def __init_subclass__(
            cls,
            car: str,
            average: int,
    ):
        super().__init_subclass__(
            space=space.Float32(3, lower=numpy.finfo(numpy.float32).min, upper=numpy.finfo(numpy.float32).max),
            car=car,
        )

        cls.average = average

    def __init__(self, agent):
        super().__init__(agent)

        self.last_n_velocities = collections.deque(maxlen=self.average)

    def __call__(self, buffer: numpy.ndarray):
        velocity = self.objects.car.localLinearVelocity.copy()

        self.last_n_velocities.append(velocity)

        average_velocity = None

        for velocity in self.last_n_velocities:
            if average_velocity is None:
                average_velocity = velocity
            else:
                average_velocity += velocity

        average_velocity /= len(self.last_n_velocities)

        frame_rate = bge.logic.getLogicTicRate()

        buffer[:] = self.objects.car.localLinearVelocity - average_velocity


class AngularAcceleration3D(sensor.Sensor, abc.ABC, space=None):
    def __init_subclass__(
            cls,
            car: str,
            average: int,
    ):
        super().__init_subclass__(
            space=space.Float32(3, lower=numpy.finfo(numpy.float32).min, upper=numpy.finfo(numpy.float32).max),
            car=car,
        )

        cls.average = average

    def __init__(self, agent):
        super().__init__(agent)

        self.last_n_velocities = collections.deque(maxlen=self.average)

    def __call__(self, buffer: numpy.ndarray):
        velocity = self.objects.car.localAngularVelocity.copy()

        self.last_n_velocities.append(velocity)

        average_velocity = None

        for velocity in self.last_n_velocities:
            if average_velocity is None:
                average_velocity = velocity
            else:
                average_velocity += velocity

        average_velocity /= len(self.last_n_velocities)

        frame_rate = bge.logic.getLogicTicRate()

        buffer[:] = self.objects.car.localAngularVelocity - average_velocity
