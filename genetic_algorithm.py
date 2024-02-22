import math
import random
import pickle
from simulated_annealing import objective_function, neighbour
#--- Constants
SOLUTION_SIZE = 48
DATA_FILE = "us_capitals.pkl"
POPULATION_SIZE = 50
VARIATION_TYPE = ""
MUTATION_RATE = 1/POPULATION_SIZE
CROSSOVER_N = 3

#--- Definitions

# Returns an array of fitnesses aligned to population of solutions
def calculate_fitness(population):
    fitnesses = []
    #fitnesses[0] = {'0': (0,0)}
    
    for solution in population:
        fitnesses.append(objective_function(solution))
    return fitnesses
    
# Generates a random candidate solution
def generate_random_solution(solution):

    shuffled_solution = {}
    
    # turn keys into a list
    keys = list(solution.keys())
    # shuffle keys
    random.shuffle(keys)

    for index, key in enumerate(keys, 1): # for each key, extract its value and append it to the dict
        shuffled_solution[index] = solution[key]
        
    return shuffled_solution

# Generates an initial solution population given a sample solution
def generate_population(solution):
    population = []
    for _ in range(POPULATION_SIZE):
        population.append(generate_random_solution(solution))
    return population

# Selects a subset of parents given their fitness values
def select_parents(population, fitnesses):
    return -1

# Applies the crossover variation operator
def crossover(parent1, parent2, n):
    parent1 = list(parent1.values())
    parent2 = list(parent2.values())
    point_list = []
    temp = []
    # generate n random points to perform crossover
    for _ in range(n):
        point_list.append(random.randint(0,SOLUTION_SIZE))
    # sort the list
    point_list.sort()
    print(point_list)
    # for each point, swap the rest of the arrays
    for point in point_list:
        point = int(point)
        temp = parent1[point:]
        parent1[point:] = parent2[point:]
        parent2[point:] = temp
    
    return parent1, parent2
# Applies the mutation variation operator
# swaps each location with a random location with probability P_m
def mutation(parents):
    for solution in parents:
        if random.uniform(0,1) < MUTATION_RATE:
            solution = neighbour(solution)
    return parents
    
# Generates new individuals by applying varation operators to parents
def generate_variations(parents):
    new_individuals = mutation(parents)
    new_individuals = crossover(new_individuals, CROSSOVER_N)
    return new_individuals

# 
def reproduce():
    return -1


def check_termination():
    return False

#--- Initialisations
with open(DATA_FILE, "rb") as file:
    solution = pickle.load(file)

population = generate_population(solution)

neighbour_solution = neighbour(solution)
print(solution)
print(neighbour_solution)
crossover_test1, crossover_test2 = crossover(solution, neighbour_solution, 3)
print(crossover_test1)
print(crossover_test2)
# for solution in population:
#     print(solution)
#     print("-----------------------------------")
    
termination_flag = False
t = 0
fitnesses = calculate_fitness(population)

# while not termination_flag:
#     #--- Selection
#     # Select parents from population basen on their fitness
#     parents = select_parents(population, fitnesses)
#     #--- Variation
#     # Breed new individuals by applying operators
#     new_individuals = generate_variations(parents)
#     #--- Fitness Calculation
#     # Evaluate fitness of new individuals
#     new_fitnesses = calculate_fitness(new_individuals)
#     #--- Reproduction
#     # Generate new populations by replacing least fit individuals
#     new_population = reproduce(population, fitnesses, new_individuals, new_fitnesses)
#     t +=1
#     termination_flag = check_termination()