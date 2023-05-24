import numpy as np
from scipy.stats import norm

from definitions import MEASUREMENT_SIGMA
from model.localization.markov_localization import MarkovLocalization


class UncertainMarkovLocalization(MarkovLocalization):

    def measurement_probability(self, measurement: float) -> np.ndarray:
        # create nd-array of gaussians, centered at the true measurement.
        # Sample the measurement from the PDFs
        return norm.pdf(measurement, self.true_measurements, MEASUREMENT_SIGMA)
