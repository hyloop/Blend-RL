import abc
import types

import numpy

from .... import space


class Module:
    @abc.abstractmethod
    def __init_subclass__(cls, space: space.Space, **objects: str):
        cls.space = space
        cls.objects = objects

    @abc.abstractmethod
    def __init__(self, agent):
        self.objects = types.SimpleNamespace(
            **{name: agent.groupMembers[object] for name, object in self.objects.items()}
        )

    @abc.abstractmethod
    def __call__(self, buffer: numpy.ndarray) -> None:
        pass
