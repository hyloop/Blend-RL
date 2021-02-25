import typing

import bge

from .module import actuator, sensor


class Agent(bge.types.KX_GameObject):
    def __init_subclass__(
            cls,
            actuators: typing.Tuple[typing.Type[actuator.Actuator], ...],
            sensors: typing.Tuple[typing.Type[sensor.Sensor], ...],

    ):
        cls.Actuators = {actuator.__name__: actuator for actuator in actuators}
        cls.Sensors = {sensor.__name__: sensor for sensor in sensors}

        cls.actuators = None
        cls.sensors = None

    def __init__(self, owner: bge.types.KX_GameObject):
        self.actuators = {name: actuator(self) for name, actuator in self.Actuators.items()}
        self.sensors = {name: sensor(self) for name, sensor in self.Sensors.items()}
