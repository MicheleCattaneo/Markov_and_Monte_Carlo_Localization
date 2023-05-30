from shapely.geometry import Point as ShapelyPoint
from typing import List, Tuple
import numpy as np
from base.shapes import DisplayableRectangle
from definitions import defs


class ContinuousWorld:
    def __init__(self, width: int, height: int, tile_size, batch) -> None:
        self.height, self.width = height, width
        self.batch = batch

        self.objects = []
        for obj, kwargs in defs.objects:
            points = (np.array(kwargs.pop("points")) * tile_size).tolist()
            self.objects.append(obj(*points, **kwargs, batch=batch))

        self.objects += self._get_walls(width, height, (255, 255, 255), batch)
        
    def _get_walls(self, width: int, height: int, color: Tuple[int, int, int], batch) -> List[DisplayableRectangle]:
        thickness = 10  # Define your wall thickness here
        return [
            DisplayableRectangle(0, 0, width, thickness, color=color, batch=batch),
            DisplayableRectangle(0, 0, thickness, height, color=color, batch=batch),
            DisplayableRectangle(width - thickness, 0, thickness, height, color=color, batch=batch),
            DisplayableRectangle(0, height - thickness, width, thickness, color=color, batch=batch)
        ]

    def is_occupied(self, x: float, y: float) -> bool:
        point = ShapelyPoint(x, y)
        
        for obj in self.objects:
            if obj.shapely_shape.contains(point):
                return True
                
        return False

    def check_within_boundaries(self, x: float, y: float) -> bool:
        return 0 <= x <= self.width and 0 <= y <= self.height

