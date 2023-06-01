import numpy as np

from base.localization import LocalizationBase
from base.robot import RobotBase
from base.sensor import SensorBase
from definitions import *


class ContinuousRobot(RobotBase):
    def __init__(self, world, x, y, sensor: SensorBase, localization: LocalizationBase) -> None:
        self.sensor = sensor
        self.set_position(x, y)

        self.world = world
        self.localization = localization

        # reset sensor to fit the robots position
        self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)

    def move(self, action: RobotBase.Action, dt: float):
        self.current_action = action

        if action == action.TURN_LEFT:
            self.orientation = self.Direction((self.orientation.value - 1) % len(self.Direction))
        elif action == action.TURN_RIGHT:
            self.orientation = self.Direction((self.orientation.value + 1) % len(self.Direction))
        else:

            uncertainty_multiplier = 1.

            move_dir = self.orientation.value \
                if action == action.FORWARD \
                else (self.orientation.value + 4) % len(self.Direction)

            speed_mult = SPEED * dt
            new_pos = self.position + uncertainty_multiplier * speed_mult * ContinuousRobot.directions[
                move_dir] * TILE_SIZE / np.linalg.norm(ContinuousRobot.directions[move_dir] * TILE_SIZE)

            new_center = (new_pos + ROBOT_SIZE) * TILE_SIZE
            if not self.world.check_within_boundaries(new_center[0], new_center[1]) or self.world.is_occupied(
                    new_center[0], new_center[1]):
                return
            self.set_position(new_pos)

        reading = self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)[0]

        self.localization.act(action)
        self.localization.see(reading)

        self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)

        self.on_move.notify()
