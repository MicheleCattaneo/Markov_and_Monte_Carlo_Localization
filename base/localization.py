from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.robot import RobotBase

import abc


class LocalizationBase(abc.ABC):
    @abc.abstractmethod
    def see(self, measurement: float) -> None:
        pass

    @abc.abstractmethod
    def act(self, action: RobotBase.Action) -> None:
        pass
