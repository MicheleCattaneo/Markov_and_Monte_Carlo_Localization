import numpy as np
from pyglet import app

import sys

from shapely import affinity

from shapes import DisplayableRectangle
from definitions import *

COMMAND_TYPE = 'AUTO'

def update(dt):
    print(f'Dt={dt}')
    r = np.random.random()


    if COMMAND_TYPE == 'KEYBOARD':
        if keys[key.UP]:
            robot.deterministic_move(Robot.Direction.UP)
        elif keys[key.DOWN]:
            robot.deterministic_move(Robot.Direction.DOWN)
        elif keys[key.LEFT]:
            robot.deterministic_move(Robot.Direction.LEFT)
        elif keys[key.RIGHT]:
            robot.deterministic_move(Robot.Direction.RIGHT)
        robot.get_intersection(world)
    else:
        r = np.random.random()

        if r > 0.5:
            robot.deterministic_move(Robot.Direction.DOWN_LEFT)
        else:
            robot.deterministic_move(Robot.Direction.DOWN_RIGHT)

        robot.get_intersection(world)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg == 'keyboard':
            COMMAND_TYPE = 'KEYBOARD'

    rec1 = DisplayableRectangle(300, 250, 100, 200, color=(255, 20, 147), batch=batch)
    # rec1.opacity = 128
    print(rec1)
    world.add(rec1)

    rec2 = DisplayableRectangle(400, 250, 200, 100, color=(255, 20, 147), batch=batch)
    # rec2.opacity = 128
    world.add(rec2)

    rec3 = DisplayableRectangle(100, 350, 200, 100, color=(255, 20, 147), batch=batch)
    # rec2.opacity = 128
    world.add(rec3)

    rec4 = DisplayableRectangle(300, 500, 200, 100, color=(255, 20, 147), batch=batch)
    # rec2.opacity = 128
    world.add(rec4)

    # get dictionary of i,j indices that have objects
    # the robot avoids those to avoid collisions
    collisions_dic = world.get_collision_bounds_dictionary()
    robot.set_collision_dic(collisions_dic)

    print(robot.sensor.shapely_shape.coords.xy)
    print(affinity.rotate(robot.sensor.shapely_shape, 90, origin=(robot.sensor.x, robot.sensor.y)))


    @window.event
    def on_draw():
        window.clear()
        batch.draw()


    pyglet.clock.schedule_interval(update, 0.1)
    app.run()
