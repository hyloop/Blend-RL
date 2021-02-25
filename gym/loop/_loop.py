import pathlib
import subprocess
import sys
import typing

import bge
import numpy

from . import agent, environment
from .. import space


class RAMDiskNotFoundException(Exception):
    pass


ram_disk = pathlib.Path('/dev/shm')

if not ram_disk.exists():
    raise RAMDiskNotFoundException(f'RAM disk {ram_disk} not found. ')


class Loop:
    @staticmethod
    def _unload(name: str) -> None:
        bge.logic.LibFree(name)

    @staticmethod
    def _create(name: str, seed: str) -> bytes:
        path = pathlib.Path(sys.path[0], name)

        blend = path.joinpath('main.blend')
        py = path.joinpath('main.py')

        temp = ram_disk.joinpath('main.temp')

        try:
            subprocess.run(
                f'blender {blend} --python {py} --background -- --seed {seed} --temp {temp}'.split(' '),
                capture_output=True,
                check=True,
            )

            return temp.read_bytes()
        finally:
            if temp.exists():
                temp.unlink()

    @staticmethod
    def _load(name: str, data: bytes) -> None:
        bge.logic.LibLoad(name, 'Scene', data)

    def __init__(self, agent: typing.Type[agent.Agent], environment: typing.Type[environment.Environment]):
        self._action_space = space.Dict(**{name: actuator.space for name, actuator in agent.Actuators.items()})
        self._observation_space = space.Dict(**{name: sensor.space for name, sensor in agent.Sensors.items()})

        self._Agent = agent
        self._Environment = environment

        self._agent = None
        self._environment = None

        self._random = numpy.random.RandomState()

    @property
    def action_space(self) -> space.Dict:
        return self._action_space

    @property
    def observation_space(self) -> space.Dict:
        return self._observation_space

    def seed(self, seed: int = None) -> None:
        self._random = numpy.random.RandomState(seed)

    def reset(self, buffer: memoryview = None) -> numpy.recarray:
        self._unload('agent')
        self._unload('environment')

        seed = self._random.bytes(8).hex()

        self._load('agent', self._create('agent', seed))
        self._load('environment', self._create('environment', seed))

        scene = bge.logic.getCurrentScene()

        self._agent = self._Agent(scene.objects['_agent'])
        self._environment = self._Environment(scene.objects['_environment'])

        return self._sense(buffer).view(numpy.recarray)

    def render(self):
        pass

    def step(self, action: numpy.ndarray, buffer: memoryview = None) -> numpy.recarray:
        self._actuate(action)

        bge.logic.NextFrame()

        return self._sense(buffer).view(numpy.recarray)  # includes reward, done & info

    def close(self) -> None:
        self._unload('agent')
        self._unload('environment')

        bge.logic.endGame()

    def _sense(self, buffer: memoryview = None) -> numpy.ndarray:
        sensors = self._agent.sensors

        observation = self._observation_space(buffer)

        for name, sensor in sensors.items():
            sensor(observation[0][name])

        return observation.view(numpy.recarray)

    def _actuate(self, action: numpy.ndarray) -> None:
        actuators = self._agent.actuators

        for name, actuator in actuators.items():
            actuator(action[0][name])
