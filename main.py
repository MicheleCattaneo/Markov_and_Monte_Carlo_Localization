import numpy as np
import shapely
import pyglet
from pyglet import app
from pyglet.window import Window
from shapely.geometry import Polygon as ShapelyPolygon
from shapely import LineString as ShapelyLine
from shapely import Point as ShapelyPoint
from shapely.ops import nearest_points
from shapely.validation import make_valid
from pyglet import shapes
from enum import Enum
from shapely import affinity

class DisplayableShape():
       pass

class DisplayableRectangle(shapes.Rectangle, DisplayableShape):
        
        def __init__(self, x, y, width, height, color=..., batch=None, group=None):
                super().__init__(x, y, width, height, color, batch, group)

                self.shapely_shape = ShapelyPolygon([[x, y], [x+width, y], [x+width, y+height], [x, y+height]])


        def intersect(self, other):
            return self.shapely_shape.intersection(other.shapely_shape)
               

class DisplayableLine(shapes.Line, DisplayableShape):
       
       def __init__(self, x, y, x2, y2, width=1, color=..., batch=None, group=None):
              super().__init__(x, y, x2, y2, width, color, batch, group)

              self.shapely_shape = ShapelyLine([[x,y],[x2,y2]])

class DisplayableIntersection(shapes.Star, DisplayableShape):
     def __init__(self, x, y, outer_radius, inner_radius, num_spikes, rotation=0, color=..., batch=None, group=None) -> None:
          super().__init__(x, y, outer_radius, inner_radius, num_spikes, rotation, color, batch, group)

          self.shapely_shape = ShapelyPoint(x,y)

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
    np.array([0,1]),
    np.array([0,-1]),
    np.array([-1,0]),
    np.array([1,0]),
    np.array([-1,1]),
    np.array([1,1]),
    np.array([-1,-1]),
    np.array([1,-1])
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

class GridWorld():
     
    def __init__(self, grid_size, tile_size) -> None:
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.objects = []

    def add(self, object):
         self.objects.append(object)

    

class Robot():
    def __init__(self, x,y, batch, sensor_length=100) -> None:
        self.location = np.array([x,y])
        self.sensor_length = sensor_length
        self.laser_color = (124,252,0)
        self.color =(255,18,18)
        self.batch = batch
        self.direction = 0 # look up by default
        self.sensor = DisplayableLine(x=x+5, y=y+5, x2=x+5, y2=y+5+sensor_length, color=self.laser_color, batch=batch)
        self.body = DisplayableRectangle(x,y, 10,10, color=(255,18,18), batch=batch)
        self.body.opacity = 128
        self.closest_sensed_obj = None
        self.mass_center = shapely.Point((x+5,y+5))

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
        
        if self.closest_sensed_obj != None:
            # delete old DisplayableIntersection 
            self.closest_sensed_obj.delete()
            self.closest_sensed_obj = None
        if closest_obj:
            # Add new DisplayableIntersection
            self.closest_sensed_obj = DisplayableIntersection(closest_obj.x, closest_obj.y, 
                                                              10, 3, 10, color=(255,255,0), batch=batch)

    def print_sensor_loc(self):
        print("Sensor loc: ", self.sensor.shapely_shape.coords.xy)

    def get_sensor(self, direction):
        x = self.location[0]
        y = self.location[1]

        line = ShapelyLine([[x+5,y+5],[x+5,y+5+self.sensor_length]])
        angle = rotations[direction.value]
        # get rotated sensor
        line = affinity.rotate(line, angle, origin=(x+5, y+5))

        x2 = line.coords.xy[0][1]
        y2 = line.coords.xy[1][1]
        # print(line.coords.xy)
        return DisplayableLine(x+5,y+5,x2,y2, color=self.laser_color, batch=self.batch)

    def deterministic_move(self, direction):
        self.location = self.location+directions[direction.value]*10
        self.body.delete()
        self.body = DisplayableRectangle(self.location[0], self.location[1], 10, 10, color=self.color, batch=self.batch)
        self.body.opacity = 128
        self.sensor.delete()
        self.sensor = self.get_sensor(direction)

        print(f'New position: {self.location+directions[direction.value]*10}')


window = Window(width=720, height=720)
batch = pyglet.graphics.Batch()

robot = Robot(500,500, batch, sensor_length=200)

world = GridWorld(720, 10)


dd = True

def update(dt):
    print(f'Dt={dt}')
    r = np.random.random()

    if r > 0.5:
        robot.deterministic_move(Direction.DOWN_LEFT)
    else:
        robot.deterministic_move(Direction.DOWN_RIGHT)
    # robot.print_sensor_loc()
    robot.get_intersection(world)



if __name__ == '__main__': 


    rec1 = DisplayableRectangle(300,250,100,200, color=(255,20,147), batch=batch)
    # rec1.opacity = 128
    print(rec1)
    world.add(rec1)

    rec2 = DisplayableRectangle(500,250,200,100, color=(255,20,147), batch=batch)
    # rec2.opacity = 128
    world.add(rec2)

    rec2 = DisplayableRectangle(100,350,200,100, color=(255,20,147), batch=batch)
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

