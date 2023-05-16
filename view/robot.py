import pyglet.graphics

from definitions import *
from base.observer_pattern import Observer
from base.robot import RobotBase
from base.shapes import DisplayableRectangle


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

        self.body = DisplayableRectangle(
            x, y, TILE_SIZE, TILE_SIZE,
            color=self.color, batch=self.batch)
        self.body.opacity = 128

