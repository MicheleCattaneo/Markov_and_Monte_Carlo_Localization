import pyglet.graphics

from definitions import *
from base.observer_pattern import Observer
from base.robot import RobotBase
from base.shapes import DisplayableRectangle
from base.shapes import DisplayableRobot


class RobotView(Observer):

    def __init__(self, robot: RobotBase, batch: pyglet.graphics.Batch):
        self.robot = robot
        self.batch = batch

        self.color = (255, 18, 18)
        self.body = None

        self.robot.on_move.subscribe(self)
        self.update()

    def update(self) -> None:
        x, y = self.robot.position * TILE_SIZE
        if self.body:
            self.body.delete()

        self.body = DisplayableRobot(x, y, TILE_SIZE // 2, batch=self.batch)
        self.body.set_rotation(self.robot.orientation)
