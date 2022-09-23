from turtle import pos
from numpy import array
from pymunk import Space
from pymunk.bb import Vec2d
from .settings import *
from pygad import GA
from .models import *


class AgentManager:

    objects: list[AbstractAgentModel]

    def __init__(self,
                 app,
                 model: tuple
                 ):
        self.app = app
        self.space = app.space
        self.ga = model[1](self)
        self.model = model[0]
        self.model.init_environmental(self.space)
        self.objects = [1 for _ in range(len(self.ga.ga.population))]

    def start(self):
        self.ga.start_ga()
