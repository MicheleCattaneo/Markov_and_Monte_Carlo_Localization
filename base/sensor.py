import abc

import numpy as np

from base.robot import RobotBase


class SensorBase(abc.ABC):
    @abc.abstractmethod
    def sense(self, xy: np.ndarray, direction: RobotBase.Direction) -> float:
        pass

    @abc.abstractmethod
    def likelihood(self, true_measurements, measurement) -> float:
        pass

    def true_reading(self, xy: np.ndarray, direction: RobotBase.Direction) -> float:
        return self.sense(xy, direction)
