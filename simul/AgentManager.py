from turtle import pos
from .objects import Agent
from base import LogicManager
from numpy import array
from pymunk import Space
from pymunk.bb import Vec2d
from .settings import *
from pygad import GA
from .models import *


def smooth_func(a):
    return 1/((-1 if a < 0 else 1)+a)


class AgentManager:

    objects: list[AbstractAgentModel]

    def __init__(self,
                 app,
                 model):
        self.app = app
        self.space = app.space
        self.ga = LogicManager(model.inputs,self.on_fitness,self.fitness_func)
        self.model = model
        self.objects = [1 for _ in range(len(self.ga.ga_instance.population))]
        global manager
        manager = self

    @staticmethod
    def on_fitness(gad: GA, genes: array):
        manager.objects = [manager.model(num,weights,manager.space) for num,weights in enumerate(genes, start=0)]
        while [obj for obj in manager.objects if not obj.is_died]:
            manager.app.iter()
            for obj in manager.objects:
                obj.step()
        manager.app.generation += 1

    @staticmethod
    def fitness_func(_, num):
        try:
            return manager.objects[num].fitness
        except:
            return manager.objects[num]

