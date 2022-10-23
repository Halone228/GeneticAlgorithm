from . import AbstractAgentModel,AbstractAgentGA
from .objects import DroneAgent as drone
from pymunk.vec2d import Vec2d
import numpy
from numpy import array
import pygad
from simul.settings import *
import os


def activation(n):
    return 1/(1+numpy.exp(-n))


class Drone(AbstractAgentModel):
    inputs = 6

    def init_individual(self):
        self.agent = drone(self.space)

    def died_func(self):
        pos = self.agent.main_body.position
        pos = Vec2d(pos.x // WIDTH, pos.y // HEIGHT)
        self.is_died = (pos.x != 0 or pos.y != 0 or pos.y < 0)

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
            max_force = -3000
            left_force = Vec2d(0, numpy.nan_to_num(activation(outputs[2])*max_force))
            right_force = Vec2d(0, numpy.nan_to_num(activation(outputs[5])*max_force))
            # print(f'R:{right_force}::L:{left_force}')
            self.agent.left_body.angle = numpy.nan_to_num(left_angel)
            self.agent.right_body.angle = numpy.nan_to_num(right_angel)
            self.agent.left_body.apply_force_at_local_point(left_force)
            self.agent.right_body.apply_force_at_local_point(right_force)
            self.fitness += 1/FPS
            self.died_func()

    def init_environmental(self):
        pass


class DroneGA(AbstractAgentGA):
    def init_logic(self):
        self.init_range_low = 0.5
        self.init_range_high = 10
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
            random_mutation_min_val=-.5,
            random_mutation_max_val=.5,
            on_generation=self.on_generations,
            save_best_solutions=bool(os.environ.get('save_best'))
        )