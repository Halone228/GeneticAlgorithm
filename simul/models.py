from abc import ABCMeta, abstractproperty,abstractmethod,abstractstaticmethod
from .objects import Agent as default_Agent
from numpy import array
from pymunk import Space
from .settings import *
import math
from .objects import *


class AbstractAgentModel(metaclass=ABCMeta):
    agent: any
    is_died: bool = False

    @property
    @abstractmethod
    def inputs(self) -> int: ...

    @abstractmethod
    def init_individual(self): ...

    @abstractmethod
    def died_func(self): ...

    @abstractmethod
    def step(self): ...

    @abstractstaticmethod
    def init_environmental(self): ...

    def __init__(self,
                 num: int,
                 weights: array,
                 space: Space):
        self.num = num
        self.space = space
        self.weights = weights
        self.fitness = 0
        self.init_individual()

    def __repr__(self):
        return f"Agent::{self.__class__}(num={self.num},is_died={self.is_died})"


class Equilibrium(AbstractAgentModel):
    inputs = 2

    def init_individual(self):
        self.agent = default_Agent(self.space)

    def died_func(self):
        if abs(self.agent.angel) >= 1 or 0 > self.agent.down_rect.position.x > 720:
            self.is_died = True
            del self.agent

    def step(self):
        if not self.is_died:
            position = (self.agent.position-WIDTH/2)/(WIDTH/4)
            inputs = array([self.agent.angel*math.pi, position])
            force = Vec2d(sum(inputs * self.weights), 0)*50
            self.agent.down_rect.velocity = force
            self.fitness += 1/FPS
            self.died_func()
            if self.fitness > 1000:
                self.is_died = True

    @staticmethod
    def init_environmental(space):
        ground = Rect(Vec2d(.0, float(HEIGHT)), WIDTH, 100, is_dynamic=False, friction=0.1)
        ground.add_to_space(space)
