import numpy as np
from scipy.signal import convolve2d

from base.localization import LocalizationBase
from base.movement_models import InvalidActionException, MovementModelBase
from base.robot import RobotBase
from base.sensor import SensorBase
from definitions import *
from model.continuous_world import ContinuousWorld

class Particle:
    def __init__(self, x, y, orientation, weight=1.0):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.weight = weight


    def move(self, action: RobotBase.Action, world: ContinuousWorld):
        #if action == RobotBase.Action.FORWARD:
        #    self.x += MonteCarloLocalization.directions[self.orientation.value][0] * SPEED
        #    self.y += MonteCarloLocalization.directions[self.orientation.value][1] * SPEED
        #elif action == RobotBase.Action.TURN_LEFT:
        #    self.orientation = RobotBase.Direction((self.orientation.value - 1) % len(RobotBase.Direction))
        #elif action == RobotBase.Action.TURN_RIGHT:
        #    self.orientation = RobotBase.Direction((self.orientation.value + 1) % len(RobotBase.Direction))

        if action == action.TURN_LEFT:
            self.orientation = RobotBase.Direction((self.orientation.value - 1) % len(RobotBase.Direction))
        elif action == action.TURN_RIGHT:
            self.orientation = RobotBase.Direction((self.orientation.value + 1) % len(RobotBase.Direction))
        else:
            
            uncertainty_multiplier = 1.

            move_dir = self.orientation.value \
                if action == action.FORWARD \
                else (self.orientation.value + 4) % len(self.Direction)

            speed_mult = SPEED / FPS
            new_pos = np.array([self.x, self.y]) + uncertainty_multiplier * speed_mult * MonteCarloLocalization.directions[move_dir] * TILE_SIZE / np.linalg.norm(MonteCarloLocalization.directions[move_dir])

            new_center = (new_pos + ROBOT_SIZE)
            if not world.check_within_boundaries(new_center[0], new_center[1]) or world.is_occupied(new_center[0], new_center[1]):
                return
            self.x, self.y = new_pos

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
        self.particles = self.initialize_particles(num_particles)


    def initialize_particles(self, num_particles: int):
        particles = []
        for _ in range(num_particles):
            while True:
                x = np.random.uniform(0, self.world.width)
                y = np.random.uniform(0, self.world.height)
                if not self.world.is_occupied(x, y):
                    orientation = RobotBase.Direction(np.random.choice(range(0,8)))
                    particles.append(Particle(x, y, orientation))
                    break


        return particles


    def measurement_probability(self, measurement: float) -> np.ndarray:
        """
        Given a measurement, returns the probability
        of being at a position and measuring the given measurement.
        """
        return np.isclose(self.true_measurements, measurement).astype('int')


    def _resample(self):
        # create new particles with the states of sampled particles, but reset weights
        sampled_particles = np.random.choice(self.particles, size=NUM_PARTICLES, replace=True, p=[particle.weight for particle in self.particles])
        self.particles = []
        for particle in sampled_particles:
            sd = np.sqrt(1 / particle.weight)
            noise_x = np.random.normal(0, sd*PARTICLE_NOISE)
            noise_y = np.random.normal(0, sd*PARTICLE_NOISE)
            new_x = particle.x + noise_x
            new_y = particle.y + noise_y

            if not self.world.check_within_boundaries(new_x, new_y) or self.world.is_occupied(new_x, new_y):
                new_x, new_y = particle.x, particle.y

            stay_prob = np.sqrt(1 - particle.weight)
            shift_prob = (1 - stay_prob) / 2
            orientation_noise = np.random.choice([-1, 0, 1], p=[shift_prob, stay_prob, shift_prob])
            new_orientation = RobotBase.Direction((particle.orientation.value + orientation_noise) % len(RobotBase.Direction))
        
            self.particles.append(Particle(new_x, new_y, new_orientation, weight=1.0/NUM_PARTICLES))


    def act(self, action: RobotBase.Action) -> None:
        for particle in self.particles:
            particle.move(action, self.world)


    def see(self, measurement: float) -> None:
        for particle in self.particles:
            # compute the expected measurement for this particle
            true_measurement = self.sensor.true_reading(np.array([particle.x // TILE_SIZE, particle.y // TILE_SIZE]), particle.orientation)

            # update the particle's weight based on the likelihood of the observation
            particle.weight *= self.sensor.likelihood(true_measurement, measurement)

        total_weight = np.sum([particle.weight for particle in self.particles])
        for particle in self.particles:
            particle.weight /= total_weight

        # resample the particles based on their weights
        self._resample()
