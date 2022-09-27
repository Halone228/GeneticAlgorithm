from abc import ABCMeta, abstractproperty, abstractmethod

import numpy

from .objects import EquilibriumAgent as default_Agent, DroneAgent as drone
from numpy import array
from pymunk import Space
from .settings import *
import math
from .objects import *
import pygad
from pygad.nn import sigmoid


class AbstractAgentModel(metaclass=ABCMeta):
    """
    Model agent handles all processes between environmental and GA.
    For each model NEED to be implemented.

    """
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

    @staticmethod
    @abstractmethod
    def init_environmental(space): ...

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


class AbstractAgentGA(metaclass=ABCMeta):
    """
    Abstract object of main GA logic. For each model NEED to be implemented.
    """
    ga: pygad.GA
    # Class have GA variables, for specific model it can be different
    num_generations = 30000
    num_parents_mating = 2
    sol_per_pop = 10
    init_range_low = 25
    init_range_high = 50
    parent_selection_type = "rws"
    keep_parents = 2
    crossover_type = "uniform"
    mutation_type = "random"
    mutation_percent_genes = 25

    def on_fitness(self, gad: pygad.GA, *args):
        self.manager.objects = [self.manager.model(num, weights, self.manager.space) for num, weights in
                                enumerate(gad.population, start=0)]
        while [obj for obj in self.manager.objects if not obj.is_died]:
            self.manager.app.iter()
            for obj in self.manager.objects:
                obj.step()
        self.manager.app.generation += 1

    def fitness_func(self, _, *args):
        try:
            return self.manager.objects[args[0]].fitness
        except AttributeError:
            return self.manager.objects[args[0]]

    @abstractmethod
    def init_logic(self): ...

    def start_ga(self):
        self.ga.run()

    def __init__(self,
                 manager):
        self.init_logic()
        self.manager = manager


class Equilibrium(AbstractAgentModel):
    inputs = 2

    def init_individual(self):
        self.agent = default_Agent(self.space)

    def died_func(self):

        if abs(self.agent.angel) >= 1 or self.agent.position < 0 or self.agent.position > WIDTH:
            self.is_died = True
            del self.agent

    def step(self):
        if not self.is_died:
            position = (4*self.agent.position-2*WIDTH)/WIDTH
            inputs = array([self.agent.angel * numpy.e, position])
            force = Vec2d(sum(inputs * self.weights), 0)*70
            self.agent.down_rect.velocity = force
            self.fitness += 1 / FPS
            self.died_func()
            if self.fitness > 1000:
                self.is_died = True

    @staticmethod
    def init_environmental(space):
        ground = Rect(Vec2d(.0, float(HEIGHT)), WIDTH, 100, is_dynamic=False, friction=0.1)
        ground.add_to_space(space)


class EquilibriumGA(AbstractAgentGA):

    def init_logic(self):
        self.ga = pygad.GA(num_generations=self.num_generations,
                           num_parents_mating=self.num_parents_mating,
                           fitness_func=self.fitness_func,
                           sol_per_pop=self.sol_per_pop,
                           num_genes=2,
                           init_range_low=self.init_range_low,
                           init_range_high=self.init_range_high,
                           parent_selection_type=self.parent_selection_type,
                           keep_parents=self.keep_parents,
                           crossover_type=self.crossover_type,
                           mutation_type=self.mutation_type,
                           mutation_percent_genes=self.mutation_percent_genes,
                           mutation_num_genes=1,
                           gene_type=float,
                           on_fitness=self.on_fitness,
                           mutation_by_replacement=True,
                           allow_duplicate_genes=True,
                           keep_elitism=5,
                           random_mutation_min_val=-.5,
                           random_mutation_max_val=.5)


class Drone(AbstractAgentModel):
    inputs = 6

    def init_individual(self):
        self.agent = drone(self.space)

    def died_func(self):
        pos = self.agent.main_body.position
        pos = Vec2d(pos.x//WIDTH, pos.y//HEIGHT)
        self.is_died = (pos.x != 0 or pos.y != 0)

    def step(self):
        if not self.is_died:
            inputs = array([self.agent.left_body.angle,
                            self.agent.main_body.angle,
                            self.agent.left_body.velocity.y,
                            self.agent.right_body.angle,
                            self.agent.main_body.angle,
                            self.agent.right_body.velocity.y])
            outputs = inputs*self.weights
            left_angel = outputs[0]+outputs[1]
            right_angel = outputs[3]-outputs[4]
            left_force = Vec2d(0,sigmoid(outputs[2])*500)
            right_force = Vec2d(0,sigmoid(outputs[5])*500)
            self.agent.left_body.angle = left_angel
            self.agent.right_body.angle = right_angel
            self.agent.left_body.apply_force_at_local_point(left_force)
            self.agent.right_body.apply_force_at_local_point(right_force)
            self.fitness += 1/1+abs(self.agent.main_body.velocity.y)
            self.died_func()

    def init_environmental(space):
        pass


class DroneGA(AbstractAgentGA):
    def init_logic(self):
        self.ga = pygad.GA(
            num_generations=self.num_generations,
            num_parents_mating=self.num_parents_mating,
            fitness_func=self.fitness_func,
            sol_per_pop=self.sol_per_pop,
            num_genes=6,
            init_range_low=self.init_range_low,
            init_range_high=self.init_range_high,
            parent_selection_type=self.parent_selection_type,
            keep_parents=self.keep_parents,
            crossover_type=self.crossover_type,
            mutation_type=self.mutation_type,
            mutation_percent_genes=self.mutation_percent_genes,
            mutation_num_genes=3,
            gene_type=float,
            on_fitness=self.on_fitness,
            mutation_by_replacement=True,
            allow_duplicate_genes=True,
            keep_elitism=5,
            random_mutation_min_val=-2,
            random_mutation_max_val=2
        )
