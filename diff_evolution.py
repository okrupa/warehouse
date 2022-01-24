from matplotlib.container import Container
from numpy import asarray
import random
from numpy import argmin


import matplotlib.pyplot as plt
import numpy as np


class Tensor:
    def __init__(self, dimensions, position, order):
        self.dimensions = dimensions
        self.position = position
        self.order = order

    def calculateOverlapping(self, otherContainer):
        overlappingDim = []
        for i in range(self.order):
            wp = max(self.position[i], otherContainer.position[i])
            wk = min(self.position[i] + self.dimensions[i], otherContainer.position[i] + otherContainer.dimensions[i])
            overlapping = wk - wp if wk - wp > 0 else 0
            overlappingDim.append(overlapping)
        overlapping = 1
        for o in overlappingDim:
            overlapping *= o
        return overlapping
    

    def calculateOutsticking(self, otherContainer):
        overlapping = self.calculateOverlapping(otherContainer)
        V = 1
        for dim in self.dimensions:
            V *= dim
        return V - overlapping

    def permutateDimensions(self):
        rot_idx = random.sample([i for i in range(self.order)], 2)
        self.dimensions[rot_idx[0]], self.dimensions[rot_idx[1]] = self.dimensions[rot_idx[1]], self.dimensions[rot_idx[0]]
        

def getBounds(storehouse, ORDER):
    return asarray([(0, storehouse[i] - 1) for i in range(ORDER)])


def getPopulation(containers, bounds, population_size, ORDER):
    pop = []
    for _ in range(population_size):
        individual = []
        for container in containers:
            position = [random.randint(bounds[i][0], bounds[i][1]) for i in range(ORDER)]
            individual.append(Tensor(container, position, 3))
        pop.append(individual)
    return pop

def obj(individual, storehouse):
    error = 0
    for i in range(len(individual)):
        for j in range(i+1, len(individual)):
            error += individual[i].calculateOverlapping(individual[j])
        error += individual[i].calculateOutsticking(storehouse)
    return error


def mutate(candidates, individual, F, P, ORDER):
    mutated_individual = []
    for i in range(len(candidates[0])):
        mutated_position = []
        for j in range(ORDER):
            mutated_dim = candidates[0][i].position[j] + F * (candidates[1][i].position[j] - candidates[2][i].position[j])
            mutated_position.append(mutated_dim)
        mutated_tensor = Tensor(individual[i].dimensions, mutated_position, 3)
        mutated_individual.append(mutated_tensor)

        # Mutate dimensions permutation
        if random.random() < P:
            mutated_tensor.permutateDimensions()

    return mutated_individual


def roundPosition(individual, ORDER):
    for tensor in individual:
        for i in range(ORDER):
            tensor.position[i] = round(tensor.position[i])


def normalizeBounds(individual, bounds, ORDER):
    for tensor in individual:
        for i in range(ORDER):
            if tensor.position[i] < min(bounds[i]):
                tensor.position[i] = min(bounds[i])
            if tensor.position[i] > max(bounds[i]):
                tensor.position[i] = max(bounds[i])

def crossover(mutated_individual, individual, CR):
    crossover_individual = []
    for mutated_tensor, tensor in zip(mutated_individual, individual):
        crossover_tensor = mutated_tensor if random.random() < CR else tensor
        crossover_individual.append(crossover_tensor)
    return crossover_individual


def differential_evolution(population_size, bounds, iter_number, F, CR, P, ORDER, containers, storehouse):
    storehouse = Tensor(storehouse, [0, 0, 0], 3)
    # Initialise population
    population = getPopulation(containers, bounds, population_size, ORDER)
    # Evaluate initial population
    obj_all = [obj(individual, storehouse) for individual in population]
    best_individual = population[argmin(obj_all)]
    best_obj = min(obj_all)

    i = 0
    while i < iter_number and best_obj > 0:
        for j, individual in enumerate(population):
            # Choose 3 candidates
            candidates = [candidate for candidate in population if candidate != individual]
            candidates = random.sample(candidates, 3)
            # Mutation
            mutated_individual = mutate(candidates, individual, F, P, ORDER)
            roundPosition(mutated_individual, ORDER)
            normalizeBounds(mutated_individual, bounds, ORDER)
            # Crossover
            crossover_individual = crossover(mutated_individual, individual, CR)
            # Evaluate individual
            obj_individual = obj(individual, storehouse)
            #obj_temp_individual = obj(mutated_individual, storehouse)
            obj_temp_individual = obj(crossover_individual, storehouse)
            # Selection
            if obj_temp_individual < obj_individual:
                population[j] = crossover_individual
        # Evaluate population
        obj_all = [obj(individual, storehouse) for individual in population]
        best_individual = population[argmin(obj_all)]
        best_obj = min(obj_all)
        i += 1
    
    return best_individual, best_obj == 0


def main():
    storehouse = [2, 5, 3]
    containers = [[1,1,1], [1,1,1], [1,1,2],[1,2,2], [2,3,1], [2,2,2], [2,1,2]]

    POPULATION_SIZE = 150
    ITER_NUMBER = 1000
    F = 0.5
    CR = 0.7
    P = 0.5
    ORDER = 3

    bounds = getBounds(storehouse, ORDER)
    solution, cond = differential_evolution(POPULATION_SIZE, bounds, ITER_NUMBER, F, CR, P, ORDER, containers, storehouse)

    print(cond)
    for tensor in solution:
        print(f'{tensor.position}   {tensor.dimensions}')
        

    ax = plt.figure().add_subplot(projection='3d')
    for tensor in solution:
        filled = np.zeros((2, 5, 3))
        for x in range(tensor.position[0], tensor.position[0] + tensor.dimensions[0]):
            for y in range(tensor.position[1], tensor.position[1] + tensor.dimensions[1]):
                for z in range(tensor.position[2], tensor.position[2] + tensor.dimensions[2]):
                    filled[x][y][z] = True
        ax.voxels(filled)
    
    
    plt.show()

if __name__ == "__main__":
    main()
