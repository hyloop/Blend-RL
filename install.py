import bpy
import pathlib
import argparse
import sys

s1 = '''
from gym import *


class MyAgent(
    Agent,
    sensors=(),
    actuators=(),
):
    pass


class MyEnvironment(
    Environment
):
    pass


loop = Loop(MyAgent, MyEnvironment)

loop.seed(0)

for e in range(10):
    observation = loop.reset()
    for t in range(100):
        # loop.render()
        print(observation)
        action = loop.action_space.sample()
        observation, reward, done, info = loop.step(action), None, None, None
        if done:
            print(f'Episode finished after {t + 1} time steps. ')
            break

loop.close()

'''


s2 = '''
def generate(seed, temp) -> None:
    import bpy
    # todo
    bpy.ops.wm.save_as_mainfile(filepath=temp)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=str, required=True, metavar='SEED', dest='seed')
    parser.add_argument('-t', '--temp', type=str, required=True, metavar='TEMP', dest='temp')

    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])

    generate(args.seed, args.temp)

'''


def init(resolution_x: int, resolution_y: int, physics_fps: int, physics_gravity: float, realtime: bool, debug: bool):
    scene = bpy.data.scenes.get('_main')

    scene.render.engine = 'BLENDER_GAME'

    # aspect ratio
    scene.render.resolution_x, scene.render.resolution_y = 1, 1

    # resolution
    scene.game_settings.resolution_x, scene.game_settings.resolution_y = resolution_x, resolution_y

    scene.game_settings.material_mode = 'GLSL'

    # frame rate
    scene.game_settings.use_frame_rate = realtime
    scene.game_settings.vsync = 'OFF'

    # display
    scene.game_settings.show_debug_properties = debug
    scene.game_settings.show_framerate_profile = debug
    scene.game_settings.show_mouse = True
    scene.game_settings.show_physics_visualization = debug
    scene.game_settings.use_deprecation_warnings = debug

    # physics
    scene.game_settings.fps = physics_fps
    scene.game_settings.physics_gravity = physics_gravity
    scene.game_settings.physics_step_sub = 1
    scene.game_settings.logic_step_max = 1
    scene.game_settings.physics_step_max = 1
    scene.game_settings.deactivation_time = 0.0

    # etc
    scene.game_settings.use_occlusion_culling = False
    scene.game_settings.use_scene_hysteresis = False

    scene.camera = None

    scene.unit_settings.system = 'METRIC'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    viewport = parser.add_argument_group('Viewport')
    viewport.add_argument('--width', default=640, type=int, required=False, metavar='WIDTH', dest='viewport_width')
    viewport.add_argument('--height', default=640, type=int, required=False, metavar='HEIGHT', dest='viewport_height')

    physics = parser.add_argument_group('Physics')
    physics.add_argument('--fps', default=60, type=int, required=False, metavar='FPS', dest='physics_fps')
    physics.add_argument('--gravity', default=10, type=float, required=False, metavar='GRAVITY', dest='physics_gravity')

    parser.add_argument('--realtime', action='store_true', dest='realtime')
    parser.add_argument('--debug', action='store_true', dest='debug')

    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])

    main = pathlib.Path.cwd()

    agent = main.joinpath('agent')
    environment = main.joinpath('environment')

    for directory in (main, agent, environment):
        if not directory.exists():
            directory.mkdir()

        py = directory.joinpath('main.py')

        if not py.exists():
            py.write_text(s1 if directory is main else s2)

        blend = directory.joinpath('main.blend')

        if not blend.exists():
            bpy.ops.wm.read_homefile()

            scene = bpy.data.scenes.new('_main')

            for s in bpy.data.scenes:
                if s != scene:
                    bpy.data.scenes.remove(s, do_unlink=True)

            if directory is main:
                text = bpy.data.texts.new('_main')
                text.from_string('import main')

                scene['__main__'] = text.name
            elif directory is agent:
                agent = bpy.data.objects.new('_agent', object_data=None)
                agent.empty_draw_type = 'ARROWS'
                agent.empty_draw_size = 1
                scene.objects.link(agent)
            elif directory is environment:
                environment = bpy.data.objects.new('_environment', object_data=None)
                environment.empty_draw_type = 'CUBE'
                environment.empty_draw_size = 1
                scene.objects.link(environment)
            else:
                pass

            bpy.ops.wm.save_as_mainfile(filepath=str(blend))

        bpy.ops.wm.open_mainfile(filepath=str(blend))

        init(
            args.viewport_width,
            args.viewport_height,
            args.physics_fps,
            args.physics_gravity,
            args.realtime,
            args.debug,
        )

        bpy.ops.wm.save_as_mainfile(filepath=str(blend))
