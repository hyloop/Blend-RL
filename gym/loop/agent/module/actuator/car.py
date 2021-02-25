import abc
import dataclasses
import typing

import bge
import numpy

from .. import actuator
from ..... import space, utils


@dataclasses.dataclass(frozen=True)
class Suspension:
    z: float
    rest_length: float
    compression: float
    damping: float
    stiffness: float


@dataclasses.dataclass(frozen=True)
class Wheel:
    suspension: Suspension
    name: bge.types.KX_GameObject
    steer: float
    throttle: float
    brake: float
    roll_influence: float
    tyre_friction: float


class Car(actuator.Actuator, abc.ABC, space=None):
    def __init_subclass__(
            cls,
            car: str,
            cpa: float,
            wheels: typing.Tuple[Wheel, ...],
    ):
        super().__init_subclass__(
            space=space.Float32(2, lower=-1.0, upper=1.0),
            car=car,
        )

        cls.cpa = cpa
        cls.wheels = wheels

    def __init__(self, agent):
        super().__init__(agent)

        constraint_id = bge.constraints.createConstraint(
            self.objects.car.getPhysicsId(),
            0,
            bge.constraints.VEHICLE_CONSTRAINT,
        ).getConstraintId()

        self.constraint = bge.constraints.getVehicleConstraint(constraint_id)

        for i, wheel in enumerate(self.wheels):
            self.add_wheel(agent, i, wheel)

    def add_wheel(self, agent: bge.types.KX_GameObject, i: int, wheel: Wheel):
        wheel_object = agent.groupMembers[wheel.name]

        position = wheel_object.localPosition.copy()
        radius = utils.mesh.get_dimensions(wheel_object).yz.length / 2 ** 0.5 / 2

        self.constraint.addWheel(
            wheel_object,
            position,
            (0, 0, -1),
            (1, 0, 0),
            wheel.suspension.rest_length,
            radius,
            bool(wheel.steer),
        )

        self.constraint.setTyreFriction(wheel.tyre_friction, i)
        self.constraint.setRollInfluence(wheel.roll_influence, i)
        self.constraint.setSuspensionStiffness(wheel.suspension.stiffness, i)
        self.constraint.setSuspensionDamping(wheel.suspension.damping, i)
        self.constraint.setSuspensionCompression(wheel.suspension.compression, i)

    def __call__(self, buffer: numpy.ndarray):
        steer, arg = buffer

        throttle = brake = 0.0

        if arg > 0:
            throttle = arg
        else:
            brake = arg

        speed = self.objects.car.localLinearVelocity.y

        self.objects.car.applyForce(
            self.cpa * numpy.array(self.objects.car.localLinearVelocity.to_tuple(), dtype=numpy.float) ** 2,
            True,
        )

        for i, wheel in enumerate(self.wheels):
            if wheel.steer:
                if speed > 20:
                    steering_sensitivity = 0.333
                elif speed > 10:
                    steering_sensitivity = 0.666
                else:
                    steering_sensitivity = 1.0
                self.constraint.setSteeringValue(wheel.steer * steer * steering_sensitivity, i)

            if wheel.throttle:
                self.constraint.applyEngineForce(wheel.throttle * throttle, i)

            if wheel.brake:
                if speed > 0.27:
                    self.constraint.applyBraking(wheel.brake * brake, i)
                else:
                    self.constraint.applyBraking(0.0, i)
