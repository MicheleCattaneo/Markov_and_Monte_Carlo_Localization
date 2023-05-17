import abc
from enum import Enum
from typing import Optional, Union, Tuple

import numpy as np

from base.observer_pattern import Subject


class RobotBase(abc.ABC):
    class Direction(Enum):
        """
        Mapping between a direction and an index
        """
        UP = 0
        UP_RIGHT = 1
        RIGHT = 2
        DOWN_RIGHT = 3
        DOWN = 4
        DOWN_LEFT = 5
        LEFT = 6
        UP_LEFT = 7

    class Action(Enum):
        """
        Possible actions of the robot
        """
        FORWARD = 0
        BACKWARD = 1
        TURN_LEFT = 2
        TURN_RIGHT = 3

    orientation: Direction = Direction.UP
    """
    Array containing the x, y coordinate of the robot.
    """
    position: np.ndarray

    on_move: Subject = Subject()

    @abc.abstractmethod
    def move(self, action: Action):
        pass

    @property
    def state(self) -> Tuple[int, int, int]:
        x, y = self.position.astype(int)
        return x, y, self.orientation.value

    def set_position(self, x: Union[float, np.ndarray], y: Optional[float] = None) -> None:
        if isinstance(x, np.ndarray):
            self.position = x
        else:
            self.position = np.array([x, y])
