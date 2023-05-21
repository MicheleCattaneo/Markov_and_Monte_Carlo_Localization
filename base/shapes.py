import abc
from shapely import Point as ShapelyPoint
from shapely import LineString as ShapelyLine
from shapely.geometry import Polygon as ShapelyPolygon

from pyglet import shapes


class DisplayableShape(abc.ABC):
    shapely_shape = None


class DisplayableRectangle(shapes.Rectangle, DisplayableShape):

    def __init__(self, x, y, width, height, color=..., batch=None, group=None):
        super().__init__(x, y, width, height, color, batch, group)

        self.shapely_shape = ShapelyPolygon([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])

    def intersect(self, other):
        return self.shapely_shape.intersection(other.shapely_shape)
    

class DisplayableCircle(shapes.Circle, DisplayableShape):
    def __init__(self, x, y, radius, segments=None, color=..., batch=None, group=None):
        super().__init__(x, y, radius, segments, color, batch, group)

        self.shapely_shape =ShapelyPoint(x, y).buffer(radius)


class DisplayableLine(shapes.Line, DisplayableShape):

    def __init__(self, x, y, x2, y2, width=1, color=..., batch=None, group=None):
        super().__init__(x, y, x2, y2, width, color, batch, group)

        self.shapely_shape = ShapelyLine([[x, y], [x2, y2]])


class DisplayableIntersection(shapes.Star, DisplayableShape):
    def __init__(self, x, y, outer_radius, inner_radius, num_spikes, rotation=0, color=..., batch=None,
                 group=None) -> None:
        super().__init__(x, y, outer_radius, inner_radius, num_spikes, rotation, color, batch, group)

        self.shapely_shape = ShapelyPoint(x, y)
