from __future__ import annotations
from typing import TYPE_CHECKING

from definitions import ROBOT_SIZE, TILE_SIZE

if TYPE_CHECKING:
    from base.localization import LocalizationBase
    from base.sensor import SensorBase


import abc
from enum import Enum
from typing import Optional, Union, Tuple

import numpy as np

from base.observer_pattern import Subject


class RobotBase(abc.ABC):
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

    localization: LocalizationBase

    sensor: SensorBase

    on_move: Subject = Subject()

    @abc.abstractmethod
    def move(self, action: Action, dt: float):
        pass

    @property
    def state(self) -> Tuple[int, int, int]:
        x, y = self.position.astype(int)
        return x, y, self.orientation.value

    def set_position(self, x: Union[float, np.ndarray], y: Optional[float] = None) -> None:
        """Sets the new position of the robot. Notifies the on_move subscription and
        makes the sensor sense, to get the new sensor intersection.
        """        

        if isinstance(x, np.ndarray):
            self.position = x
        else:
            self.position = np.array([x, y], dtype='float32')

    def teleport(self, x: float, y: float) -> None:
        """Teleports the robot to a new position.
        Calls robot.set_position()

        Args:
            x (float): x pixel coordinates
            y (float): y pixel coordinates
        """
        self.set_position(x // TILE_SIZE, y // TILE_SIZE)
        self.sensor.sense(self.position + ROBOT_SIZE, self.orientation)
        self.on_move.notify()
