from shapely.geometry import Polygon as ShapelyPolygon

class GridWorld:

    def __init__(self, grid_size, tile_size) -> None:
        self.grid_size = grid_size
        self.tile_size = tile_size
        self.objects = []

    def add(self, object):
        self.objects.append(object)


    def get_collision_bounds_dictionary(self):
        '''
        Returns a dictionary containing a pair (i,j) when the corresponding tile
        as indices i,j contains an object. The robot can not go on those tiles.
        '''
        dic = {}
        width = self.tile_size - 2
        for x in range(0, self.grid_size, self.tile_size):
            for y in range(0, self.grid_size, self.tile_size):
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
                        dic[(int(x/self.tile_size), int(y/self.tile_size))] = True
                        break

        return dic
