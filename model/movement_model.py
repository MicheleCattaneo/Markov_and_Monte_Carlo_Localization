import numpy as np

from base.movement_models import MovementModelBase


class DiscreteMovementModel(MovementModelBase):

    def _get_convolution_forward(self):
        filter = np.zeros((3, 3, 8))
        o = 6
        filter[0, 1, (0 + o) % 8] = 1
        filter[0, 2, (1 + o) % 8] = 1
        filter[1, 2, (2 + o) % 8] = 1
        filter[2, 2, (3 + o) % 8] = 1
        filter[2, 1, (4 + o) % 8] = 1
        filter[2, 0, (5 + o) % 8] = 1
        filter[1, 0, (6 + o) % 8] = 1
        filter[0, 0, (7 + o) % 8] = 1

        return filter

    def _get_convolution_backward(self):
        filter = np.zeros((3, 3, 8))
        o = 6
        filter[2, 1, (0 + o) % 8] = 1
        filter[2, 0, (1 + o) % 8] = 1
        filter[1, 0, (2 + o) % 8] = 1
        filter[0, 0, (3 + o) % 8] = 1
        filter[0, 1, (4 + o) % 8] = 1
        filter[0, 2, (5 + o) % 8] = 1
        filter[1, 2, (6 + o) % 8] = 1
        filter[2, 2, (7 + o) % 8] = 1

        return filter


class UncertainMovementModel(MovementModelBase):
    """Represents an uncertain movement model modelled by probabilities [p1,p2,p3]
    where p1 is the probability of executing the actual issued command, 
    p2 is the probability of not executing any command
    and p3 is the probability of issuing the opposite command.
    The sum p1 + p2 + p3 must be equal to 1.
    """

    def __init__(self, probs: np.ndarray = None) -> None:
        """Initializes an uncertain movement model.

        Args:
            probs (np.ndarray, optional): a 3-d array containing the probabilities p1,p2 and p3 of executing the issued
            command, the probability of executing no command and the probability of executing the opposite command.
            When not defined, default values of [.8,.1,.1] are used.
        """
        if probs is not None:
            self.probs = probs
        else:
            self.probs = np.array([.8, .1, .1])
        assert np.isclose(self.probs.sum(), 1.)

    def _get_convolution_forward(self):
        filter = np.zeros((3, 3, 8))
        o = 6
        # prob. of going forward
        filter[0, 1, (0 + o) % 8] = self.probs[0]
        filter[0, 2, (1 + o) % 8] = self.probs[0]
        filter[1, 2, (2 + o) % 8] = self.probs[0]
        filter[2, 2, (3 + o) % 8] = self.probs[0]
        filter[2, 1, (4 + o) % 8] = self.probs[0]
        filter[2, 0, (5 + o) % 8] = self.probs[0]
        filter[1, 0, (6 + o) % 8] = self.probs[0]
        filter[0, 0, (7 + o) % 8] = self.probs[0]
        # prob. of staying in place
        filter[1, 1, (0 + o) % 8] = self.probs[1]
        filter[1, 1, (1 + o) % 8] = self.probs[1]
        filter[1, 1, (2 + o) % 8] = self.probs[1]
        filter[1, 1, (3 + o) % 8] = self.probs[1]
        filter[1, 1, (4 + o) % 8] = self.probs[1]
        filter[1, 1, (5 + o) % 8] = self.probs[1]
        filter[1, 1, (6 + o) % 8] = self.probs[1]
        filter[1, 1, (7 + o) % 8] = self.probs[1]
        # prob. of going backwards
        filter[2, 1, (0 + o) % 8] = self.probs[2]
        filter[2, 0, (1 + o) % 8] = self.probs[2]
        filter[1, 0, (2 + o) % 8] = self.probs[2]
        filter[0, 0, (3 + o) % 8] = self.probs[2]
        filter[0, 1, (4 + o) % 8] = self.probs[2]
        filter[0, 2, (5 + o) % 8] = self.probs[2]
        filter[1, 2, (6 + o) % 8] = self.probs[2]
        filter[2, 2, (7 + o) % 8] = self.probs[2]

        return filter

    def _get_convolution_backward(self):
        filter = np.zeros((3, 3, 8))
        o = 6
        # prob. of going forward
        filter[0, 1, (0 + o) % 8] = self.probs[2]
        filter[0, 2, (1 + o) % 8] = self.probs[2]
        filter[1, 2, (2 + o) % 8] = self.probs[2]
        filter[2, 2, (3 + o) % 8] = self.probs[2]
        filter[2, 1, (4 + o) % 8] = self.probs[2]
        filter[2, 0, (5 + o) % 8] = self.probs[2]
        filter[1, 0, (6 + o) % 8] = self.probs[2]
        filter[0, 0, (7 + o) % 8] = self.probs[2]
        # prob. of staying in place
        filter[1, 1, (0 + o) % 8] = self.probs[1]
        filter[1, 1, (1 + o) % 8] = self.probs[1]
        filter[1, 1, (2 + o) % 8] = self.probs[1]
        filter[1, 1, (3 + o) % 8] = self.probs[1]
        filter[1, 1, (4 + o) % 8] = self.probs[1]
        filter[1, 1, (5 + o) % 8] = self.probs[1]
        filter[1, 1, (6 + o) % 8] = self.probs[1]
        filter[1, 1, (7 + o) % 8] = self.probs[1]
        # prob. of going backwards
        filter[2, 1, (0 + o) % 8] = self.probs[0]
        filter[2, 0, (1 + o) % 8] = self.probs[0]
        filter[1, 0, (2 + o) % 8] = self.probs[0]
        filter[0, 0, (3 + o) % 8] = self.probs[0]
        filter[0, 1, (4 + o) % 8] = self.probs[0]
        filter[0, 2, (5 + o) % 8] = self.probs[0]
        filter[1, 2, (6 + o) % 8] = self.probs[0]
        filter[2, 2, (7 + o) % 8] = self.probs[0]

        return filter
