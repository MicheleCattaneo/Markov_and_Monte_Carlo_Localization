import numpy as np

from definitions import MEASUREMENT_SIGMA
from base.robot import RobotBase
from model.sensors.LaserSensor import LaserSensor


class UncertainLaserSensor(LaserSensor):
    def sense(self, xy: np.ndarray, direction: RobotBase.Direction) -> np.ndarray:
        reading = self.true_reading(xy, direction)
        return reading + np.random.normal(0, MEASUREMENT_SIGMA, size=1)

    def true_reading(self, xy: np.ndarray, direction: RobotBase.Direction):
        return super().sense(xy, direction)
