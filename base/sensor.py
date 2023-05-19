import abc

import numpy as np

from base.robot import RobotBase


class SensorBase(abc.ABC):
    @abc.abstractmethod
    def sense(self, xy: np.ndarray, direction: RobotBase.Direction):
        pass