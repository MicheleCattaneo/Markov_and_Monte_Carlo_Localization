from enum import Enum

import numpy as np
import shapely
from shapely import LineString as ShapelyLine, affinity
from base.shapes import DisplayableIntersection, DisplayableLine, DisplayableRectangle

from definitions import *
from base.robot import RobotBase


class Robot(RobotBase):

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
        self.set_position(x, y)
        self.sensor_length = sensor_length
        self.mass_center = shapely.Point((x + ROBOT_SIZE / 2, y + ROBOT_SIZE / 2))

        # region Sensor

        self.batch = batch
        self.laser_color = (124, 252, 0)
        self.sensor = DisplayableLine(x=x + ROBOT_SIZE / 2, y=y + ROBOT_SIZE / 2, x2=x + ROBOT_SIZE / 2, y2=y + ROBOT_SIZE / 2 + sensor_length, color=self.laser_color,
                                      batch=batch)

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

    def act(self, direction: RobotBase.Direction):
        direction = self.directions[direction.value]

    # endregion

    # region Sensor

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
                                                              ROBOT_SIZE, 3, ROBOT_SIZE, color=(255, 255, 0), batch=self.batch)
        return closest_obj

    def print_sensor_loc(self):
        print("Sensor loc: ", self.sensor.shapely_shape.coords.xy)

    def get_sensor(self, direction: RobotBase.Direction):
        x, y = self.position * ROBOT_SIZE
        return self.get_sensor_given_xy(x, y, direction)

    def get_sensor_given_xy(self, x, y, direction: RobotBase.Direction):
        line = ShapelyLine(
            [[x + ROBOT_SIZE / 2, y + ROBOT_SIZE / 2], [x + ROBOT_SIZE / 2, y + ROBOT_SIZE / 2 + self.sensor_length]])
        angle = Robot.rotations[direction.value]
        # get rotated sensor
        line = affinity.rotate(line, angle, origin=(x + ROBOT_SIZE / 2, y + ROBOT_SIZE / 2))

        x2 = line.coords.xy[0][1]
        y2 = line.coords.xy[1][1]
        return DisplayableLine(x + ROBOT_SIZE / 2, y + ROBOT_SIZE / 2, x2, y2, color=self.laser_color, batch=self.batch)

    # endregion

    # region Move

    def set_mass_center(self):
        self.mass_center = shapely.Point((self.position[0]*ROBOT_SIZE + ROBOT_SIZE / 2, self.position[1]*ROBOT_SIZE + ROBOT_SIZE / 2))

    def move(self, action: RobotBase.Action):
        if action == action.TURN_LEFT:
            self.orientation = self.Direction((self.orientation.value - 1) % len(self.Direction))
        elif action == action.TURN_RIGHT:
            self.orientation = self.Direction((self.orientation.value + 1) % len(self.Direction))
        else:
            move_dir = self.orientation.value \
                if action == action.FORWARD \
                else (self.orientation.value + 4) % len(self.Direction)

            new_pos = self.position + Robot.directions[move_dir]

            # get i,j coordinates and check whether that tile is occupied by an object (obstacle)
            if not self.world.walkable[tuple(new_pos.astype(int))]:
                print("Would hit the wall, can't do this move.")
                return

            self.set_position(new_pos)
            print(f'New position: {self.position * TILE_SIZE}')

        # region Sensor

        self.sensor.delete()
        self.sensor = self.get_sensor(self.orientation)
        self.set_mass_center()

        # endregion

        self.on_move.notify()

    # endregion
