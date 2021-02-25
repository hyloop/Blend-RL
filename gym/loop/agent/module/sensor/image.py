import abc

import bge
import numpy

from .. import sensor
from ..... import space


class Image(sensor.Sensor, abc.ABC, space=None):
    def __init_subclass__(
            cls,
            width: int,
            height: int,
            camera: bge.types.KX_Camera,
    ):
        super().__init_subclass__(
            space=space.UnsignedInteger8(width, height, 4, lower=0, upper=255),
            camera=camera,
        )

    def __init__(self, agent):
        super().__init__(agent)

        w, h, *args = self.space.shape

        camera = self.objects.camera

        self.render = bge.texture.ImageRender(
            camera.scene,
            camera,
            bge.render.offScreenCreate(w, h),
        )
        self.render.flip = True

    def __call__(self, buffer: numpy.ndarray):
        self.render.refresh(buffer)
