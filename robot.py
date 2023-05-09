from enum import Enum

import numpy as np
import shapely
from shapely import LineString as ShapelyLine, affinity
from shapes import DisplayableIntersection, DisplayableLine, DisplayableRectangle

from definitions import *\

import math as m


class Robot:
    class Direction(Enum):
        '''
        Mapping between a direction and an index
        '''
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3
        UP_LEFT = 4
        UP_RIGHT = 5
        DOWN_LEFT = 6
        DOWN_RIGHT = 7

    # mapping between an index (from Direction) and a direction array to be added
    # to the current position in order to perform a movement
    directions = [
        np.array([0, 1]),
        np.array([0, -1]),
        np.array([-1, 0]),
        np.array([1, 0]),
        np.array([-1, 1]),
        np.array([1, 1]),
        np.array([-1, -1]),
        np.array([1, -1])
    ]

    rotations = [
        0,
        180,
        90,
        -90,
        45,
        -45,
        135,
        -135
    ]

    def __init__(self, x, y, batch, sensor_length=100) -> None:
        self.location = np.array([x, y])
        self.sensor_length = sensor_length
        self.laser_color = (124, 252, 0)
        self.color = (255, 18, 18)
        self.batch = batch
        self.direction = 0  # look up by default
        self.sensor = DisplayableLine(x=x + TILE_SIZE / 2, y=y + TILE_SIZE / 2, x2=x + TILE_SIZE / 2, y2=y + TILE_SIZE / 2 + sensor_length, color=self.laser_color,
                                      batch=batch)
        self.body = DisplayableRectangle(x, y, TILE_SIZE, TILE_SIZE, color=(255, 18, 18), batch=batch)
        self.body.opacity = 200
        self.closest_sensed_obj = None
        self.mass_center = shapely.Point((x + TILE_SIZE / 2, y + TILE_SIZE / 2))

    def set_collision_dic(self, dic):
        self.collision_dic = dic

    def get_intersection(self, world):

        closest_dist = float('inf')
        closest_obj = None

        for object in world.objects:
            intersection = object.shapely_shape.exterior.intersection(self.sensor.shapely_shape)
            if not intersection.is_empty:
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

    def print_sensor_loc(self):
        print("Sensor loc: ", self.sensor.shapely_shape.coords.xy)

    def get_sensor(self, direction: Direction):
        x = self.location[0]
        y = self.location[1]

        line = ShapelyLine([[x + TILE_SIZE / 2, y + TILE_SIZE / 2], [x + TILE_SIZE / 2, y + TILE_SIZE / 2 + self.sensor_length]])
        angle = Robot.rotations[direction.value]
        # get rotated sensor
        line = affinity.rotate(line, angle, origin=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))

        x2 = line.coords.xy[0][1]
        y2 = line.coords.xy[1][1]
        # print(line.coords.xy)
        return DisplayableLine(x + TILE_SIZE / 2, y + TILE_SIZE / 2, x2, y2, color=self.laser_color, batch=self.batch)

    def get_ij_from_xy(self, xy: tuple):
        return (m.floor(xy[0]/TILE_SIZE), m.floor(xy[1]/TILE_SIZE) )

    def deterministic_move(self, direction: Direction):
        new_location = self.location + Robot.directions[direction.value] * TILE_SIZE

        # get i,j coordinates and check whether that tile is occupied by an object (obstacle)
        if self.get_ij_from_xy(new_location) in self.collision_dic:
            print("Would hit the wall, can't do this move.")
            return 
        self.location = new_location
        self.body.delete()
        self.body = DisplayableRectangle(self.location[0], self.location[1], TILE_SIZE, TILE_SIZE, color=self.color, batch=self.batch)
        self.body.opacity = 128
        self.sensor.delete()
        self.sensor = self.get_sensor(direction)

        print(f'New position: {self.location + Robot.directions[direction.value] * TILE_SIZE}')

