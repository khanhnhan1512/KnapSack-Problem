import time
from test import *


class Item:
    """Our Item"""

    def __init__(self, weight, value, _class, pre_pos):
        self.weight = weight
        self.value = value
        self._class = _class
        self.pre_position = pre_pos
        self.new_position = pre_pos
        self.prio = self.value / self.weight


class Node:
    """A node demonstrayes a status of our bag"""

    def __init__(self, weight: float, value: int, classes: list, items: list[int]):
        self.total_weight = weight
        self.total_value = value
        self.total_class = classes
        self.total_item = items


class Branch_Bound:
    """The resolution"""

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.get_input()
        # after having a list of items, we sort them by their "prio" value
        self.list_item.sort(key=lambda x: x.prio, reverse=True)
        # Save the new index after sorting
        for i in range(len(self.list_item)):
            self.list_item[i].new_position = i
        # Initialize our result
        self.node_result = Node(0, 0, [], [])

    def get_input(self):
        """Read the data from input file and turn them to item list"""
        with open(self.file_name) as file_object:
            self.capacity = float(file_object.readline().rstrip())
            self.number_class = int(file_object.readline().rstrip())
            list_weight = list(
                map(float, file_object.readline().rstrip().split(',')))
            list_value = list(
                map(int, file_object.readline().rstrip().split(',')))
            list_class = list(
                map(int, file_object.readline().rstrip().split(',')))
        # Create a list of item after getting their weight, value, class
        self.list_item = [Item(list_weight[i], list_value[i], list_class[i], i)
                          for i in range(len(list_weight))]

    def solve(self):
        """Calculating and return the result"""
        stack = [Node(0, 0, [], [])]
        while stack:
            current_node = stack.pop(0)
            i = len(current_node.total_item)
            # check if the current node is a leaf
            if i == len(self.list_item):
                if len(set(current_node.total_class)) == self.number_class:
                    if current_node.total_value > self.node_result.total_value:
                        # Update out result
                        self.node_result = current_node
            else:
                item = self.list_item[i]
                new_class = current_node.total_class.copy()
                # A child node for not picking the i'th item
                NotAddItem = Node(current_node.total_weight,
                                  current_node.total_value,
                                  new_class,
                                  current_node.total_item + [0])
                # A child node for picking the i'th item
                AddItem = Node(current_node.total_weight + item.weight,
                               current_node.total_value + item.value,
                               new_class + [item._class],
                               current_node.total_item + [1])
                if self.isPromissing(NotAddItem):
                    stack.insert(0, NotAddItem)
                if self.isPromissing(AddItem):
                    stack.insert(0, AddItem)

        return self.node_result

    def isPromissing(self, node: Node):
        """Check if we prunch or not prunch a node"""
        return node.total_weight <= self.capacity and self.getBound(node) > self.node_result.total_value and self.Check_Class(node)

    def getBound(self, node: Node):
        """Calculate the "possible value" we can get if travel this branch"""
        remainingWeight = self.capacity - node.total_weight
        bound = node.total_value

        for i in range(len(node.total_item), len(self.list_item)):
            item = self.list_item[i]
            if remainingWeight >= item.weight:
                remainingWeight -= item.weight
                bound += item.value
            else:
                bound += item.prio * remainingWeight
                break
        return bound

    def Check_Class(self, node: Node):
        """Check if we can have full of classes if we travel this branch
        Return True if we can, else return False"""
        remaining_weight = self.capacity - node.total_weight
        temp_class = node.total_class.copy()

        for i in range(len(node.total_item), len(self.list_item)):
            item = self.list_item[i]
            temp_class += [item._class]
            if remaining_weight >= item.weight:
                remaining_weight -= item.weight
            else:
                break
        return (len(set(temp_class)) == self.number_class)

    def Write_Result(self, file_name):
        """Write our result for this test case to the output file"""
        self.list_item.sort(key=lambda x: x.pre_position)
        answer_items = []
        # traceback our item, because after sorting, our items are messed up
        # So we need to get them to their previous positions
        for i in range(len(self.list_item)):
            answer_items.append(
                self.node_result.total_item[self.list_item[i].new_position])
        # Finally, write the result to the output file
        with open(file_name, 'w') as file_object:
            file_object.write(str(self.node_result.total_value) + '\n')
            for index, item in enumerate(answer_items):
                if index == 0:
                    file_object.write(str(item))
                else:
                    file_object.write(', ' + str(item))


if __name__ == '__main__':
    algo = Branch_Bound(f'input/INPUT_10.txt')
    start_time = time.time()
    result = algo.solve()
    end_time = time.time()
    print(result.total_value)
    running_time = end_time - start_time
    print(f"Running time (ms): {running_time*1000} ms")

    algo.Write_Result(f'OUTPUT_10.txt')
