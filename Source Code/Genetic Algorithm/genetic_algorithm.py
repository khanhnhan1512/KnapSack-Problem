import random
import time


class Item:
    def __init__(self, weight: float, value: int, color: int):
        self.weight = weight
        self.value = value
        self.color = color
        self.optimal_point = value / weight


class Knapsack:
    def __init__(self, max_weight: float, num_class: int):
        self.max_weight = max_weight
        self.num_class = num_class


LIST_POINT = []
SUGGEST_TAKEN_RATE = 0.5


class Individual:
    def __init__(self, knapsack: Knapsack, item_list: list):
        self.chromosome = [0] * len(item_list)
        self.total_weight = 0

        global LIST_POINT
        for i in range(len(item_list)):
            LIST_POINT.append(item_list[i].optimal_point)
        LIST_POINT.sort()
        median_point = LIST_POINT[round(len(LIST_POINT) / 2)]

        total_value = 0
        class_mask = [False] * knapsack.num_class
        for i in range(len(item_list)):
            coefficient = 1.0
            if 0 < SUGGEST_TAKEN_RATE <= 0.3:
                coefficient = 3
            elif 0.3 <= SUGGEST_TAKEN_RATE < 0.45:
                coefficient = 2
            elif 0.45 <= SUGGEST_TAKEN_RATE <= 0.65:
                coefficient = 1.5

            # if optimal point is good -> high rate
            # else optimal point is low -> low rate
            if item_list[i].optimal_point > median_point:
                rate = SUGGEST_TAKEN_RATE * coefficient
            else:
                rate = SUGGEST_TAKEN_RATE * (1 / coefficient)

            if random.random() < rate:
                self.chromosome[i] = 1
                self.total_weight += item_list[i].weight
                total_value += item_list[i].value
                class_mask[item_list[i].color - 1] = True

        self.fitness = total_value if self.total_weight <= knapsack.max_weight else 0

        for bit in class_mask:
            if not bit:
                self.fitness = 0

    def update(self, chromosome: list, knapsack: Knapsack, item_list: list):
        self.chromosome = chromosome
        self.total_weight = 0
        total_value = 0
        class_mask = [False] * knapsack.num_class

        for i in range(len(chromosome)):
            if self.chromosome[i] == 1:
                self.total_weight += item_list[i].weight
                total_value += item_list[i].value
                class_mask[item_list[i].color - 1] = True

        self.fitness = total_value if self.total_weight <= knapsack.max_weight else 0

        for bit in class_mask:
            if not bit:
                self.fitness = 0


class Population:
    def __init__(self, pop_size: int, knapsack: Knapsack, item_list: list):
        self.size = pop_size
        self.population = []
        for i in range(pop_size):
            self.population.append(Individual(knapsack, item_list))

    def get(self) -> list:
        return self.population


class Elitism:
    def __init__(self, rate: float):
        self.rate = rate

    def apply(self, population: list) -> list:
        new_pop = []
        population.sort(key=lambda x: x.fitness, reverse=True)

        new_pop = population[-int(self.rate * len(population)) : -1]
        origin_pop_idx = 0
        new_pop_idx = 0
        while origin_pop_idx < len(population):
            is_dup = False
            for b4 in range(new_pop_idx):
                if population[origin_pop_idx].chromosome == population[b4].chromosome:
                    is_dup = True
                    break
            if not is_dup and new_pop_idx < len(new_pop):
                new_pop[new_pop_idx] = population[origin_pop_idx]
                new_pop_idx += 1
            origin_pop_idx += 1

        return new_pop


class Crossover:
    def __init__(self):
        pass

    def apply(self, mom_chromosome: list, dad_chromosome: list) -> list:
        child_chromosome = []
        cross_point = random.randint(0, len(mom_chromosome) - 1)

        if random.random() < 0.5:
            child_chromosome = mom_chromosome[:cross_point] + dad_chromosome[cross_point:]
        else:
            child_chromosome = dad_chromosome[:cross_point] + mom_chromosome[cross_point:]

        return child_chromosome


class Mutation:
    def __init__(self, mutation_rate: float):
        self.rate = mutation_rate

    def apply(self, chromosome: list):
        for gene in chromosome:
            if random.random() < self.rate:
                gene = 1 - gene


class Nature:
    def __init__(self, elitism: Elitism, crossover: Crossover, mutation: Mutation):
        self.elitism = elitism
        self.crossover = crossover
        self.mutation = mutation

    def select(self, population: list, knapsack: Knapsack, item_list: list) -> list:
        # return a better population with the size equal to the given one
        new_pop = self.elitism.apply(population)

        while len(new_pop) < len(population):
            child = Individual(knapsack, item_list)

            m = random.randint(0, len(new_pop) - 1)
            d = random.randint(0, len(new_pop) - 1)

            mom = new_pop[m]
            dad = new_pop[d]
            child_chromo = self.crossover.apply(mom.chromosome, dad.chromosome)

            self.mutation.apply(child_chromo)

            child.update(child_chromo, knapsack, item_list)

            new_pop.append(child)

        return new_pop


class GeneticAlgo:
    def __init__(self, generation: int, pop_size: int, nature: Nature):
        self.generation = generation
        self.pop_size = pop_size
        self.nature = nature

    def solve(self, knapsack: Knapsack, item_list: list) -> Individual:
        population = Population(self.pop_size, knapsack, item_list).get()

        for i in range(self.generation):
            print(f"gen {i}")
            population = self.nature.select(population, knapsack, item_list)

        population.sort(key=lambda x: x.fitness, reverse=True)

        return population[0]


if __name__ == '__main__':
    elitism = Elitism(0.3)
    crossover = Crossover()
    mutation = Mutation(0.01)
    nature = Nature(elitism, crossover, mutation)
    algo = GeneticAlgo(20, 20, nature)

    # get input
    seq = 1

    input_filename = f"input/INPUT_{seq}.txt"
    output_filename = f"output/OUTPUT_{seq}.txt"

    # get items from a file and create Item objects using the file
    item_list = []
    with open(input_filename, 'r') as f:
        max_weight = float(f.readline().strip())
        number_class = int(f.readline().strip())
        weights = list(map(float, f.readline().strip().split(',')))
        values = list(map(int, f.readline().strip().split(',')))
        classes = list(map(int, f.readline().strip().split(',')))

        for i in range(0, len(weights)):
            new_item = Item(float(weights[i]), int(values[i]), int(classes[i]))
            item_list.append(new_item)

    knapsack = Knapsack(max_weight, number_class)

    # solve
    start = time.time()

    total_weight = 0
    for item in item_list:
        total_weight += item.weight

    SUGGEST_TAKEN_RATE = knapsack.max_weight / total_weight

    solution = algo.solve(knapsack, item_list)

    end = time.time()

    # print outputs
    print(solution.chromosome)
    print(f"number of items = {len(solution.chromosome)}")
    print(f"time = {(end - start) * 1000} ms")
    print(f"value = {solution.fitness}")
    print(f"weight = {solution.total_weight}")
    print(f"(knapsack's max weight) / (all items' weight) = {SUGGEST_TAKEN_RATE}")
    print(f"median of value/weight ratio = {LIST_POINT[round(len(LIST_POINT) / 2)]}")

    # write to output files
    with open(output_filename, 'w') as f:
        f.write(str(solution.fitness) + '\n')
        f.write(str(solution.chromosome))