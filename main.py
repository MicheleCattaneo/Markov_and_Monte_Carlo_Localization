from definitions import *

import numpy as np
import pyglet
from pyglet import app
from pyglet.window import Window

import sys

from shapely import affinity

from model.environment import GridWorld
from model.robot import Robot
from pyglet.window import key

from model.sensor import LaserSensor
from view.robot import RobotView

from model.movement_model import DiscreteMovementModel


def update(dt):
    print(f'Dt={dt}', np.argwhere(robot.belief == robot.belief.max()), "max prob position")

    if COMMAND_TYPE == 'KEYBOARD':
        if keys[key.UP]:
            robot.move(Robot.Action.FORWARD)
        elif keys[key.DOWN]:
            robot.move(Robot.Action.BACKWARD)
        elif keys[key.LEFT]:
            robot.move(Robot.Action.TURN_LEFT)
        elif keys[key.RIGHT]:
            robot.move(Robot.Action.TURN_RIGHT)
    else:
        r = np.random.random()

        robot.move(Robot.Action(int(r*4)))



if __name__ == '__main__':

    window = Window(height=RES_HEIGHT, width=RES_WIDTH)
    env_batch = pyglet.graphics.Batch()
    rob_batch = pyglet.graphics.Batch()

    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    world = GridWorld((RES_WIDTH, RES_HEIGHT), TILE_SIZE, SENSOR_LENGTH, env_batch)

    sensor = LaserSensor(20+TILE_SIZE*ROBOT_SIZE, 10+TILE_SIZE*ROBOT_SIZE, world, SENSOR_LENGTH, rob_batch)
    robot = Robot(world, 20//TILE_SIZE, 10//TILE_SIZE, DiscreteMovementModel(), sensor)
    robot_view = RobotView(robot, rob_batch)

    @window.event
    def on_draw():
        window.clear()
        env_batch.draw()
        rob_batch.draw()


    pyglet.clock.schedule_interval(update, 0.1)
    app.run()
