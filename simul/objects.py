import pymunk
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
from pymunk.constraints import *
import random
from .settings import AGENT_POS

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
                 friction: float = 1,
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

    def __init__(self,space: Space, position: Vec2d = AGENT_POS):
        """
        Size 100w 40h
        :param space:
        """
        self.__init_body__(position)

        self.joint.collide_bodies = False
        space.add(
                self.joint,
                self.down_rect,self.down_shape,
                self.up_rect,self.up_shape
            )
        self.space = space
        self.up_rect.apply_impulse_at_local_point(Vec2d(random.random(),0))
        filter = pymunk.ShapeFilter(group=1)
        self.down_shape.filter = filter
        self.up_shape.filter = filter

    def __init_body__(self,
                      position: Vec2d):
        self.down_rect = Body(body_type=Body.KINEMATIC)
        self.down_rect.position = position
        self.down_shape = _T_poly.create_box(self.down_rect,(100,40))
        self.down_shape.friction = 0.5
        self.up_rect = Body()
        up_rect_height = 150
        self.up_shape = _T_poly.create_box(self.up_rect,(10,up_rect_height))
        self.up_rect.position = position + Vec2d(0,-up_rect_height//2)
        self.up_shape.mass = 0.01
        self.joint = PivotJoint(self.down_rect, self.up_rect,
                                position)

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.down_rect.apply_force_at_local_point((100,0))
        if keys[pg.K_a]:
            self.down_rect.apply_force_at_local_point((-100,0))
        print(self.angel)

    @property
    def angel(self):
        """In radians"""
        return self.up_rect.angle

    @property
    def velocity_x(self):
        return self.down_rect.velocity.x

    @property
    def position(self):
        return self.down_rect.position.x

    def __del__(self):
        self.space.remove(self.down_rect,self.down_shape,self.up_rect,self.up_shape,self.joint)
