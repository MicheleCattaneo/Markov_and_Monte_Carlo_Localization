import numpy as np

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

    def __init__(self, world, x, y, sensor: SensorBase) -> None:
        self.set_position(x, y)
        self.sensor = sensor

        self.world = world
        self.true_measurements = self.precompute_measurements(world.height, world.width)

        self.believe = np.ones_like(self.true_measurements)
        self.believe[~self.world.walkable] = 0
        self.believe /= self.believe.sum()

        print()

    # region Markov

    def precompute_measurements(self, height: int, width: int):
        means = np.zeros((height, width, 8))

        for i in range(means.shape[0]):
            for j in range(means.shape[1]):
                for d in range(means.shape[2]):
                    if not self.world.walkable[i, j]:
                        continue

                    means[i, j, d] = self.sensor.sense(np.array([i, j]) + ROBOT_SIZE, self.Direction(d))

        return means

    def see(self):
        pass

    def act(self, direction: RobotBase.Direction):
        direction = self.directions[direction.value]

    # endregion

    # region Move

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
                print("Would hit the wall, can't do this move.")
                return

            self.set_position(new_pos)
            print(f'New position: {self.position * TILE_SIZE}')

        reading = self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)
        assert reading == self.true_measurements[self.state], "True measurements are incorrect"

        self.on_move.notify()

    # endregion
