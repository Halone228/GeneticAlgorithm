import math

from . import AbstractAgentGA, AbstractAgentModel
from pymunk.vec2d import Vec2d
from .objects import EquilibriumAgent as default_Agent
from .objects import Rect
import pygad
from simul.settings import *
import os
import numpy
from numpy import array


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
            velocity = (4*self.agent.velocity_x-2*WIDTH)/WIDTH
            inputs = array([math.degrees(self.agent.angel), position, velocity])
            force = Vec2d(sum(inputs * self.weights), 0)
            self.agent.down_rect.apply_impulse_at_local_point(force)
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
        self.parent_selection_type = 'tournament'
        self.K_tournament = 10
        self.ga = pygad.GA(num_generations=self.num_generations,
                           num_parents_mating=self.num_parents_mating,
                           fitness_func=self.fitness_func,
                           sol_per_pop=self.sol_per_pop,
                           num_genes=3,
                           init_range_low=self.init_range_low,
                           init_range_high=self.init_range_high,
                           parent_selection_type=self.parent_selection_type,
                           keep_parents=self.keep_parents,
                           crossover_type=self.crossover_type,
                           mutation_type=self.mutation_type,
                           mutation_percent_genes=self.mutation_percent_genes,
                           K_tournament=self.K_tournament,
                           mutation_num_genes=1,
                           gene_type=float,
                           on_fitness=self.on_fitness,
                           mutation_by_replacement=True,
                           allow_duplicate_genes=True,
                           random_mutation_min_val=-.5,
                           random_mutation_max_val=.5,
                           on_generation=self.on_generations,
                           initial_population=self.initial_population
                           )
