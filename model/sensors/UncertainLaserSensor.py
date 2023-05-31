import numpy as np

from scipy.stats import norm

from definitions import MEASUREMENT_SIGMA
from base.robot import RobotBase
from model.sensors.LaserSensor import LaserSensor


class UncertainLaserSensor(LaserSensor):
    """Represents an uncertain sensor. Each reading is subject to 
    gaussian noise.

    """    
    def sense(self, xy: np.ndarray, direction: RobotBase.Direction) -> np.ndarray:   
        reading = self.true_reading(xy, direction)
        return reading + np.random.normal(0, MEASUREMENT_SIGMA, size=1)

    def true_reading(self, xy: np.ndarray, direction: RobotBase.Direction):
        return super().sense(xy, direction)

    def likelihood(self, true_measurements, measurement):
        return norm.pdf(measurement, true_measurements, MEASUREMENT_SIGMA)
