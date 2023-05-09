TILE_SIZE = 10

import pyglet
from pyglet.window import Window

from environment import GridWorld
from robot import Robot


window = Window(width=720, height=720)
batch = pyglet.graphics.Batch()

robot = Robot(500, 500, batch, sensor_length=200)

world = GridWorld(720, TILE_SIZE)

dd = True
