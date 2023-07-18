import itertools
import tracemalloc

class Brute_Force:
    def __init__(self,file_name):
        self.file_name = file_name
        self.get_Data()


    def get_Data(self):
        with open(self.file_name) as file:
            self.capacity = float(file.readline().rstrip())
            self.number_class = int(file.readline().rstrip())

            self.weights = list(map(float, file.readline().rstrip().split(',')))
            self.profits = list(map(int, file.readline().rstrip().split(',')))
            self.classes = list(map(int, file.readline().rstrip().split(',')))

    def solve(self):
        # max value
        max_val = 0

        # best combination
        best_comb = [] 

        # number of items
        n = len(self.weights)

        # use intertools.product to create every combination
        for combination in itertools.product(range(2), repeat=n): 

            w = sum(combination[i]*self.weights[i] for i in range(n))

            # check if the current weight is bigger than the capacity or not
            if w <= self.capacity: 
                combination_value = sum(combination[i]*self.profits[i] for i in range(n))
                
                if combination_value > max_val:
                    # list to check whether we have enough class
                    class_check = [0 for i in range(self.number_class)] 
                    
                    # check if the current value is bigger than the max value or not
                    for i in range(n): 
                        if combination[i] == 1:
                            class_check[self.classes[i] - 1] = 1
                    
                    if all(class_check[y]==1 for y in range(self.number_class)):
                        max_val = combination_value
                        best_comb = combination
                        
        return best_comb, max_val
    
    def Write_Result(self, file_name, result):
        with open(file_name, 'w') as file_object:
            file_object.write(str(result[1]) + '\n')
            for i in range(len(result[0])):
                if i == 0:
                    file_object.write(str(result[0][0]))
                else:
                    file_object.write(', ' + str(result[0][i]))

        
from time import time

# Driver Code
if __name__ == '__main__':
    
    algo = Brute_Force('INPUT_2.txt')

    start = time()
    result = algo.solve()# solve here
    end = time()
    print("Time :", (end - start)*1000, "ms")

    algo.Write_Result('OUTPUT_2.txt',result) 

    

   

