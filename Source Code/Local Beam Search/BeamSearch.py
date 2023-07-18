import random
from test import *
import time


class Beam_Search:
    """The resolution of KnapSack problem by using Local Beam Search"""

    def __init__(self, file_name):
        self.file_name = file_name
        self.k = 300  # Beam Width
        # the maximum loop we wait to find a new state that be better than current state
        self.max_loop = 1200
        self.Get_Data()
        self.n = len(self.list_value)  # Number of items
        self.Initialize_Nodes()

    def Get_Data(self):
        """Read the data from input file"""
        with open(self.file_name) as file_object:
            self.capacity = float(file_object.readline().rstrip())
            self.number_class = int(file_object.readline().rstrip())
            self.list_weight = list(
                map(float, file_object.readline().rstrip().split(',')))
            self.list_value = list(
                map(int, file_object.readline().rstrip().split(',')))
            self.list_class = list(
                map(int, file_object.readline().rstrip().split(',')))

    def Heuristic(self, node):
        """Calculating the heuristic value for the state"""
        node_weight = 0
        node_value = 0
        node_classes = [0]*self.number_class
        for i in range(self.n):
            if node[i] == 1:
                node_weight += self.list_weight[i]
                node_value += self.list_value[i]
                node_classes[self.list_class[i] - 1] += 1
        if node_weight > self.capacity or not all(c > 0 for c in node_classes):
            # if state's weight is greater than capacity or it contains not enough class, its heuristic is -1
            return -1
        else:
            # else, its heuristic is its value
            return node_value

    def Create_Successors(self, node):
        """Creating "beam width" successor states from the current state"""
        successors_list = []
        for i in range(self.n):
            successor = node.copy()
            successor[i] = 1 - successor[i]
            successors_list.append(successor)
        return successors_list

    def Initialize_Nodes(self):
        """Firstly, creating the first states to repair for the beam search"""
        self.current_nodes = []
        y_n = [0, 1]
        for _ in range(self.k):
            node = [random.choice(y_n) for _ in range(self.n)]
            self.current_nodes.append(node)

    def solve(self):
        loop_times = 0
        best_node = max(self.current_nodes, key=self.Heuristic)
        best_value = self.Heuristic(best_node)
        while loop_times < self.max_loop:
            loop_times += 1
            next_nodes = []
            for node in self.current_nodes:
                # Creating successor states from current states
                next_nodes.extend(self.Create_Successors(node))
            # Choosing "beam width" states that have highest heuristic values
            self.current_nodes = sorted(
                next_nodes, key=self.Heuristic, reverse=True)[:self.k]
            # Take best state from the best states to compare with current state
            best_current_node = max(self.current_nodes, key=self.Heuristic)
            if self.Heuristic(best_current_node) > best_value:
                # if our current state is updated, reset the "loop_time" to 0
                best_value = self.Heuristic(best_current_node)
                best_node = best_current_node
                loop_times = 0

        return best_node, best_value

    def Write_Result(self, file_name):
        """Write the result to output file"""
        start = time.time()
        result = self.solve()
        end = time.time()
        running_time = end - start
        print(f"Running time: {running_time*1000} ms")
        with open(file_name, 'w') as file_object:
            file_object.write(str(result[1]) + '\n')
            for i in range(len(result[0])):
                if i == 0:
                    file_object.write(str(result[0][0]))
                else:
                    file_object.write(', ' + str(result[0][i]))


if __name__ == '__main__':
    algo = Beam_Search('input/INPUT_8.txt')
    algo.Write_Result('output/OUTPUT_8.txt')
