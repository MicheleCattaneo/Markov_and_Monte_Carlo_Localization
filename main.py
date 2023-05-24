from definitions import *

import numpy as np
import pyglet
from pyglet import app
from pyglet.window import Window
from pyglet.window import key

import os

from model.robot import Robot
from model.environment import GridWorld
from model.movement_model import DiscreteMovementModel, UncertainMovementModel
from model.localization import MarkovLocalization, UncertainMarkovLocalization
from model.sensors import LaserSensor, UncertainLaserSensor

from view.robot import RobotView
from view.probs_grid import LocalizationBeliefView


def update(dt: float) -> None:
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

        robot.move(Robot.Action(int(r * 4)))


if __name__ == '__main__':
    os.makedirs('plots', exist_ok=True)

    # region Pyglet Setup

    # Enable transparency
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)

    # Set the blending function
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    window = Window(height=RES_HEIGHT, width=RES_WIDTH)
    env_batch = pyglet.graphics.Batch()
    rob_batch = pyglet.graphics.Batch()

    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    # endregion

    # region Variable Initializations

    world = GridWorld(RES_WIDTH, RES_HEIGHT, TILE_SIZE, env_batch)

    sensor = UncertainLaserSensor(
        (ROBOT_START_X + ROBOT_SIZE) * TILE_SIZE, (ROBOT_START_Y + ROBOT_SIZE) * TILE_SIZE,
        world, SENSOR_LENGTH, rob_batch)
    localization = UncertainMarkovLocalization(world, sensor, UncertainMovementModel())

    robot = Robot(world, ROBOT_START_X, ROBOT_START_Y, sensor, localization)

    robot_view = RobotView(robot, rob_batch)
    probabilities_view = LocalizationBeliefView(robot, world, env_batch)

    # endregion

    # region Pyglet Run

    @window.event
    def on_draw():
        window.clear()
        env_batch.draw()
        rob_batch.draw()


    pyglet.clock.schedule_interval(update, 1/FPS)
    app.run()

    # endregion
