import numpy as np

from base.sensor import SensorBase
from base.movement_models import InvalidActionException, MovementModelBase
from definitions import *
from base.robot import RobotBase
from scipy.signal import convolve2d
import seaborn as sns
import matplotlib.pyplot as plt


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

    def __init__(self, world, x, y, movement_model: MovementModelBase, sensor: SensorBase) -> None:
        self.set_position(x, y)
        self.sensor = sensor

        self.world = world
        self.true_measurements = self.precompute_measurements(world.width, world.height)

        self.belief = np.ones_like(self.true_measurements)
        self.belief[~self.world.walkable] = 0
        self.belief /= self.belief.sum()

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(self.world.walkable, ax=ax, linewidths=0.1)
        fig.savefig('./plots/walkable_belief_up.png')

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(self.belief[:, :, 0], ax=ax, linewidths=0.1)
        fig.savefig('./plots/first_belief_up.png')

        for i in range(8):
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.heatmap(self.true_measurements[:, :, i], ax=ax, linewidths=0.1)
            fig.savefig(f'./plots/true_measurements_{i}.png')

        self.movement_model = movement_model

        print()

    # region Markov

    def precompute_measurements(self, width: int, height: int):
        orientations = 8
        means = np.zeros((width, height, orientations))

        for i in range(width):
            for j in range(height):
                for d in range(orientations):
                    if not self.world.walkable[i, j]:
                        continue

                    means[i, j, d] = self.sensor.sense(np.array([i, j]) + ROBOT_SIZE, self.Direction(d))
        means.setflags(write=False)
        return means

    def measurement_probability(self, measurement: float) -> float:
        """
        Given a measurement, returns the probability
        of being at a position and measuring the given measurement.
        """
        return np.isclose(self.true_measurements, measurement).astype('int')

    def measurement_probability_uncertain(self, measurement: float, location: tuple) -> float:
        pass

    def see(self, measurement):
        self.belief = self.measurement_probability(measurement) * self.belief
        self.belief = self.belief / self.belief.sum()

        # assert np.isclose(self.belief.sum(), 1.), f'sum is not 1 {self.belief.sum()}'

    def act(self, action: RobotBase.Action):
        try:
            filter = self.movement_model.get_filter(action)
            for i in range(filter.shape[-1]):
                self.belief[:, :, i] = convolve2d(self.belief[:, :, i], filter[:, :, i], mode='same', boundary="wrap")
            return
        except InvalidActionException:
            pass
        direction = 1 if action == action.TURN_RIGHT else -1
        self.belief = np.roll(self.belief, shift=direction, axis=2)

    # endregion

    def plot_8_orientations(self):
        fig, ax = plt.subplots(3, 3, figsize=(12, 12))

        row, col = 0, 0
        j = 0
        for _ in range(9):
            if row == 1 and col == 1:
                col += 1
                continue
            sns.heatmap(self.belief[:, :, j].T, ax=ax[row, col], linewidths=0.1)
            ax[row, col].invert_yaxis()
            col += 1
            j += 1
            if col % 3 == 0:
                col = 0
                row += 1
        fig.savefig("plots/probs.png")
        fig.show()

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
                return
            self.set_position(new_pos)

        reading = self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)
        assert reading == self.true_measurements[self.state], "True measurements are incorrect"

        self.act(action)
        self.see(reading)

        self.plot_8_orientations()

        # fig, ax = plt.subplots(figsize=(8, 4))
        # sns.heatmap(self.belief[:, :, (8-self.orientation.value)%8].T, ax=ax, linewidths=0.1)
        # ax.invert_yaxis()
        # fig.savefig('./plots/prob_belief_up.png')
        # fig.show()

        self.on_move.notify()

    # endregion
