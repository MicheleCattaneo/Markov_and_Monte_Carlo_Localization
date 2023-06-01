import pyglet.graphics
from pyglet import shapes

from base.observer_pattern import Observer
from definitions import PARTICLE_SIZE
from model.localization import MonteCarloLocalization
from model.robots.continuous_robot import ContinuousRobot


class ParticleView(Observer):
    def __init__(self, localization: MonteCarloLocalization, robot: ContinuousRobot,
                 batch: pyglet.graphics.Batch) -> None:
        self.localization = localization
        self.robot = robot
        self.robot.on_move.subscribe(self)
        self.particle_shapes = []
        self.batch = batch

        self.update()

    def update(self) -> None:
        self.draw_particles()

    def draw_particles(self):
        self.particle_shapes.clear()

        for particle in self.localization.particles:
            color = (0, 0, 255)
            particle_shape = shapes.Circle(particle.x, particle.y, PARTICLE_SIZE, color=color, batch=self.batch)
            particle_shape.opacity = int(particle.weight ** 0.1 * 255)
            self.particle_shapes.append(particle_shape)
