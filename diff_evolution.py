from numpy import asarray
import random
from numpy import argmin
from numpy.random import choice


class Tensor:
    def __init__(self, dimensions, position, order):
        self.dimensions = dimensions
        self.position = position
        self.order = order

    def calculateOverlapping(self, otherContainer):
        overlappingDim = []
        for i in range(self.order):
            minPosition = min(self.position[i], otherContainer.position[i])
            if minPosition == self.position[i]:
                if self.position[i] + self.dimensions[i] <= otherContainer.position[i]:
                    overlappingDim.append(0)
                else:
                    overlappingDim.append(self.position[i] + self.dimensions[i] - otherContainer.position[i])
            elif minPosition == otherContainer.position[i]:
                if otherContainer.position[i] + otherContainer.dimensions[i] <= self.position[i]:
                    overlappingDim.append(0)
                else:
                    overlappingDim.append(otherContainer.position[i] + otherContainer.dimensions[i] - self.position[i])
        overlapping = 1
        for o in overlappingDim:
            overlapping *= o
        return overlapping
        

def getBounds(storehouse):
    return asarray([(0, storehouse[i] - 1) for i in range(3)])


def getPopulation(containers, bounds, population_size):
    pop = []
    for _ in range(population_size):
        individual = []
        for container in containers:
            position = [random.randint(bounds[i][0], bounds[i][1]) for i in range(3)]
            individual.append(Tensor(container, position, 3))
        pop.append(individual)
    return pop

def obj(individual):
    error = 0
    for i in range(len(individual)):
        for j in range(i+1, len(individual)):
            error += individual[i].calculateOverlapping(individual[j])
    return error


def mutate(candidates, individual, F):
    mutated_individual = []
    for i in range(len(candidates[0])):
        mutated_position = []
        for j in range(3):
            mutated_dim = candidates[0][i].position[j] + F * (candidates[1][i].position[j] - candidates[2][i].position[j])
            mutated_position.append(mutated_dim)
        mutated_individual.append(Tensor(individual[i].dimensions, mutated_position, 3))
    return mutated_individual


def roundPosition(individual):
    for tensor in individual:
        for i in range(3):
            tensor.position[i] = round(tensor.position[i])


def normalizeBounds(individual, bounds):
    for tensor in individual:
        for i in range(3):
            if tensor.position[i] < min(bounds[i]):
                tensor.position[i] = min(bounds[i])
            if tensor.position[i] > max(bounds[i]):
                tensor.position[i] = max(bounds[i])


def differential_evolution(population_size, bounds, iter_number, F, CR, containers):
    # Initialise population
    population = getPopulation(containers, bounds, population_size)
    # Evaluate initial population
    obj_all = [obj(individual) for individual in population]
    print(obj_all)
    # Find the best individual and best obj 
    best_individual = population[argmin(obj_all)]
    best_obj = min(obj_all)

    i = 0
    while i < iter_number and best_obj > 0:
        for j, individual in enumerate(population):
            # Choose 3 candidates
            candidates = [candidate for candidate in population if candidate != individual]
            a, b, c = random.sample(candidates, 3)
            # Mutation
            mutated_individual = mutate([a, b, c], individual, F)
            roundPosition(mutated_individual)
            normalizeBounds(mutated_individual, bounds)
            # Crossover
            # Evaluate individual
            obj_individual = obj(individual)
            obj_temp_individual = obj(mutated_individual)
            # Selection
            if obj_temp_individual < obj_individual:
                prev_pop = population.copy()
                population[j] = mutated_individual
        # Evaluate population
        obj_all = [obj(individual) for individual in population]
        best_individual = population[argmin(obj_all)]
        best_obj = min(obj_all)
        print(obj_all)
        print(f'Iteration: {i}: {best_obj}')
        i += 1
    
    return best_individual, best_obj == 0


storehouse = [2, 5, 3]
containers = [[2, 1, 3], [1,1,1], [1,1,1], [1,1,2],[1,2,2], [2,3,1], [2,1,2], [3,1,1]]

POPULATION_SIZE = 15
ITER_NUMBER = 1000
F = 0.5
CR = 0.7

bounds = getBounds(storehouse)
differential_evolution(POPULATION_SIZE, bounds, ITER_NUMBER, F, CR, containers)
