import pickle
import os
from abc import ABCMeta, abstractproperty, abstractmethod
import numpy
from tqdm import tqdm
import pygad
from numpy import array
from pymunk import Space
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib


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
    num_generations = 10000
    num_parents_mating = 8
    sol_per_pop = 40
    init_range_low = -3
    init_range_high = 3
    parent_selection_type = "rws"
    keep_parents = -1
    crossover_type = "uniform"
    mutation_type = "random"
    mutation_percent_genes = 8
    initial_population = None

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
        # self.save()
        # self.ga.save('eq.pkl')

    def __init__(self,
                 manager):
        # self.load()
        self.init_logic()
        self.manager = manager
        self.tqdm = tqdm(total=self.num_generations)
        if os.environ['plot']:
            self.fig: Figure = matplotlib.pyplot.figure()
            matplotlib.pyplot.show(block=False)

    def on_generations(self,*args):
        self.tqdm.update(1)
        self.manager.app.update_time()
        if self.ga.generations_completed > 1 and os.environ['plot']:
            font_size = 14
            matplotlib.pyplot.title('Fitness/Generation', fontsize=font_size)
            matplotlib.pyplot.xlabel("Generation", fontsize=font_size)
            matplotlib.pyplot.ylabel("Fitness", fontsize=font_size)
            matplotlib.pyplot.draw()
            matplotlib.pyplot.pause(0.001)
            matplotlib.pyplot.plot(self.ga.best_solutions_fitness, linewidth=3, color="#3870FF")
            # matplotlib.pyplot.savefig(fname='plot.png',bbox_inches='tight')
        if len(self.ga.best_solutions) > self.ga.sol_per_pop*5:
            self.ga.best_solutions = self.ga.best_solutions[len(self.ga.best_solutions)-self.ga.sol_per_pop:]

    # def save(self):
    #     if os.environ.get('save_path', False):
    #         # self.ga.save(str(os.environ['save_path']))
    #         with open(os.environ.get('save_path')+'.pkl','wb') as f:
    #             pickle.dump(self.ga.best_solutions[len(self.ga.best_solutions)-self.sol_per_pop:], f)
    #
    # def load(self):
    #     if os.environ.get('load_path', False):
    #         with open(os.environ.get('load_path')+'.pkl', 'rb') as f:
    #             loaded_values = pickle.load(f)
    #             self.initial_population = loaded_values


from .equilibrim import Equilibrium, EquilibriumGA
from .drone import Drone, DroneGA

