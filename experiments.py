import matplotlib.pyplot as plt
import numpy as np
import random

from ordering_functions import orderContainers


def visualize(arrangement, storehouse):
    ax = plt.figure().add_subplot(projection='3d')
    for tensor in arrangement:
        filled = np.zeros(storehouse)
        for x in range(tensor.position[0], tensor.position[0] + tensor.dimensions[0]):
            for y in range(tensor.position[1], tensor.position[1] + tensor.dimensions[1]):
                for z in range(tensor.position[2], tensor.position[2] + tensor.dimensions[2]):
                    filled[x][y][z] = True
        ax.voxels(filled)
    plt.show()

def main():
    random.seed(10)
    storehouse = [3, 4, 10]
    containers = [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2], [3, 3, 1], [1, 1, 1], [1, 1, 1]]

    arrangement = orderContainers(containers, storehouse)

    visualize(arrangement, storehouse)

main()