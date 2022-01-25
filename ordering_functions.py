import copy
from diff_evolution import Tensor
import diff_evolution as DE
import a_star


def orderContainers(containers, storehouse):
    print("Start: A*")
    start = a_star.get_list(containers)
    nodes = a_star.astar(start, containers, storehouse)
    print("Finish: A*")

    foundCorrectArrangement = False
    while not foundCorrectArrangement:
        max_volume = 0
        foundNode = False
        for node in nodes:
            if node.g > max_volume:
                #znalezeinie max ilości kontenerów dla pełnego wektora
                whole_arr_check = 0
                if "?" in node.position:
                    whole_arr_check = -1
                if whole_arr_check == 0:
                    max_volume = node.g
                    max_volume_node = node
                    foundNode = True
        if not foundNode:
            for node in nodes:
                if node.g > max_volume:
                    node.position = [0 if x == '?' else x for x in node.position]
                    max_volume = node.g
                    max_volume_node = node

        print("Start: DE")
        possibleArrangement, foundCorrectArrangement = runDE(max_volume_node.position, containers, storehouse)
        print("Finish iteration: DE")
        if not foundCorrectArrangement:
            nodes.remove(max_volume_node)
    #return pullDown(possibleArrangement, storehouse)
    return possibleArrangement


def runDE(containers_list, containers, storehouse):
    containersToOrder = []
    for i, symbol in enumerate(containers_list):
        if symbol == 1:
            containersToOrder.append(containers[i])
    
    POPULATION_SIZE = 50
    ITER_NUMBER = 500
    F = 0.5
    CR = 0.7
    P = 0.5
    ORDER = 3
    
    bounds = DE.getBounds(storehouse, ORDER)
    solution, cond = DE.differential_evolution(POPULATION_SIZE, bounds, ITER_NUMBER, F, CR, P, ORDER, containersToOrder, storehouse)

    return solution, cond


def pullDown(arrangement, storehouse):
    storehouseTensor = Tensor(storehouse, [0, 0, 0], 3)
    newArrangement = copy.deepcopy(arrangement)

    changedPosition = True
    while changedPosition:
        changedPosition = False
        for i, tensor in enumerate(newArrangement):
            temp_tensor = copy.deepcopy(tensor)
            overlapping = 0
            outsticking = 0
            while overlapping == 0 and outsticking == 0:
                temp_tensor.position[2] = temp_tensor.position[2] - 1
                for otherTensor in newArrangement:
                    if otherTensor != tensor:
                        overlapping += temp_tensor.calculateOverlapping(otherTensor)
                outsticking += temp_tensor.calculateOutsticking(storehouseTensor)
            temp_tensor.position[2] = temp_tensor.position[2] + 1
            if temp_tensor.position[2] != tensor.position[2]:
                changedPosition = True
            newArrangement[i] = temp_tensor
    return newArrangement
