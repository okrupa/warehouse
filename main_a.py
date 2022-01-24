import random

import diff_evolution as DE

import matplotlib.pyplot as plt
import numpy as np

from diff_evolution import Tensor

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self,  position=None):
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0


def runDE(containers_list, containers, storehouse):
    containersToOrder = []
    for i, symbol in enumerate(containers_list):
        if symbol == 1:
            containersToOrder.append(containers[i])
    
    POPULATION_SIZE = 25
    ITER_NUMBER = 50
    F = 0.5
    CR = 0.7
    P = 0.5
    ORDER = 3
    
    bounds = DE.getBounds(storehouse, ORDER)
    solution, cond = DE.differential_evolution(POPULATION_SIZE, bounds, ITER_NUMBER, F, CR, P, ORDER, containersToOrder, storehouse)

    return cond


def runHeuristics(containers_list, containers, storehouse):
    storehouse_volume = storehouse[0]*storehouse[1]*storehouse[2]
    actual_volume = 0
    c_volume = []
    for i in containers:
        c_volume.append(i[0]*i[1]*i[2])

    for i in range(len(containers_list)):
        if containers_list[i] == 1:
            con_vol = c_volume[i]
            actual_volume += con_vol
    if storehouse_volume < actual_volume:
        return False
    return True


def get_neighbours(containers_list):
    # obliczenie sąsiadów dla punktu
    undecided = []
    neighbours = []
    for i in range(len(containers_list)):
        if containers_list[i] == '?':
            undecided.append(i)
    for i in undecided:
        new_n = containers_list.copy()
        new_n[i]=1
        new_neighbour = Node(new_n)
        neighbours.append([new_neighbour, i])
    return neighbours


def g(containers_list):
    # f zysku
    g = 0
    for i in containers_list:
        if i ==1:
            g+=1
    return g


def h(containers_list, containers, storehouse):
    # f heurystyczna
    storehouse_volume = storehouse[0]*storehouse[1]*storehouse[2]
    
    c_volume = []
    for i in containers:
        c_volume.append(i[0]*i[1]*i[2])

    c_left_volume = c_volume.copy()
    actual_volume = 0

    num_containers = 0
    deleted = 0
    for i in range(len(containers_list)):
        if containers_list[i] == 1:
            c_left_volume.pop(i-deleted)
            deleted +=1
            con_vol = c_volume[i]
            actual_volume += con_vol

    while True:
        if c_left_volume:
            min_value = min(c_left_volume)
            value_after = storehouse_volume - actual_volume - min_value
            if value_after >= 0:
                min_index = c_left_volume.index(min_value)
                c_left_volume.pop((min_index))
                num_containers += 1
                actual_volume += min_value
            else:
                break
        else:
            break
    return num_containers


def astar( start, end,  containers, storehouse, f_limits):

    first_node = Node( start)
    all_c_node = Node( end)

    open_list = []
    closed_list = []

    open_list.append(first_node)

    i = 0
    while len(open_list) > 0:
        print(i)
        i += 1
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            #BIERZEMY O NAJWIĘKSZEJ FUNKCJI F - CZYLI MAX =1
            if item.f > current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        #Przypadek - wszytskie kontenery możemy umieścić w magazynie - przerywamy
        if current_node.position == all_c_node.position:
            return current_node.position # Return POSITIONS

        neighbours = get_neighbours(current_node.position)

        for neighbour_with_index in neighbours:
            add = True
            neighbour = neighbour_with_index[0]

            # wektor był juz sprawdzony - closed_list
            for closed_n in closed_list:
                if neighbour.position == closed_n.position:
                    add = False

            # wektor juz istnieje w wektorach czekających na sprawdzenie - open_list
            for open_n in open_list:
                if neighbour.position == open_n.position:
                    add = False
            if add:
                # Create the f, g, and h values
                neighbour.g = g(neighbour.position)
                neighbour.h = h(neighbour.position, containers, storehouse)
                neighbour.f = neighbour.g + neighbour.h

                
                # Child cannot exist - put DE algorithm
                possible_arrangement = f_limits(neighbour.position, containers, storehouse)
                if not possible_arrangement:
                    neighbour.position[neighbour_with_index[1]] = 0
                    neighbour.g = g(neighbour.position)
                    neighbour.h = h(neighbour.position, containers, storehouse)
                    neighbour.f = neighbour.g + neighbour.h

                    #sprawdzenie po zmianie wektora 
                    for open_n in open_list:
                        if neighbour.position == open_n.position:
                            add = False
                if add:
                    open_list.append(neighbour)
    max_volume = 0
    max_volume_position = start
    # for i in range(len(closed_list)):
    #     print(f"{i} - {closed_list[i].position} ,g- {closed_list[i].g}, h -{closed_list[i].h}, f-{closed_list[i].f}")
    for node in closed_list:
        if node.g > max_volume:
            #znalezeinie max ilości kontenerów dla pełnego wektora
            whole_arr_check = 0
            if "?" in node.position:
                whole_arr_check = -1
            if whole_arr_check == 0:
                max_volume = node.g
                max_volume_position = node.position
    return max_volume_position


def get_list(containers):
    containers_list = []
    for i in range(len(containers)):
        containers_list.append('?')
    return containers_list

def get_list_end(containers):
    containers_list = []
    for i in range(len(containers)):
        containers_list.append(1)
    return containers_list

def main():

    storehouse = [5, 5, 5]
    # storehouse = [10,10,10]
    containers = [[2, 4, 3], [7, 4, 5], [2, 1, 3], [1, 1, 1]]
    
    start = get_list(containers)
    end = get_list_end(containers)

    path = astar( start, end, containers, storehouse, runHeuristics)
    print(path)

    c_volume = []
    for i in containers:
        c_volume.append(i[0]*i[1]*i[2])
    print(c_volume)

    containersToShow = []
    for i, symbol in enumerate(path):
        if symbol == 1:
            containersToShow.append(containers[i])

    POPULATION_SIZE = 50
    ITER_NUMBER = 200
    F = 0.5
    CR = 0.7
    P = 0.5
    ORDER = 3
    
    bounds = DE.getBounds(storehouse, ORDER)
    solution, cond = DE.differential_evolution(POPULATION_SIZE, bounds, ITER_NUMBER, F, CR, P, ORDER, containersToShow, storehouse)

    if cond:
        ax = plt.figure().add_subplot(projection='3d')
        for tensor in solution:
            filled = np.zeros((5, 5, 5))
            for x in range(tensor.position[0], tensor.position[0] + tensor.dimensions[0]):
                for y in range(tensor.position[1], tensor.position[1] + tensor.dimensions[1]):
                    for z in range(tensor.position[2], tensor.position[2] + tensor.dimensions[2]):
                        filled[x][y][z] = True
            ax.voxels(filled)
        plt.show()
    else:
        for i in range(len(solution)):
            temp_solution = solution.copy()
            temp_solution.remove(solution[i])
            containersToShow = [ind.dimensions for ind in temp_solution]
            new_solution, cond = DE.differential_evolution(POPULATION_SIZE, bounds, ITER_NUMBER, F, CR, P, ORDER, containersToShow, storehouse)
            if cond:
                ax = plt.figure().add_subplot(projection='3d')
                for tensor in new_solution:
                    filled = np.zeros((5, 5, 5))
                    for x in range(tensor.position[0], tensor.position[0] + tensor.dimensions[0]):
                        for y in range(tensor.position[1], tensor.position[1] + tensor.dimensions[1]):
                            for z in range(tensor.position[2], tensor.position[2] + tensor.dimensions[2]):
                                filled[x][y][z] = True
                    ax.voxels(filled)
                plt.show()
                break

if __name__ == '__main__':
    main()