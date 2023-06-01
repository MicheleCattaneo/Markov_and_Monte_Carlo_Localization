from definitions import *

import numpy as np
import pyglet
from pyglet import app
from pyglet.window import Window
from pyglet.window import key

import os

from model.robots import DiscreteRobot, ContinuousRobot
from model.grid_world import GridWorld
from model.continuous_world import ContinuousWorld
from model.movement_model import UncertainMovementModel, MovementModel
from model.localization import MarkovLocalization, MonteCarloLocalization, UncertainMarkovLocalization
from model.sensors import UncertainLaserSensor, LaserSensor

from view.robot import RobotView
from view.laser_sensor import LaserSensorView
from view.probs_grid import LocalizationBeliefView
from view.probs_particle import ParticleView


def update(dt: float) -> None:
    if not robot_view.allow_move:
        robot_view.update()
    elif COMMAND_TYPE == 'KEYBOARD':
        robot_view.update()
        if keys[key.UP]:
            robot.move(DiscreteRobot.Action.FORWARD, dt)
        elif keys[key.DOWN]:
            robot.move(DiscreteRobot.Action.BACKWARD, dt)
        elif keys[key.LEFT]:
            robot.move(DiscreteRobot.Action.TURN_LEFT, dt)
        elif keys[key.RIGHT]:
            robot.move(DiscreteRobot.Action.TURN_RIGHT, dt)
    else:
        r = np.random.random()

        robot.move(DiscreteRobot.Action(int(r * 4)), dt)


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

    if SIM_TYPE == "DISCRETE":
        world = GridWorld(RES_WIDTH, RES_HEIGHT, TILE_SIZE, env_batch)
        sensor = UncertainLaserSensor(world, SENSOR_LENGTH)
        localization = UncertainMarkovLocalization(world, sensor, UncertainMovementModel(np.array([0.8, 0.2, 0.0])))
        robot = DiscreteRobot(world, ROBOT_START_X, ROBOT_START_Y, sensor, localization)
        probabilities_view = LocalizationBeliefView(robot, world, env_batch)

    elif SIM_TYPE == "CONTINUOUS":
        world = ContinuousWorld(RES_WIDTH, RES_HEIGHT, TILE_SIZE, env_batch)
        sensor = UncertainLaserSensor(world, SENSOR_LENGTH)
        localization = MonteCarloLocalization(world, sensor, NUM_PARTICLES)
        robot = ContinuousRobot(world, ROBOT_START_X, ROBOT_START_Y, sensor, localization)
        probabilities_view = ParticleView(localization, robot, env_batch)

    robot_view = RobotView(robot, rob_batch)
    laser_view = LaserSensorView(robot, sensor, rob_batch)

    # endregion

    # region Pyglet Run

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == 1:
            robot.teleport(x,y)

    @window.event
    def on_draw():
        window.clear()
        env_batch.draw()
        rob_batch.draw()

    pyglet.clock.schedule_interval(update, 1/FPS)
    app.run()

    # endregion
