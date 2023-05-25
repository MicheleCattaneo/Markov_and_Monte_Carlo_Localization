from typing import Optional

import numpy as np
import pyglet
from pyglet import shapes

from base.observer_pattern import Observer
from base.robot import RobotBase
from definitions import TILE_SIZE, ROBOT_SIZE
from model.sensors import LaserSensor


class LaserSensorView(Observer):
    """
    View for Laser Sensors. The laser is visualized with a line and the intersection with a star.
    """

    def __init__(self, robot: RobotBase, laser: LaserSensor, batch: pyglet.graphics.Batch):
        self.robot = robot
        self.laser = laser

        self.batch = batch
        self.laser_color = (124, 252, 0)
        self.intersection_color = (255, 255, 0)

        self.laser_beam_line: Optional[shapes.Line] = None
        self.intersection_star: Optional[shapes.Star] = None

        self.robot.on_move.subscribe(self)
        self.update()

    def update(self) -> None:
        self._draw_intersection()

        if self.laser_beam_line is not None:
            self.laser_beam_line.delete()

        end_xy = self.laser.intersection if self.laser.intersection is not None else self._get_endpoint()

        self.laser_beam_line = shapes.Line(
            *(self.robot.position + ROBOT_SIZE) * TILE_SIZE,
            *end_xy, width=1,
            color=self.laser_color, batch=self.batch
        )

    def _get_endpoint(self):
        rot_deg = -self.laser.rotations[self.robot.orientation.value]
        y_rot_direction = np.array([np.sin(np.deg2rad(rot_deg)), np.cos(np.deg2rad(rot_deg))])
        vec = y_rot_direction * self.laser.sensor_length

        return (self.robot.position + ROBOT_SIZE) * TILE_SIZE + vec

    def _draw_intersection(self):
        # remove old intersection
        if self.intersection_star is not None:
            self.intersection_star.delete()
            self.intersection_star = None

        # if there is no new intersection, return
        if self.laser.intersection is None:
            return

        # create star at intersection
        ix, iy = self.laser.intersection
        self.intersection_star = shapes.Star(
            ix, iy, outer_radius=TILE_SIZE / 2, inner_radius=TILE_SIZE / 10,
            num_spikes=10, color=self.intersection_color, batch=self.batch
        )

