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
from simul.settings import AGENT_POS
from abc import ABCMeta, abstractmethod

_T_num = float | int


class AbstractAgent(metaclass=ABCMeta):
    @abstractmethod
    def __init_body__(self,
                      position): ...

    @abstractmethod
    def __init__(self, space: Space, position: Vec2d = AGENT_POS): ...

    def __del__(self): ...


class EquilibriumAgent(AbstractAgent):

    def __init__(self, space: Space, position: Vec2d = AGENT_POS):
        """
        Size 100w 40h
        :param space:
        """
        self.space = space
        self.__init_body__(position)
        self.joint.collide_bodies = False
        self.up_rect.apply_impulse_at_local_point(Vec2d(random.random() / 1000, 0))
        filter = pymunk.ShapeFilter(group=1)
        self.down_shape.filter = filter
        self.up_shape.filter = filter

    def __init_body__(self,
                      position: Vec2d):
        self.down_rect = Body(body_type=Body.DYNAMIC)
        self.down_rect.position = position
        self.down_shape = _T_poly.create_box(self.down_rect, (100, 40))
        self.down_shape.friction = 0.5
        self.down_shape.mass = 1
        self.down_shape.color = Color(102, 102, 153)
        self.up_rect = Body()
        up_rect_height = 500
        self.up_shape = _T_poly.create_box(self.up_rect, (10, up_rect_height))
        self.up_rect.position = position + Vec2d(0, -up_rect_height // 2)
        self.up_shape.mass = 0.00001
        self.up_shape.color = Color(102, 51, 0)
        self.joint = PivotJoint(self.down_rect, self.up_rect,
                                position)
        self.joint.color = Color(0, 102, 255)
        self.space.add(
            self.joint,
            self.down_rect, self.down_shape,
            self.up_rect, self.up_shape
        )

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
        self.space.remove(self.down_rect,
                          self.down_shape,
                          self.up_rect,
                          self.up_shape,
                          self.joint)


class DroneAgent(AbstractAgent):
    def __init__(self, space: Space, position: Vec2d = AGENT_POS):
        self.space = space
        self.__init_body__(position + Vec2d(0, -100))
        self.main_body.apply_impulse_at_local_point(Vec2d(random.random() / 1000, 0))
        filter_ = pymunk.ShapeFilter(group=1)
        self.main_shape.filter = filter_
        self.right_shape.filter = filter_
        self.left_shape.filter = filter_

    def __init_body__(self,
                      position: Vec2d):
        # Init bodies
        self.main_body = Body()
        self.main_body.position = position
        self.main_shape = _T_poly.create_box(self.main_body, (60, 20))
        self.main_shape.mass = 1
        self.left_body = Body()
        self.left_body.position = position + Vec2d(-60, 15)
        self.left_shape = _T_poly.create_box(self.left_body, (5, 15))
        self.left_shape.mass = 0.5
        self.left_shape.friction = 1
        self.right_body = Body()
        self.right_body.position = position + Vec2d(60, 15)
        self.right_shape = _T_poly.create_box(self.right_body, (5, 15))
        self.right_shape.mass = 0.5
        self.right_shape.friction = 1
        # Init joints
        main_vs = self.main_shape.get_vertices()
        self.left_joint1 = PinJoint(self.left_body, self.main_body, (0, 0), main_vs[-1])
        self.right_joint1 = PinJoint(self.right_body, self.main_body, (0, 0), main_vs[0])
        self.left_joint2 = PinJoint(self.left_body, self.main_body, (0, 0), main_vs[-2])
        self.right_joint2 = PinJoint(self.right_body, self.main_body, (0, 0), main_vs[1])

        self.space.add(
            self.left_joint1, self.right_joint1, self.left_joint2, self.right_joint2,
            self.main_body, self.main_shape,
            self.right_body, self.right_shape,
            self.left_body, self.left_shape
        )

    def __del__(self):
        self.space.remove(self.left_joint1, self.right_joint1,
                          self.left_joint2, self.right_joint2,
                          self.main_body, self.main_shape,
                          self.right_body, self.right_shape,
                          self.left_body, self.left_shape)


class Shape:
    shape: _T_shape
    body: Body

    def __init__(self,
                 position: Vec2d,
                 mass: _T_num = 20.0,
                 friction: _T_num = 0,
                 color: tuple = (174, 160, 140),
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

class Rect(Shape):
    def __init__(self,
                 position: Vec2d,
                 w: int,
                 h: int,
                 mass: float = 20,
                 friction: float = 1,
                 color: tuple = (174, 160, 140),
                 is_dynamic: bool = True):
        super().__init__(Vec2d(position.x + w // 2, position.y - h // 2), mass, friction, color,
                         Body.DYNAMIC if is_dynamic else Body.KINEMATIC)
        self.shape = _T_poly.create_box(self.body, (w, h))
        self.__init_defaults__()