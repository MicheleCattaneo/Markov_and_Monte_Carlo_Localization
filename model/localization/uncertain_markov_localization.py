import numpy as np
from scipy.stats import norm

from definitions import MEASUREMENT_SIGMA
from model.localization.markov_localization import MarkovLocalization


class UncertainMarkovLocalization(MarkovLocalization):
    """Represents the logic of an uncertain Markov Localization.
        The probability of a measurement i given a pose l is defined as follows:
        p(i|l) ~ Norm(true_i, sigma)
    """

    def measurement_probability(self, measurement: float) -> np.ndarray:
        # create nd-array of gaussians, centered at the true measurement.
        # Sample the measurement from the PDFs
        return norm.pdf(measurement, self.true_measurements, MEASUREMENT_SIGMA)
