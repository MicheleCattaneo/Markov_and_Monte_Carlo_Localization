from typing import Tuple, Optional

import numpy as np
import shapely
from shapely import LineString as ShapelyLine, affinity


from base.robot import RobotBase
from base.sensor import SensorBase
from definitions import TILE_SIZE, ROBOT_SIZE


class LaserSensor(SensorBase):
    """Represents a laser sensor with certain measurements.
    """    
    rotations = [
        0,
        -45,
        -90,
        -135,
        180,
        135,
        90,
        45
    ]

    def __init__(self, world, sensor_length: float):
        self.world = world
        self.sensor_length = sensor_length

        self.intersection: Optional[Tuple[float, float]] = None

    def likelihood(self, true_measurements, measurement):
        return np.isclose(true_measurements, measurement).astype('float')

    def sense(self, xy: np.ndarray, direction: RobotBase.Direction) -> np.ndarray:
        gx, gy = xy * TILE_SIZE

        mass_center = shapely.Point((gx, gy))
        laser_beam_obj = self.create_laser_beam_object(gx, gy, direction)

        closest_dist = np.inf
        closest_obj = None

        for object in self.world.objects:
            if object.shapely_shape.geom_type == "LineString":
                intersection = object.shapely_shape.intersection(laser_beam_obj)
            else:
                intersection = object.shapely_shape.exterior.intersection(laser_beam_obj)
            if not intersection.is_empty:
                if intersection.geom_type == "LineString":
                    intersection = intersection.boundary
                if intersection.geom_type == 'Point':
                    # if intersection is a point, use envelope
                    d = intersection.envelope.distance(mass_center)
                    if d < closest_dist:
                        closest_dist = d
                        closest_obj = intersection.envelope
                else:
                    # if intersection is a multipoint, iterate through the points
                    for point in intersection.geoms:
                        d = point.distance(mass_center)
                        if d < closest_dist:
                            closest_dist = d
                            closest_obj = point

        self.intersection = (closest_obj.x, closest_obj.y) if closest_obj is not None else None

        # default measurement can not be 'inf' because it creates issues when modelling
        # measurement probabilities with an infinite mean:
        # E.g: if p(i|l) ~ Norm(inf, 1), when sampling 'inf' from the pdf generates NaNs.
        return closest_dist if closest_dist != float('inf') else -1
    
    def create_laser_beam_object(self, x, y, direction: RobotBase.Direction):
        line = ShapelyLine(
            [[x, y], [x, y + self.sensor_length]])
        angle = self.rotations[direction.value]
        # get rotated sensor
        line = affinity.rotate(line, angle, origin=(x, y))

        x2 = line.coords.xy[0][1]
        y2 = line.coords.xy[1][1]
        return ShapelyLine([[x, y], [x2, y2]])

