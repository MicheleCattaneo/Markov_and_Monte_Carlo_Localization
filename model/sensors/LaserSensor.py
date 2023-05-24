import numpy as np
import pyglet.graphics
import shapely
from shapely import LineString as ShapelyLine, affinity


from base.robot import RobotBase
from base.sensor import SensorBase
from base.shapes import DisplayableLine, DisplayableIntersection
from definitions import TILE_SIZE


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

    def __init__(self, init_x: float, init_y: float, world, sensor_length: float, batch: pyglet.graphics.Batch):
        self.world = world
        self.sensor_length = sensor_length

        # region View

        self.batch = batch
        self.laser_color = (124, 252, 0)
        self.laser_beam_obj = DisplayableLine(x=init_x, y=init_y, x2=init_x, y2=init_y + sensor_length,
                                              color=self.laser_color, batch=batch)

        # endregion

        self.closest_sensed_obj = None

    def sense(self, xy: np.ndarray, direction: RobotBase.Direction) -> np.ndarray:
        self.laser_beam_obj.delete()
        gx, gy = xy * TILE_SIZE

        mass_center = shapely.Point((gx, gy))
        self.laser_beam_obj = self.create_laser_beam_object(gx, gy, direction)

        closest_dist = np.inf
        closest_obj = None

        for object in self.world.objects:
            if object.shapely_shape.geom_type == "LineString":
                intersection = object.shapely_shape.intersection(self.laser_beam_obj.shapely_shape)
            else:
                intersection = object.shapely_shape.exterior.intersection(self.laser_beam_obj.shapely_shape)
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

        if self.closest_sensed_obj is not None:
            # delete old DisplayableIntersection
            self.closest_sensed_obj.delete()
            self.closest_sensed_obj = None
        if closest_obj:
            # Add new DisplayableIntersection
            self.closest_sensed_obj = DisplayableIntersection(closest_obj.x, closest_obj.y,
                                                              TILE_SIZE/2, TILE_SIZE/10, 10, color=(255, 255, 0), batch=self.batch)
            
        # default measurement can not be 'inf' because it creates issues when modelling
        # measurement probabilities with an infinite mean:
        # E.g: if p(i|l) ~ Norm(inf, 1), when sampling 'inf' from the pdf generates NaNs.
        return closest_dist if closest_dist != float('inf') else -1
    
    def print_sensor_loc(self):
        print("Sensor loc: ", self.laser_beam_obj.shapely_shape.coords.xy)

    def create_laser_beam_object(self, x, y, direction: RobotBase.Direction):
        line = ShapelyLine(
            [[x, y], [x, y + self.sensor_length]])
        angle = self.rotations[direction.value]
        # get rotated sensor
        line = affinity.rotate(line, angle, origin=(x, y))

        x2 = line.coords.xy[0][1]
        y2 = line.coords.xy[1][1]
        return DisplayableLine(x, y, x2, y2, color=self.laser_color, batch=self.batch)

