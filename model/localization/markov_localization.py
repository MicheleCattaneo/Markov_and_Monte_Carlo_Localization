import numpy as np
from scipy.signal import convolve2d

from base.localization import LocalizationBase
from base.movement_models import InvalidActionException, MovementModelBase
from base.robot import RobotBase
from base.sensor import SensorBase
from definitions import ROBOT_SIZE
from model.environment import GridWorld


class MarkovLocalization(LocalizationBase):
    """ Represents the logic for Markov Localization assuming perfect measurements.
        The probability of a measurement i given a pose l is defined as follows:
            p(i|l) = 1 if i is eps-close to the true measurement and 0 otherwise.
    """    

    def __init__(self, world: GridWorld, sensor: SensorBase, movement_model: MovementModelBase) -> None:
        self.world = world
        self.sensor = sensor
        self.movement_model = movement_model

        self.true_measurements = self._precompute_measurements(world.width, world.height)

        self.belief = np.ones_like(self.true_measurements)
        
        self.mask_out_belief_on_obstacles()
        self.normalize_belief()
        
    def mask_out_belief_on_obstacles(self):
        """Annihilates likelihood that ended up in non walkbable regions due to
        convolutions. This function does not normalize the belief to sum up to 1.
        """        
        self.belief[~self.world.walkable] = 0

    def normalize_belief(self):
        """Normalizes the belief to sum up to 1.
        """        
        self.belief /= self.belief.sum()

    def _precompute_measurements(self, width: int, height: int):
        orientations = 8
        means = np.zeros((width, height, orientations))

        for i in range(width):
            for j in range(height):
                for d in range(orientations):
                    if not self.world.walkable[i, j]:
                        continue

                    means[i, j, d] = self.sensor.true_reading(np.array([i, j]) + ROBOT_SIZE, RobotBase.Direction(d))

        return means

    def measurement_probability(self, measurement: float) -> np.ndarray:
        """
        Given a measurement, returns the probability
        of being at a position and measuring the given measurement.
        """
        return np.isclose(self.true_measurements, measurement).astype('int')

    def see(self, measurement: float) -> None:
        self.belief = self.measurement_probability(measurement) * self.belief

        self.belief = self.belief / self.belief.sum()

    def act(self, action: RobotBase.Action) -> None:
        try:
            filter = self.movement_model.get_filter(action)
            for i in range(filter.shape[-1]):
                self.belief[:, :, i] = convolve2d(self.belief[:, :, i], filter[:, :, i], mode='same')

            self.mask_out_belief_on_obstacles()
            self.normalize_belief()
            return
        except InvalidActionException:
            pass
        direction = 1 if action == action.TURN_RIGHT else -1
        self.belief = np.roll(self.belief, shift=direction, axis=2)



