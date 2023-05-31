import abc
from shapely import Point as ShapelyPoint
from shapely.geometry import Polygon as ShapelyPolygon
from shapely import geometry

from pyglet import shapes, image, sprite


class DisplayableShape(abc.ABC):
    shapely_shape = None


class DisplayableRectangle(shapes.Rectangle, DisplayableShape):

    def __init__(self, x, y, width, height, color=..., batch=None, group=None):
        super().__init__(x, y, width, height, color, batch, group)

        self.shapely_shape = ShapelyPolygon([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])


class DisplayableObstacle(DisplayableRectangle):
    def __init__(self, x, y, width, height, color=..., textured=True, batch=None, group=None):
        super().__init__(x, y, width, height, color, batch, group)

        self.sprite = None
        self.batch = batch
        if textured:
            self.load_texture()

    def load_texture(self):
        original_texture = image.load('./textures/brick_wall.jpg').get_texture()
    
        # Here, we make the assumption that the size of the texture is greater than or equal to the size of the rectangle.
        cropped_texture = original_texture.get_region(0, 0, original_texture.width, original_texture.height)
    
        self.sprite = sprite.Sprite(cropped_texture, x=self.x, y=self.y, batch=self.batch)
        self.opacity = 0
    
        self.sprite.scale_x = self.width / original_texture.width
        self.sprite.scale_y = self.height / original_texture.height


class DisplayableCircle(shapes.Circle, DisplayableShape):
    def __init__(self, x, y, radius, segments=None, color=..., batch=None, group=None):
        super().__init__(x, y, radius, segments, color, batch, group)

        self.shapely_shape = ShapelyPoint(x, y).buffer(radius)


class DisplayablePolygon(shapes.Polygon, DisplayableShape):

    def __init__(self, *coordinates, color=..., batch=None, group=None):
        super().__init__(*coordinates, color=color, batch=batch, group=group)

        self.shapely_shape = ShapelyPolygon(coordinates)