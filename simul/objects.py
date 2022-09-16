from pymunk.body import Body
from pymunk import Space
from pymunk.shapes import (
    Circle as _T_circle,
    Poly as _T_poly,
    Shape as _T_shape
)
from pymunk.bb import Vec2d
from pygame import Color
from pygame import key
import pygame as pg


_T_num = float|int


class Shape:
    shape: _T_shape
    body: Body

    def __init__(self,
                 position: Vec2d,
                 mass: _T_num = 20.0,
                 friction: _T_num = 0,
                 color: tuple = (174,160,140),
                 body_type=Body.DYNAMIC):
        self.body = Body()
        self.mass = mass
        self.body.position = position
        self.pos = position
        self.friction = friction
        self.color = color
        self.body.body_type = body_type

    def __init_defaults__(self):
        try:
            self.shape
        except NameError:
            raise ValueError("Shape not defined")

        self.shape.friction = self.friction
        self.shape.color = Color(*self.color)
        self.shape.mass = self.mass

    def add_to_space(self, space: Space):
        space.add(self.body, self.shape)

    def update(self):
        pass


class Rect(Shape):
    def __init__(self,
                 position: Vec2d,
                 w: int,
                 h: int,
                 mass: float = 20,
                 friction: float = 0,
                 color: tuple = (174,160,140),
                 is_dynamic: bool = True):
        super().__init__(Vec2d(position.x+w//2,position.y-h//2),mass,friction,color,
                         Body.DYNAMIC if is_dynamic else Body.KINEMATIC)
        self.shape = _T_poly.create_box(self.body, (w, h))
        self.__init_defaults__()


class Circle(Shape):
    def __init__(self,
                 position: Vec2d,
                 radius: _T_num,
                 mass: _T_num = 20,
                 friction: _T_num = 0,
                 color: tuple = (174, 160, 140),
                 is_dynamic: bool = True):
        super().__init__(position,mass,friction,color,Body.DYNAMIC if is_dynamic else Body.KINEMATIC)
        self.radius = radius
        self.shape = _T_circle(self.body, radius)
        self.__init_defaults__()

    def get_keys(self):
        keys = key.get_pressed()
        if keys[pg.K_d]:
            self.shape.body.apply_force_at_local_point((100,0))
        if keys[pg.K_a]:
            self.shape.body.apply_force_at_local_point((-100, 0))

    def update(self):
        self.get_keys()


class Agent:

    def __init__(self,space: Space):
        self.__init_body__(position)
        space.add_to_space(
                self.rect_body,self.rect_shape,
                self.forward_wheel_body,self.forward_wheel_shape
                self.forward_string,
                self.back_wheel_body,self.back_wheel_shape,
                self.back_string
            )

    def __init_body__(self,
                    position: Vec2d):
        self.rect_body = Body()
        self.body.position
        self.rect_shape = Poly.create_box(self.rect_body,(100,40))
        self.rect_shape.mass = 5
        self.rect_shape.friction = 0.5
        verticels = self.rect_body.get_vertices()
        ##CREATE FORWARD WHEEL
        self.forward_wheel_body = Body() 
        self.forward_wheel_body.position = verticels[0] - Vec2d(0,40)
        self.forward_wheel_shape = _T_circle(self.forward_wheel_body, 10)
        self.forward_wheel_shape.mass = 1
        self.forward_string = DampedRotaryString(
            self.rect_body,
            self.forward_wheel_body,
            0,
            .5,
            .5
        )
        self.forward_string.collide_bodies = False
        ##END OF CREATE FORWARD WHEEL
        ##CREATE BACK WHEEL
        self.back_wheel_body = Body()
        self.back_wheel_body.position = verticels[-1] - Vec2d(0,40)
        self.back_wheel_shape = _T_circle(self.back_wheel_body, 10)
        self.back_wheel_shape.mass = 1
        self.back_string = DampedRotaryString(
            self.rect_body,
            self.back_wheel_body,
            0,
            .5,
            .5
        )


