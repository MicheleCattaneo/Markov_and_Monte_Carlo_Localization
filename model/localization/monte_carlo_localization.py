import numpy as np
from scipy.signal import convolve2d

from base.localization import LocalizationBase
from base.movement_models import InvalidActionException, MovementModelBase
from base.robot import RobotBase
from base.sensor import SensorBase
from definitions import ROBOT_SIZE
from model.continuous_world import ContinuousWorld

class MonteCarloLocalization(LocalizationBase):
	def __init__(self, world: ContinuousWorld, sensor: SensorBase) -> None:
		self.world = world
		self.sensor = sensor

	def measurement_probability(self, measurement: float) -> np.ndarray:
		"""
		Given a measurement, returns the probability
		of being at a position and measuring the given measurement.
		"""
		return np.isclose(self.true_measurements, measurement).astype('int')

	def see(self, measurement: float) -> None:
		pass

	def act(self, action: RobotBase.Action) -> None:
		pass