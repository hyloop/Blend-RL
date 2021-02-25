import abc

import numpy
import mathutils
import bge
import re

from .. import sensor
from ..... import space


class SequentialSpatialReward(sensor.Sensor, abc.ABC, space=None):
    class Reward(bge.types.KX_GameObject):

        pattern = re.compile(r'.\w+.(\d+)')

        def __init__(self, o):
            self.i = int(self.pattern.fullmatch(self.name).group(1))

        def __lt__(self, other):
            return self.i < other.i

    def __init_subclass__(
            cls,
            object: str,
            reward_parent: str,
            reward_prefix: str,
            reward_radius: float,
            max_reward: float,
            decay_rate: float,
    ):
        super().__init_subclass__(
            space=space.Float32(2, lower=numpy.finfo(numpy.float32).min, upper=numpy.finfo(numpy.float32).max),
            object=object,
        )

        cls.reward_parent = reward_parent
        cls.reward_prefix = reward_prefix
        cls.reward_radius = reward_radius
        cls.max_reward = max_reward
        cls.decay_rate = decay_rate

    def __init__(self, agent):
        super().__init__(agent)

        self.landscape = agent.scene.objects['_landscape_mesh']
        self.parent = agent.scene.objects[self.reward_parent]
        self.rewards = tuple(
            sorted(
                self.Reward(object) for object in self.parent.childrenRecursive if object.name.startswith(self.reward_prefix)
            )
        )
        self.reward_index = 0
        self.frame_elapsed = 0
        self.is_done = 0  # -1 is bad, 0 is in progress, 1 is good
        self.reward_received = 0

    def __call__(self, buffer: numpy.ndarray):
        buffer[:] = 0

        reward_value = self.max_reward / len(self.rewards)

        reward_object = self.rewards[self.reward_index]

        distance_to_reward = self.objects.object.getDistanceTo(reward_object)

        if distance_to_reward < self.reward_radius:
            self.reward_received += reward_value

            self.reward_index += 1

            # done (good)
            if self.is_done == 0:
                if self.reward_index >= len(self.rewards):
                    self.is_done = 1
        else:
            self.reward_received = 0

        object, point, normal = self.objects.object.rayCast(
            self.objects.object.worldPosition + mathutils.Vector((0.0, 0.0, -1.0)),
            self.objects.object, 1)

        # done (bad)
        if self.is_done == 0:
            if object is self.landscape:
                self.is_done = -1

        self.frame_elapsed += 1

        self.reward_received -= 0.025

        buffer[:] = self.reward_received, self.is_done
