import numpy as np
from scipy.stats import norm

from definitions import MEASUREMENT_SIGMA
from model.localization.markov_localization import MarkovLocalization


class UncertainMarkovLocalization(MarkovLocalization):

    def measurement_probability(self, measurement: float) -> np.ndarray:
        # create nd-array of gaussians, centered at the true measurement.
        gaussians = np.random.normal(self.true_measurements, MEASUREMENT_SIGMA, size=self.true_measurements.shape)

        # Sample the measurement from the PDFs
        return norm.pdf(measurement, gaussians)
