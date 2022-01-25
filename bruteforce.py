
import numpy as np

def bruteforce(magasine, containers, current = 0, mag_points=None, num_fit=0):
    if current == len(containers):
        return num_fit, []
    if mag_points is None:
        mag_points = np.zeros(tuple(magasine))-1
    container = containers[current]
    max_fit = num_fit
    max_fit, positions = bruteforce(magasine, containers, current+1, mag_points, num_fit)
    positions.insert(0, None)

    rotations = 3
    best_rot = 0
    for rot in range(rotations):
        for i in range(magasine[0]):
            for j in range(magasine[1]):
                for k in range(magasine[2]):
                    if try_place(mag_points, container, (i,j,k), current):
                        fit, positions_now = bruteforce(magasine, containers, current+1, mag_points, num_fit+1)
                        if fit > max_fit:
                            max_fit = fit
                            positions = positions_now
                            positions.insert(0, [i,j,k])
                            best_rot = rot
                        unplace(mag_points, container, (i,j,k))
        rotate_in_place(container)

    for i in range(best_rot):
        rotate_in_place(container)

    rotate_2d(container)
    rotations = 3
    best_rot = 0
    for rot in range(rotations):
        for i in range(magasine[0]):
            for j in range(magasine[1]):
                for k in range(magasine[2]):
                    if try_place(mag_points, container, (i,j,k), current):
                        fit, positions_now = bruteforce(magasine, containers, current+1, mag_points, num_fit+1)
                        if fit > max_fit:
                            max_fit = fit
                            positions = positions_now
                            positions.insert(0, [i,j,k])
                            best_rot = rot
                        unplace(mag_points, container, (i,j,k))
        rotate_in_place(container)

    return max_fit, positions
                    
def rotate_in_place(container):
    x = container[0]
    container[0] = container[1]
    container[1] = container[2]
    container[2] = x

def rotate_2d(container):
    x = container[0]
    container[0] = container[1]
    container[1] = x

def try_place(mag_points: np.ndarray, container, coords, current):
    if mag_points.shape[0] < coords[0]+container[0] or \
        mag_points.shape[1] < coords[1]+container[1] or \
            mag_points.shape[2] < coords[2]+container[2]:
            return False

    for i in range(coords[0],coords[0]+container[0]):
        for j in range(coords[1],coords[1]+container[1]):
            for k in range(coords[2],coords[2]+container[2]):
                if mag_points[i,j,k] != -1:
                    return False
    for i in range(coords[0],coords[0]+container[0]):
        for j in range(coords[1],coords[1]+container[1]):
            for k in range(coords[2],coords[2]+container[2]):
                mag_points[i,j,k] = current
    return True

def unplace(mag_points, container, coords):
    for i in range(coords[0],coords[0]+container[0]):
        for j in range(coords[1],coords[1]+container[1]):
            for k in range(coords[2],coords[2]+container[2]):
                mag_points[i,j,k] = -1
mag_size = [5, 5, 5]
packages = [[5, 5, 5], [4, 4, 4], [3, 3, 3], [2,2,2], [1, 1, 1]]
output = bruteforce(mag_size, packages)
print(output)
print(packages)