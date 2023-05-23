from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.robot import RobotBase

import abc

import numpy as np


class LocalizationBase(abc.ABC):
    belief: np.ndarray

    @abc.abstractmethod
    def measurement_probability(self, measurement: float) -> np.ndarray:
        pass

    @abc.abstractmethod
    def see(self, measurement: float) -> None:
        pass

    @abc.abstractmethod
    def act(self, action: RobotBase.Action) -> None:
        pass
