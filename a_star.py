class Node():
    """A node class for A* Pathfinding"""

    def __init__(self,  position=None):
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0


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


def astar(start, containers, storehouse):

    first_node = Node( start)

    open_list = []
    closed_list = []

    open_list.append(first_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            #BIERZEMY O NAJWIĘKSZEJ FUNKCJI F - CZYLI MAX =1
            if item.f > current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

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

                
                # Child cannot exist - put heuristic algorithm
                possible_arrangement = runHeuristics(neighbour.position, containers, storehouse)
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

    return closed_list


def get_list(containers):
    containers_list = []
    for i in range(len(containers)):
        containers_list.append('?')
    return containers_list
