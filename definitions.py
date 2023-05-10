TILE_SIZE = 10

import pyglet
from pyglet.window import Window

from environment import GridWorld
from robot import Robot
from pyglet.window import key

key_to_direction_mapping = {
    key.LEFT : 2,
    key.RIGHT : 3,
    key.UP : 0,
    key.DOWN : 1
}



window = Window(width=720, height=720)
batch = pyglet.graphics.Batch()

keys = key.KeyStateHandler()
window.push_handlers(keys)

robot = Robot(500, 500, batch, sensor_length=200)

world = GridWorld(720, TILE_SIZE)

dd = True
