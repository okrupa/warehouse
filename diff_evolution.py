from numpy import asarray
from numpy.random import rand


class Tensor:
    def __init__(self, dimensions, position, order):
        self.dimensions = dimensions
        self.position = position
        self.order = order

    def isOverlapping(self, otherContainer):
        for i in range(self.order):
            minPosition = min(self.position[i], otherContainer.position[i])
            if minPosition == self.position[i]:
                if self.position[i] + self.dimensions[i] <= otherContainer.position[i]:
                    return False
            if minPosition == otherContainer.position[i]:
                if otherContainer.position[i] + otherContainer.dimensions[i] <= self.position[i]:
                    return False
        return True
        

def getBounds(storehouse):
    return asarray([(0, storehouse[i] - 1) for i in range(3)])


def differential_evolution(population_size, bounds, iter_number, f, cr):
    pop = bounds[:, 0] + (rand(population_size, len(bounds)) * (bounds[:, 1] - bounds[:, 0]))
    return pop


storehouse = [2, 5, 3]
containers = [[2, 1, 3], [1,1,1], [1,1,1], [1,1,2],[1,2,2], [2,3,1], [2,1,2], [3,1,1]]

POPULATION_SIZE = 20
ITER_NUMBER = 100
F = 0.5
CR = 0.7

bounds = getBounds(storehouse)
print(differential_evolution(POPULATION_SIZE, bounds, ITER_NUMBER, F, CR))