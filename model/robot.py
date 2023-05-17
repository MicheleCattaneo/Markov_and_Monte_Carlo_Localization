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

    def __init__(self, world, x, y, movement_model: MovementModelBase ,sensor: SensorBase) -> None:
        self.set_position(x, y)
        self.sensor = sensor

        self.world = world
        self.true_measurements = self.precompute_measurements(world.height, world.width)

        self.belief = np.ones_like(self.true_measurements)
        self.belief[~self.world.walkable] = 0
        self.belief /= self.belief.sum()

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(self.world.walkable, ax=ax, linewidths=0.1)
        # ax.invert_yaxis()
        fig.savefig('./plots/walkable_belief_up.png')

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(self.belief[:,:,0], ax=ax, linewidths=0.1)
        # ax.invert_yaxis()
        fig.savefig('./plots/first_belief_up.png')

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(np.nan_to_num(self.true_measurements.max(axis=2), posinf=-1), ax=ax, linewidths=0.1)
        # ax.invert_yaxis()
        fig.savefig('./plots/true_measurements.png')

        self.movement_model = movement_model

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
    
    def measurement_probability(self, measurement: float) -> float:
        '''
        Given a measurement, returns the probability 
        of being at a position and measuring the given measurement.
        '''
        return np.isclose(self.true_measurements, measurement).astype('int')
    
    def measurement_probability_uncertain(self, measurement: float, location: tuple) -> float:
        pass

    def see(self, measurement):
        self.belief = self.measurement_probability(measurement) * self.belief
        print(self.belief.sum(), 'sum belief')
        self.belief = self.belief / self.belief.sum()

        # assert np.isclose(self.belief.sum(), 1.), f'sum is not 1 {self.belief.sum()}'

    def act(self, action: RobotBase.Action):
        try:
            filter = self.movement_model.get_filter(action)
            for i in range(filter.shape[-1]):
                self.belief[:,:,i] = convolve2d(self.belief[:,:,i], filter[:,:,i], mode='same')
        except InvalidActionException:
            pass

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
            if self.world.walkable[tuple(new_pos.astype(int))]:
                self.set_position(new_pos)


            print(f'Current position: {self.position * TILE_SIZE}')

        reading = self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)
        print(reading, 'reading')
        assert reading == self.true_measurements[self.state], "True measurements are incorrect"

        self.act(action)
        self.see(reading)

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(self.belief[:,:,0], ax=ax, linewidths=0.1)
        ax.invert_yaxis()
        fig.savefig('./plots/prob_belief_up.png')

        self.on_move.notify()

    # endregion
