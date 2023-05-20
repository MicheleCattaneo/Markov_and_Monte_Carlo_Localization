import numpy as np
from PIL import Image

from base.sensor import SensorBase
from base.movement_models import InvalidActionException, MovementModelBase
from definitions import *
from base.robot import RobotBase
from scipy.signal import convolve2d
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.ndimage import rotate
from scipy.stats import norm


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
        # reset sensor to fit the robots position
        self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)
        return means

    def measurement_probability(self, measurement: float) -> np.ndarray:
        """
        Given a measurement, returns the probability
        of being at a position and measuring the given measurement.
        """
        return np.isclose(self.true_measurements, measurement).astype('int')

    def measurement_probability_uncertain(self, measurement: float) -> np.ndarray:
        # create nd-array of gaussians, centered at the true measurement.
        std = 1.
        gaussians = np.random.normal(self.true_measurements, std, size=self.true_measurements.shape)

        # Sample the measurement from the PDFs 
        return norm.pdf(measurement, gaussians)

    def see(self, measurement):
        self.belief = self.measurement_probability_uncertain(measurement) * self.belief
        self.belief = self.belief / self.belief.sum()

        # assert np.isclose(self.belief.sum(), 1.), f'sum is not 1 {self.belief.sum()}'

    def act(self, action: RobotBase.Action):
        try:
            filter = self.movement_model.get_filter(action)
            for i in range(filter.shape[-1]):
                self.belief[:, :, i] = convolve2d(self.belief[:, :, i], filter[:, :, i], mode='same')
            return
        except InvalidActionException:
            pass
        direction = 1 if action == action.TURN_RIGHT else -1
        self.belief = np.roll(self.belief, shift=direction, axis=2)

    # endregion

    def plot_8_orientations(self):
        plt.close()
        colormap=sns.color_palette("PuBuGn", as_cmap=True)
        fig, ax = plt.subplots(3, 3, figsize=(12, 12))

        indices = [
            [7, 0, 1],
            [6, None, 2],
            [5, 4, 3]
        ]
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    img = np.asarray(Image.open("rob.png"))
                    img = rotate(img, 90 - 45*self.orientation.value, reshape=False)
                    ax[i, j].imshow(img)
                    ax[i, j].axis("off")
                    continue
                idx = indices[i][j]
                sns.heatmap(self.belief[:, :, idx].T, ax=ax[i, j], linewidths=0.1, cmap=colormap)
                ax[i, j].title.set_text(self.Direction(idx).name.replace("_", " "))

                ax[i, j].invert_yaxis()
        fig.savefig("plots/probs.png")
        # fig.show()

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
