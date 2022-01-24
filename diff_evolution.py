from matplotlib.container import Container
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
        self.dimensions[0], self.dimensions[1], self.dimensions[2] = self.dimensions[1], self.dimensions[2], self.dimensions[0]
        return
        

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

def obj(individual, storehouse):
    error = 0
    for i in range(len(individual)):
        for j in range(i+1, len(individual)):
            error += individual[i].calculateOverlapping(individual[j])
        error += individual[i].calculateOutsticking(storehouse)
    return error


def mutate(candidates, individual, F, p):
    mutated_individual = []
    for i in range(len(candidates[0])):
        mutated_position = []
        for j in range(3):
            mutated_dim = candidates[0][i].position[j] + F * (candidates[1][i].position[j] - candidates[2][i].position[j])
            mutated_position.append(mutated_dim)
        mutated_tensor = Tensor(individual[i].dimensions, mutated_position, 3)
        mutated_individual.append(mutated_tensor)

        # Mutate dimensions permutation
        if random.random() < p:
            mutated_tensor.permutateDimensions()

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

def crossover(mutated_individual, individual, CR):
    crossover_individual = []
    for mutated_tensor, tensor in zip(mutated_individual, individual):
        crossover_tensor = mutated_tensor if random.random() < CR else tensor
        crossover_individual.append(crossover_tensor)
    return crossover_individual


def differential_evolution(population_size, bounds, iter_number, F, CR, p, containers, storehouse):
    storehouse = Tensor(storehouse, [0, 0, 0], 3)
    # Initialise population
    population = getPopulation(containers, bounds, population_size)
    # Evaluate initial population
    obj_all = [obj(individual, storehouse) for individual in population]
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
            mutated_individual = mutate([a, b, c], individual, F, p)
            roundPosition(mutated_individual)
            normalizeBounds(mutated_individual, bounds)
            # Crossover
            crossover_individual = crossover(mutated_individual, individual, CR)
            # Evaluate individual
            obj_individual = obj(individual, storehouse)
            #obj_temp_individual = obj(mutated_individual, storehouse)
            obj_temp_individual = obj(crossover_individual, storehouse)
            # Selection
            if obj_temp_individual < obj_individual:
                #population[j] = mutated_individual
                population[j] = crossover_individual
        # Evaluate population
        obj_all = [obj(individual, storehouse) for individual in population]
        best_individual = population[argmin(obj_all)]
        best_obj = min(obj_all)
        print(obj_all)
        print(f'Iteration: {i}: {best_obj}')
        i += 1
    
    return best_individual, best_obj == 0


storehouse = [2, 5, 3]
containers = [[2, 1, 3], [1,1,1], [1,1,1], [1,1,2],[1,2,2], [3,1,1]]

POPULATION_SIZE = 15
ITER_NUMBER = 1000
F = 0.5
CR = 0.7
p = 0.2

bounds = getBounds(storehouse)
differential_evolution(POPULATION_SIZE, bounds, ITER_NUMBER, F, CR, p, containers, storehouse)

storehouseT = Tensor([2, 5, 3], [0, 0, 0], 3)
container = Tensor([1, 1, 1], [0, 2, 1], 3)
#print(container.calculateOutsticking(storehouseT))
#print(storehouseT.calculateOutsticking(container))