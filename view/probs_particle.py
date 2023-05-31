import pyglet.graphics

from pyglet import shapes

from base.observer_pattern import Observer
from model.continuous_world import ContinuousWorld
from model.localization import MonteCarloLocalization
from model.robot import ContinuousRobot
from definitions import PARTICLE_SIZE

class ParticleView(Observer):
    def __init__(self, localization: MonteCarloLocalization, robot: ContinuousRobot, batch: pyglet.graphics.Batch) -> None:
        self.localization = localization
        self.robot = robot
        self.robot.on_move.subscribe(self)
        self.particle_shapes = []
        self.batch = batch

    def update(self) -> None:
        self.draw_particles()

    def draw_particles(self):
        self.particle_shapes.clear()

        for particle in self.localization.particles:
            color = (255, 0, 0, 100)
            size = PARTICLE_SIZE #* particle.weight
            particle_shape = shapes.Circle(particle.x, particle.y, size, color=color, batch=self.batch)
            self.particle_shapes.append(particle_shape)
