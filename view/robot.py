import pyglet.graphics
from pyglet import image, sprite

from definitions import *
from base.observer_pattern import Observer
from base.robot import RobotBase

import numpy as np


class RobotView(Observer):

    def __init__(self, robot: RobotBase, batch: pyglet.graphics.Batch):
        self.robot = robot
        self.batch = batch

        self.color = (255, 18, 18)
        self.sprite = None

        self.sprite_texture = image.load('./textures/robot.png').get_texture()
        self.sprite_texture.anchor_x = self.sprite_texture.width // 2
        self.sprite_texture.anchor_y = self.sprite_texture.height // 2

        self.display_position = self.robot.position.copy().astype(float)
        self.moving = False
        self.allow_move = True
        self.dt = SPEED / FPS
        self.dt = min(self.dt, 1.)

        self.robot.on_move.subscribe(self)
        self.update()


    def update_moving(self):
        if self.moving:
            self.allow_move = False
        elif self.allow_move:
            self.moving = True
        else:
            self.allow_move = True

    def update(self) -> None:
        if self.moving:
            remaining_distance = np.linalg.norm(self.robot.position - self.display_position)
        
            if self.robot.current_action == RobotBase.Action.BACKWARD:
                movement = -self.dt * self.robot.directions[self.robot.orientation.value]
            else:
                movement = self.dt * self.robot.directions[self.robot.orientation.value]

            if np.linalg.norm(movement) > remaining_distance:
                self.display_position = self.robot.position
                self.moving = False
            else:
                self.display_position += movement

            if np.allclose(self.display_position, self.robot.position, atol=0.01):
                self.display_position = self.robot.position
                self.moving = False
        else:
            if not np.array_equal(self.display_position, self.robot.position):
                self.moving = True

        x, y = self.display_position * TILE_SIZE + TILE_SIZE // 2
        self.draw_robot(x, y, self.robot.orientation)

    def draw_robot(self, x: float, y: float, direction: RobotBase.Direction) -> None:
        if self.sprite is not None:
            self.sprite.delete()

        self.sprite = sprite.Sprite(self.sprite_texture, x=x, y=y, batch=self.batch)

        self.sprite.scale = .2 * SCALE

        self.sprite.rotation = direction.value * 45
