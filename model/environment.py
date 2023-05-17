import numpy as np
from shapely.geometry import Polygon as ShapelyPolygon

from base.shapes import DisplayableRectangle


class GridWorld:

    def __init__(self, resolution, tile_size, sensor_range: float, batch) -> None:
        self.resolution = resolution
        self.tile_size = tile_size
        self.height, self.width = np.array(resolution) // tile_size

        self.sensor_range = sensor_range

        self.objects = [
            # DisplayableRectangle(300, 250, 100, 200, color=(255, 20, 147), batch=batch),
            # DisplayableRectangle(400, 250, 200, 100, color=(255, 20, 147), batch=batch),
            # DisplayableRectangle(100, 350, 200, 100, color=(255, 20, 147), batch=batch),
            # DisplayableRectangle(300, 500, 200, 100, color=(255, 20, 147), batch=batch),
            DisplayableRectangle(10, 70, 20, 20, color=(255, 20, 147), batch=batch)
        ]

        self.walkable = self._compute_walkable_areas()

    def _compute_walkable_areas(self):
        '''
        Returns a dictionary containing a pair (i,j) when the corresponding tile
        as indices i,j contains an object. The robot can not go on those tiles.
        '''
        width = self.tile_size - 2
        walkable = np.ones((self.height, self.width), dtype=bool)
        for x in range(0, self.resolution[0], self.tile_size):
            for y in range(0, self.resolution[1], self.tile_size):
                # create a fake robot body, 
                # of 1 pixel smaller in each direction (e.g 9x9 instead of 10x10)
                robot_body = ShapelyPolygon([[x+1, y+1], 
                                             [x+1 + width, y+1], 
                                             [x+1 + width, y + width+1], 
                                             [x+1, y + width+1]])
                
                # For each object in the world, check whether the fake body would
                # intersect or be contained by the object
                for o in self.objects:
                    if o.shapely_shape.contains(robot_body) or o.shapely_shape.intersects(robot_body):
                        walkable[x//self.tile_size, y//self.tile_size] = False
                        break

        return walkable


