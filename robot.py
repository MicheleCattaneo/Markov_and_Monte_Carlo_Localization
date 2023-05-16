from enum import Enum

import numpy as np
import shapely
from shapely import LineString as ShapelyLine, affinity
from shapes import DisplayableIntersection, DisplayableLine, DisplayableRectangle

from definitions import *


class Robot:
    class Direction(Enum):
        '''
        Mapping between a direction and an index
        '''
        UP = 0
        UP_RIGHT = 1
        RIGHT = 2
        DOWN_RIGHT = 3
        DOWN = 4
        DOWN_LEFT = 5
        LEFT = 6
        UP_LEFT = 7

    # mapping between an index (from Direction) and a direction array to be added
    # to the current position in order to perform a movement
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

    def __init__(self, world, x, y, batch, sensor_length=100) -> None:

        self.location = np.array([x, y])
        self.sensor_length = sensor_length
        self.direction = 0  # look up by default
        self.mass_center = shapely.Point((x + TILE_SIZE / 2, y + TILE_SIZE / 2))

        # region GUI

        self.laser_color = (124, 252, 0)
        self.color = (255, 18, 18)
        self.batch = batch
        self.sensor = DisplayableLine(x=x + TILE_SIZE / 2, y=y + TILE_SIZE / 2, x2=x + TILE_SIZE / 2, y2=y + TILE_SIZE / 2 + sensor_length, color=self.laser_color,
                                      batch=batch)
        self.body = DisplayableRectangle(x, y, TILE_SIZE, TILE_SIZE, color=(255, 18, 18), batch=batch)
        self.body.opacity = 200
        self.closest_sensed_obj = None

        # endregion

        self.world = world
        self.collision_dict = world.collision_dict
        self.true_measurements = self.precompute_measurements(world.height, world.width, world.tile_size)

        self.believe = np.ones_like(self.true_measurements)
        self.believe[~self.world.walkable] = 0
        self.believe /= self.believe.sum()

        print()

    # region Markov

    def precompute_measurements(self, height: int, width: int, tile_size: int):
        means = np.zeros((height, width, 8))

        for i in range(means.shape[0]):
            for j in range(means.shape[1]):
                x, y = i * tile_size, j * tile_size
                for d in range(means.shape[2]):
                    if (i, j) in self.world.collision_dict:
                        means[i, j, d] = np.inf
                    self.sensor = self.get_sensor_given_xy(x, y, list(Robot.Direction)[d])

                    sensor_intersection = self.get_intersection(self.world)

                    means[i, j, d] = sensor_intersection.distance(shapely.Point(x, y)) if sensor_intersection else np.inf

        return means

    def see(self):
        pass

    def act(self, direction: Direction):
        direction = self.directions[direction.value]


    # endregion

    # region GUI

    def remove_gui(self):
        self.sensor.delete()
        self.body.delete()

    # endregion

    # region Move and Sense

    def set_mass_center(self):
        self.mass_center = shapely.Point((self.location[0] + TILE_SIZE / 2, self.location[1] + TILE_SIZE / 2))

    def get_intersection(self, world):

        closest_dist = float('inf')
        closest_obj = None

        for object in world.objects:
            intersection = object.shapely_shape.exterior.intersection(self.sensor.shapely_shape)
            if not intersection.is_empty:
                if intersection.geom_type == "LineString":
                    intersection = intersection.boundary
                if intersection.geom_type == 'Point':
                    # if intersection is a point, use envelope
                    d = intersection.envelope.distance(self.mass_center)
                    if d < closest_dist:
                        closest_dist = d
                        closest_obj = intersection.envelope
                else:
                    # if intersection is a multipoint, iterate through the points
                    for point in intersection.geoms:
                        d = point.distance(self.mass_center)
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
                                                              TILE_SIZE, 3, TILE_SIZE, color=(255, 255, 0), batch=self.batch)
        return closest_obj

    def print_sensor_loc(self):
        print("Sensor loc: ", self.sensor.shapely_shape.coords.xy)

    def get_sensor(self, direction: Direction):
        x = self.location[0]
        y = self.location[1]
        return self.get_sensor_given_xy(x, y, direction)

    def get_sensor_given_xy(self, x, y, direction: Direction):
        line = ShapelyLine(
            [[x + TILE_SIZE / 2, y + TILE_SIZE / 2], [x + TILE_SIZE / 2, y + TILE_SIZE / 2 + self.sensor_length]])
        angle = Robot.rotations[direction.value]
        # get rotated sensor
        line = affinity.rotate(line, angle, origin=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))

        x2 = line.coords.xy[0][1]
        y2 = line.coords.xy[1][1]
        # print(line.coords.xy)
        return DisplayableLine(x + TILE_SIZE / 2, y + TILE_SIZE / 2, x2, y2, color=self.laser_color, batch=self.batch)

    def get_ij_from_xy(self, xy: tuple):
        return xy[0] // TILE_SIZE, xy[1] // TILE_SIZE

    def deterministic_move(self, direction: Direction):
        new_location = self.location + Robot.directions[direction.value] * TILE_SIZE

        # get i,j coordinates and check whether that tile is occupied by an object (obstacle)
        if self.get_ij_from_xy(new_location) in self.collision_dict:
            print("Would hit the wall, can't do this move.")
            return 
        self.location = new_location
        self.body.delete()
        self.body = DisplayableRectangle(self.location[0], self.location[1], TILE_SIZE, TILE_SIZE, color=self.color, batch=self.batch)
        self.body.opacity = 128
        self.sensor.delete()
        self.sensor = self.get_sensor(direction)
        self.set_mass_center()

        print(f'New position: {self.location + Robot.directions[direction.value] * TILE_SIZE}')

    # endregion
