import numpy as np

from base.localization import LocalizationBase
from base.sensor import SensorBase
from definitions import *
from base.robot import RobotBase


class Robot(RobotBase):
    directions = [
        np.array([0, 1]),
        np.array([1, 1]),
        np.array([1, 0]),
        np.array([1, -1]),
        np.array([0, -1]),
        np.array([-1, -1]),
        np.array([-1, 0]),
        np.array([-1, 1])
    ]

    def __init__(self, world, x, y, sensor: SensorBase, localization: LocalizationBase) -> None:
        self.set_position(x, y)
        self.sensor = sensor

        self.world = world
        self.localization = localization

        # reset sensor to fit the robots position
        self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)

        # fig, ax = plt.subplots(figsize=(8, 4))
        # sns.heatmap(self.world.walkable, ax=ax, linewidths=0.1)
        # fig.savefig('./plots/walkable_belief_up.png')
        #
        # fig, ax = plt.subplots(figsize=(8, 4))
        # sns.heatmap(self.belief[:, :, 0], ax=ax, linewidths=0.1)
        # fig.savefig('./plots/first_belief_up.png')
        #
        # for i in range(8):
        #     fig, ax = plt.subplots(figsize=(8, 4))
        #     sns.heatmap(self.true_measurements[:, :, i], ax=ax, linewidths=0.1)
        #     fig.savefig(f'./plots/true_measurements_{i}.png')

    def move(self, action: RobotBase.Action):
        if action == action.TURN_LEFT:
            self.orientation = self.Direction((self.orientation.value - 1) % len(self.Direction))
        elif action == action.TURN_RIGHT:
            self.orientation = self.Direction((self.orientation.value + 1) % len(self.Direction))
        else:
            move_dir = self.orientation.value \
                if action == action.FORWARD \
                else (self.orientation.value + 4) % len(self.Direction)

            new_pos = self.position + Robot.directions[move_dir]

            # get i,j coordinates and check whether that tile is occupied by an object (obstacle)
            if not self.world.walkable[tuple(new_pos.astype(int))]:
                return
            self.set_position(new_pos)

        reading = self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)

        self.localization.act(action)
        self.localization.see(reading)

        self.on_move.notify()
