import abc
from base.robot import RobotBase
import numpy as np


class InvalidActionException(Exception):
    pass


class MovementModelBase(abc.ABC):

    @abc.abstractmethod
    def _get_convolution_forward(self):
        pass

    @abc.abstractmethod
    def _get_convolution_backward(self):
        pass

    def get_filter(self, action: RobotBase.Action) -> np.ndarray:
        if action == action.FORWARD:
            return self._get_convolution_forward()

        if action == action.BACKWARD:
            return self._get_convolution_backward()

        raise InvalidActionException('Invalid action, turns do not need convolutions.')
