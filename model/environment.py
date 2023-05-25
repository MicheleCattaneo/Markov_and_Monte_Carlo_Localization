from typing import List, Tuple

import numpy as np
from shapely.geometry import Polygon as ShapelyPolygon

from base.shapes import DisplayableRectangle, DisplayableObstacle, DisplayablePolygon


class GridWorld:

    def __init__(self, width: int, height: int, tile_size, batch) -> None:
        self.tile_size = tile_size
        self.height, self.width = np.array([height, width]) // tile_size
        self.batch = batch

        self.objects = [
                           # DisplayableRectangle(300, 250, 100, 200, color=(255, 20, 147), batch=batch),
                           # DisplayableRectangle(400, 250, 200, 100, color=(255, 20, 147), batch=batch),
                           # DisplayableRectangle(100, 350, 200, 100, color=(255, 20, 147), batch=batch),
                           # DisplayableRectangle(300, 500, 200, 100, color=(255, 20, 147), batch=batch),
                            # DisplayableObstacle(tile_size, 7 * tile_size, 2 * tile_size, 2 * tile_size,
                            #                     color=(255, 20, 147), batch=batch),
                            # DisplayableObstacle(5 * tile_size, 12 * tile_size, 2 * tile_size, 2 * tile_size,
                            #                     color=(255, 20, 147), batch=batch),
                            # DisplayableObstacle(5 * tile_size, 5 * tile_size, 4 * tile_size, 3 * tile_size,
                            #                     color=(255, 20, 147), batch=batch)
                        DisplayableObstacle(5 * tile_size, 5 * tile_size, 2 * tile_size, 10 * tile_size,
                                                color=(255, 20, 147), batch=batch),
                        DisplayableObstacle(10 * tile_size, 5 * tile_size, 2 * tile_size, 10 * tile_size,
                                                color=(255, 20, 147), batch=batch),
                        DisplayableObstacle(5 * tile_size, 25 * tile_size, 2 * tile_size, 10 * tile_size,
                                                color=(255, 20, 147), batch=batch),
                        DisplayableObstacle(10 * tile_size, 25 * tile_size, 2 * tile_size, 10 * tile_size,
                                                color=(255, 20, 147), batch=batch),
                        DisplayablePolygon([20* tile_size,20* tile_size],
                                           [25* tile_size,25* tile_size],
                                           [20* tile_size,25* tile_size],
                                            [18* tile_size,23* tile_size], 
                                            [20* tile_size,20* tile_size],
                                           color=(255, 20, 147), 
                                           batch=batch)                                                  
                       ] + self._get_walls(width, height, (255, 255, 255), batch)

        self.walkable = self._compute_walkable_areas()

    def _get_walls(self, width: int, height: int, color: Tuple[int, int, int], batch) -> List[DisplayableRectangle]:
        return [
            DisplayableRectangle(0, 0, width, self.tile_size, color=color, batch=batch),
            DisplayableRectangle(0, 0, self.tile_size, height, color=color, batch=batch),
            DisplayableRectangle(width - self.tile_size, 0, self.tile_size, height, color=color, batch=batch),
            DisplayableRectangle(0, height - self.tile_size, width, self.tile_size, color=color, batch=batch)
        ]

    def _compute_walkable_areas(self):
        """
        Returns a dictionary containing a pair (i,j) when the corresponding tile
        as indices i,j contains an object. The robot can not go on those tiles.
        """
        width = self.tile_size - 2
        walkable = np.ones((self.width, self.height), dtype=bool)
        for i in range(self.width):
            for j in range(self.height):
                x, y = np.array([i, j]) * self.tile_size

                # create a fake robot body,
                # of 1 pixel smaller in each direction (e.g 9x9 instead of 10x10)
                robot_body = ShapelyPolygon([[x + 1, y + 1],
                                             [x + 1 + width, y + 1],
                                             [x + 1 + width, y + width + 1],
                                             [x + 1, y + width + 1]])

                # For each object in the world, check whether the fake body would
                # intersect or be contained by the object
                for o in self.objects:
                    if o.shapely_shape.contains(robot_body) or o.shapely_shape.intersects(robot_body):
                        walkable[i, j] = False
                        break

        return walkable
