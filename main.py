from definitions import *

import numpy as np
import pyglet
from pyglet import app
from pyglet.window import Window

import sys

from shapely import affinity

from environment import GridWorld
from robot import Robot
from pyglet.window import key


COMMAND_TYPE = 'AUTO'


def update(dt):
    print(f'Dt={dt}')

    if COMMAND_TYPE == 'KEYBOARD':
        if keys[key.UP]:
            robot.deterministic_move(Robot.Direction.UP)
        elif keys[key.DOWN]:
            robot.deterministic_move(Robot.Direction.DOWN)
        elif keys[key.LEFT]:
            robot.deterministic_move(Robot.Direction.LEFT)
        elif keys[key.RIGHT]:
            robot.deterministic_move(Robot.Direction.RIGHT)
        robot.get_intersection(world)
    else:
        r = np.random.random()

        if r > 0.5:
            robot.deterministic_move(Robot.Direction.DOWN_LEFT)
        else:
            robot.deterministic_move(Robot.Direction.DOWN_RIGHT)

        robot.get_intersection(world)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == 'keyboard':
            COMMAND_TYPE = 'KEYBOARD'

    window = Window(height=RES_HEIGHT, width=RES_WIDTH)
    env_batch = pyglet.graphics.Batch()
    rob_batch = pyglet.graphics.Batch()

    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    world = GridWorld((RES_HEIGHT, RES_WIDTH), TILE_SIZE, SENSOR_LENGTH, env_batch)
    robot = Robot(world, 500, 500, rob_batch, sensor_length=SENSOR_LENGTH)

    dd = True

    print(robot.sensor.shapely_shape.coords.xy)
    print(affinity.rotate(robot.sensor.shapely_shape, 90, origin=(robot.sensor.x, robot.sensor.y)))


    @window.event
    def on_draw():
        window.clear()
        env_batch.draw()
        rob_batch.draw()


    pyglet.clock.schedule_interval(update, 0.1)
    app.run()
