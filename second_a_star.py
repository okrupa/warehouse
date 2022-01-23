class Node:
    def __init__(self, representation):
        self.representation = representation
        self.profit = 0
        self.heuristics = 0

        self.successors = []
        self.predecessor = None

    def sumProfitHeuristics(self):
        return self.profit + self.heuristics


class Tree:
    def __init__(self, node_dimensions):
        self.node_dimensions = node_dimensions

        root_representation = self.getRootRepresentation()
        self.root = Node(root_representation)

        full_representation = self.getFullRepresentation()
        self.full_node = Node(full_representation)

    def getRootRepresentation(self):
        return [[['?' for _ in range(self.node_dimensions[0])] for _ in range(self.node_dimensions[1])] for _ in range(self.node_dimensions[2])]

    def getFullRepresentation(self):
        return [[[1 for _ in range(self.node_dimensions[0])] for _ in range(self.node_dimensions[1])] for _ in range(self.node_dimensions[2])]
    
    def aStar(self, containers):
        open_list = []
        open_list.append(self.root)

        closed_list = []

        while(self.open_list):
            current_node = open_list[0]
            current_index = 0

            for index, item in enumerate(open_list):
            #BIERZEMY O NAJWIĘKSZEJ FUNKCJI F - CZYLI MAX =1
                if item.sumProfitHeuristics() > current_node.sumProfitHeuristics():
                    current_node = item
                    current_index = index
            open_list.pop(current_index)
            closed_list.append(current_node)

            #Przypadek - wszytskie kontenery możemy umieścić w magazynie - przerywamy
            if current_node.representation == self.full_node.representation:
                return True, current_node.representation # Return POSITIONS
            
            current_node.successors = self.generateSuccessors(current_node, containers)


def main():
    storehouse = [2, 5, 3]
    containers = [[2, 4, 3], [7, 4, 5], [2, 1, 3], [1,1,1], [1,1,1], [1,1,2],[1,2,2], [2,3,1], [2,2,2], [2,1,2], [3,1,1]]

    tree = Tree(storehouse)
    print(tree.root.representation)

if __name__ == "__main__":
    main()
