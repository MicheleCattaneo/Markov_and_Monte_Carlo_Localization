import pyglet.graphics
from pyglet import image, sprite

from definitions import *
from base.observer_pattern import Observer
from base.robot import RobotBase


class RobotView(Observer):

    def __init__(self, robot: RobotBase, batch: pyglet.graphics.Batch):
        self.robot = robot
        self.batch = batch

        self.color = (255, 18, 18)
        self.sprite = None

        self.sprite_texture = image.load('./textures/robot.png').get_texture()
        self.sprite_texture.anchor_x = self.sprite_texture.width // 2
        self.sprite_texture.anchor_y = self.sprite_texture.height // 2

        self.robot.on_move.subscribe(self)
        self.update()

    def update(self) -> None:
        x, y = self.robot.position * TILE_SIZE + TILE_SIZE // 2

        self.draw_robot(x, y, self.robot.orientation)

    def draw_robot(self, x: float, y: float, direction: RobotBase.Direction) -> None:
        if self.sprite is not None:
            self.sprite.delete()

        self.sprite = sprite.Sprite(self.sprite_texture, x=x, y=y, batch=self.batch)

        self.sprite.scale = .2 * SCALE

        self.sprite.rotation = direction.value * 45
