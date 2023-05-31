import numpy as np
from scipy.signal import convolve2d

from base.localization import LocalizationBase
from base.movement_models import InvalidActionException, MovementModelBase
from base.robot import RobotBase
from base.sensor import SensorBase
from definitions import ROBOT_SIZE, TILE_SIZE
from model.continuous_world import ContinuousWorld

class Particle:
    def __init__(self, x, y, orientation, weight=1.0):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.weight = weight

class MonteCarloLocalization(LocalizationBase):
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

    def __init__(self, world: ContinuousWorld, sensor: SensorBase, num_particles=10) -> None:
        self.world = world
        self.sensor = sensor
        self.particles = [Particle(np.random.uniform(0, world.width), np.random.uniform(0, world.height), RobotBase.Direction(np.random.choice(range(0,8)))) for _ in range(num_particles)]

    def measurement_probability(self, measurement: float) -> np.ndarray:
        """
        Given a measurement, returns the probability
        of being at a position and measuring the given measurement.
        """
        return np.isclose(self.true_measurements, measurement).astype('int')

    def act(self, action: RobotBase.Action) -> None:
        for particle in self.particles:
            if action == RobotBase.Action.FORWARD:
                particle.x += MonteCarloLocalization.directions[particle.orientation.value][0]
                particle.y += MonteCarloLocalization.directions[particle.orientation.value][1]
            elif action == RobotBase.Action.TURN_LEFT:
                particle.orientation = RobotBase.Direction((particle.orientation.value - 1) % len(RobotBase.Direction))
            elif action == RobotBase.Action.TURN_RIGHT:
                particle.orientation = RobotBase.Direction((particle.orientation.value + 1) % len(RobotBase.Direction))

    def see(self, measurement: float) -> None:
        for particle in self.particles:
            # compute the expected measurement for this particle
            true_measurement = self.sensor.true_reading(np.array([particle.x // TILE_SIZE, particle.y // TILE_SIZE]), particle.orientation)

            # update the particle's weight based on the likelihood of the observation
            particle.weight *= self.sensor.likelihood(true_measurement, measurement)

        total_weight = np.sum([particle.weight for particle in self.particles])
        print("-------------")
        for particle in self.particles:
            particle.weight /= total_weight
            print(particle.weight)

        print(np.sum([particle.weight for particle in self.particles]))

        # resample the particles based on their weights
        sampled_particles = np.random.choice(self.particles, size=len(self.particles), replace=True, p=[particle.weight for particle in self.particles])

        # Create new particles with the states of sampled particles, but reset weights
        self.particles = [Particle(particle.x, particle.y, particle.orientation, weight=1.0/len(self.particles)) for particle in sampled_particles]
