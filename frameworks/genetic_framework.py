'''
Framework for a genetic algorithm.
'''

import numpy as np
import random

class Generation:
    def __init__(self, population, num_attributes, fitness: "function", species = np.random.rand):
        self.population = population
        self.num_attributes = num_attributes
        self.populus = [species(num_attributes) for i in range(population)]
        self.fitness = fitness

    def fittest(self, survivor_rate):
        return sorted(self.populus, key = self.fitness, reverse = True)[:int(survivor_rate * self.population)]

    def prime_species(self):
        return max(self.populus, key = self.fitness)

class Evolution:
    def __init__(self, num_attributes, fitness: "function", mating: "function", species = np.random.rand):
        self.species = species
        self.fitness = fitness
        self.mating = mating
        self.num_attributes = num_attributes
        self.generations = []

    def add_generation(self, population, survivor_rate = 0.2):
        next_gen = Generation(population, self.num_attributes, self.fitness, species = self.species)
        if self.generations == []:
            self.generations.append(next_gen)
        else:
            next_gen.populus = self.generate_populus(population, self.generations[-1].fittest(survivor_rate))
            self.generations.append(next_gen)

    def generate_populus(self, population, fittest):
        return [self.mating(*random.sample(fittest, 2)) for i in range(population)]
        
    def evolve(self, population = 1000, generations = 10, survivor_rate = 0.2):
        for i in range(generations):
            self.add_generation(population, survivor_rate)
        prime = self.generations[-1].prime_species()
        return prime, self.fitness(prime)

    def prime_species(self):
        return self.generations[-1].prime_species()

def mse_benefit(predicted, target):
    return -sum((predicted - target)**2)

def mate_arrays(v1, v2, variance = 0.01):
    assert len(v1) == len(v2)
    return (v1 + v2) / 2 + (np.random.rand(len(v1))*2*variance - variance)
    #return np.array([random.choice((v1[i], v2[i])) for i in range(len(v1))]) + (np.random.rand(len(v1))*2*variance - variance)

#====================================================================================================================
def main():
    target = np.array([1,1,1,1,1,1,1,1,1,1])
    fitness_func = lambda x: mse_benefit(x, target)
    algo = Evolution(10, fitness_func, mate_arrays)
    for i in range(100):
        print(algo.evolve(1000, 1, 0.01))

if __name__ == '__main__':
    main()