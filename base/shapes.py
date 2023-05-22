import abc
from shapely import Point as ShapelyPoint
from shapely import LineString as ShapelyLine
from shapely.geometry import Polygon as ShapelyPolygon

from pyglet import shapes, image, gl, sprite


class DisplayableShape(abc.ABC):
    shapely_shape = None


class DisplayableRectangle(shapes.Rectangle, DisplayableShape):

    def __init__(self, x, y, width, height, color=..., batch=None, group=None):
        super().__init__(x, y, width, height, color, batch, group)

        self.shapely_shape = ShapelyPolygon([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])

    def intersect(self, other):
        return self.shapely_shape.intersection(other.shapely_shape)
    

class DisplayableObstacle(DisplayableRectangle):
    def __init__(self, x, y, width, height, color=..., batch=None, group=None):
        super().__init__(x, y, width, height, color, batch, group)

        self.sprite = None
        self.load_texture()

    def load_texture(self):
        original_texture = image.load('./textures/brick_wall.jpg').get_texture()
    
        # Here, we make the assumption that the size of the texture is greater than or equal to the size of the rectangle.
        cropped_texture = original_texture.get_region(0, 0, original_texture.width, original_texture.height)
    
        self.sprite = sprite.Sprite(cropped_texture, x=self.x, y=self.y, batch=self.batch)
    
        self.sprite.scale_x = self.width / original_texture.width
        self.sprite.scale_y = self.height / original_texture.height


class DisplayableCircle(shapes.Circle, DisplayableShape):
    def __init__(self, x, y, radius, segments=None, color=..., batch=None, group=None):
        super().__init__(x, y, radius, segments, color, batch, group)

        self.shapely_shape =ShapelyPoint(x, y).buffer(radius)


class DisplayableRobot(DisplayableShape):
    def __init__(self, x, y, radius, batch=None, group=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.batch = batch
        self.group = group

        self.sprite = None
        self.load_texture()

    def load_texture(self):
        texture_atlas = image.load('./textures/baby_sprites.png').get_texture()

        sprite_x = 0
        sprite_y = 0
        sprite_width = texture_atlas.width // 12
        sprite_height = texture_atlas.height // 8

        sprite_image_data = texture_atlas.get_image_data()
        sprite_image_data = sprite_image_data.get_region(sprite_x, sprite_y, sprite_width, sprite_height)
        sprite_texture = sprite_image_data.get_texture()

        self.sprite = sprite.Sprite(sprite_texture, x=self.x, y=self.y, batch=self.batch)
        self.sprite.scale = self.radius / sprite_width  # Scale to match the width of the circle

        self.sprite.scale = self.radius * 3 / sprite_texture.height

        # self.sprite.x = self.x + self.sprite.width // 4
        # self.sprite.y = self.y + self.sprite.height // 4


    def delete(self):
        if self.sprite is not None:
            self.sprite.delete()

    def set_rotation(self, angle):
        self.sprite.anchor_x = 1* self.sprite.width // 10
        self.sprite.anchor_y = 1* self.sprite.height // 10


        if self.sprite is not None:
            self.sprite.rotation = angle.value * 45


class DisplayableLine(shapes.Line, DisplayableShape):

    def __init__(self, x, y, x2, y2, width=1, color=..., batch=None, group=None):
        super().__init__(x, y, x2, y2, width, color, batch, group)

        self.shapely_shape = ShapelyLine([[x, y], [x2, y2]])


class DisplayableIntersection(shapes.Star, DisplayableShape):
    def __init__(self, x, y, outer_radius, inner_radius, num_spikes, rotation=0, color=..., batch=None,
                 group=None) -> None:
        super().__init__(x, y, outer_radius, inner_radius, num_spikes, rotation, color, batch, group)

        self.shapely_shape = ShapelyPoint(x, y)
