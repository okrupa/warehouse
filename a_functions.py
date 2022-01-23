storehouse = [10, 5, 5]
containers = [[2, 4, 3], [2, 4, 3], [7, 4, 5], [2, 1, 3], [2, 1, 3], [4, 1, 2], [7, 3, 5]]

def get_list(containers):
    containers_list = []
    for i in range(len(containers)):
        containers_list.append('?')
    return containers_list

def g(containers_list):
    g = 0
    for i in containers_list:
        if i ==1:
            g+=1

def h(containers_list, containers, storehouse):
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


list_cozostaje = [1, 0, 1, '?', '?',1, 0]

# num = h(list_cozostaje, containers, storehouse)
# print(num)

def get_neighbours(containers_list):
    undecided = []
    neighbours = []
    for i in range(len(containers_list)):
        if containers_list[i] == '?':
            undecided.append(i)
    for i in undecided:
        new_n = containers_list.copy()
        new_n[i]=1
        neighbours.append(new_n)
    return neighbours
# print(list_cozostaje)
# b = get_neighbours(list_cozostaje)
# print(b)
