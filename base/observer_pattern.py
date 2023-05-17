"""
Base code was taken from https://refactoring.guru/design-patterns/observer/python/example
Some adaptions were made to fit our purposes.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self) -> None:
        """
        Receive update from subject.
        """
        pass


class Subject:
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """
    _observers: List[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        """
        Subscribe an observer to the subject.
        """
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """
        Unsubscribe an observer from the subject.
        """
        self._observers.remove(observer)

    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        for observer in self._observers:
            observer.update()
