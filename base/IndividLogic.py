# Переписать по подобию документации
import pygad
from pprint import pprint
import numpy
import types


class LogicManager:
    num_generations = 400
    num_parents_mating = 2

    sol_per_pop = 10

    init_range_low = -100
    init_range_high = 100

    parent_selection_type = "rws"
    keep_parents = 2

    crossover_type = "uniform"

    mutation_type = "random"
    mutation_percent_genes = 10

    def __init__(self, input_len: int, on_fitness, fitness_function):
        """on_fitness=None: Accepts a function to be called after calculating the fitness values of all solutions in
        the population. This function must accept 2 parameters: the first one represents the instance of the genetic
        algorithm and the second one is a list of all solutions’ fitness values. Added in PyGAD 2.6.0.
        CHECK https://pygad.readthedocs.io/en/latest/README_pygad_ReadTheDocs.html#life-cycle-of-pygad"""
        self.on_fitness = on_fitness
        self.fitness_function = fitness_function
        self.num_genes = input_len
        self.ga_instance = pygad.GA(num_generations=self.num_generations,
                                    num_parents_mating=self.num_parents_mating,
                                    fitness_func=self.fitness_function,
                                    sol_per_pop=self.sol_per_pop,
                                    num_genes=self.num_genes,
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

    def start(self):
        self.ga_instance.run()
        print(self.ga_instance.population)
        print(self.ga_instance)
        self.ga_instance.save('new_weights')
