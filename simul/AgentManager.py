from objects import Agent
from base import LogicManager
from numpy import array
from pymunk import Space
from pymunk.bb import Vec2d
from settings import *
from pygad import GA


class SoloManager:
    is_died: bool = False

    def __init__(self,
                 num: int,
                 weights: array,
                 space: Space):
        self.num = num
        self.agent = Agent(space)
        self.weights = weights
        self.fitness = 0

    def is_died_func(self):
        if abs(self.agent.angel) >= 1 or 0 > self.agent.down_rect.position.x > 720:
            self.is_died = True
            del self.agent

    def step(self):
        if not self.is_died:
            inputs = array([self.agent.angel*10, self.agent.velocity_x/80.])
            force = Vec2d(sum(inputs * self.weights), 0)*10
            print(force)
            self.agent.down_rect.velocity = force
            self.fitness += 1/FPS
            self.is_died_func()
            if self.fitness > 10:
                is_died = True


class AgentManager:

    objects: list[SoloManager]

    def __init__(self,
                 app):
        self.app = app
        self.space = app.space
        self.ga = LogicManager(2,self.on_fitness,self.fitness_func)
        global objects
        objects = [1 for _ in range(len(self.ga.ga_instance.population))]
        global manager
        manager = self

    @staticmethod
    def on_fitness(gad: GA, genes: array):
        objects = [SoloManager(num,weights,manager.space) for num,weights in enumerate(genes,start=0)]
        while True if False in [o.is_died for o in objects] else False:
            manager.app.iter()
            for obj in objects:
                obj.step()

    @staticmethod
    def fitness_func(_,num):
        try:
            return objects[num].fitness
        except:
            return objects[num]