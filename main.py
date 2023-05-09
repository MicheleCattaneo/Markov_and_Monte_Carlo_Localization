import numpy as np
from pyglet import app

from shapely import affinity

from shapes import DisplayableRectangle
from definitions import *


def update(dt):
    print(f'Dt={dt}')
    r = np.random.random()

    if r > 0.5:
        robot.deterministic_move(Robot.Direction.DOWN_LEFT)
    else:
        robot.deterministic_move(Robot.Direction.DOWN_RIGHT)
    # robot.print_sensor_loc()
    robot.get_intersection(world)


if __name__ == '__main__':
    rec1 = DisplayableRectangle(300, 250, 100, 200, color=(255, 20, 147), batch=batch)
    # rec1.opacity = 128
    print(rec1)
    world.add(rec1)

    rec2 = DisplayableRectangle(500, 250, 200, 100, color=(255, 20, 147), batch=batch)
    # rec2.opacity = 128
    world.add(rec2)

    rec2 = DisplayableRectangle(100, 350, 200, 100, color=(255, 20, 147), batch=batch)
    # rec2.opacity = 128
    world.add(rec2)

    print(robot.sensor.shapely_shape.coords.xy)
    print(affinity.rotate(robot.sensor.shapely_shape, 90, origin=(robot.sensor.x, robot.sensor.y)))


    @window.event
    def on_draw():
        window.clear()
        batch.draw()


    pyglet.clock.schedule_interval(update, 1.0)
    app.run()
