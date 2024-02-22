import math
import random
import pickle
from simulated_annealing import objective_function
#--- Constants
SOLUTION_SIZE = 48
DATA_FILE = "us_capitals.pkl"
POPULATION_SIZE = 50

#--- Definitions

# Returns an array of fitnesses aligned to population of solutions
def calculate_fitness(population):
    fitnesses = []
    fitnesses[0] = {'0': (0,0)}
    
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

# Generates new individuals by applying varation operators to parents
def generate_variations(parents):
    return -1

# 
def reproduce():
    return -1
    
def check_termination():
    return False

#--- Initialisations
with open(DATA_FILE, "rb") as file:
    solution = pickle.load(file)

population = generate_population(solution)
print(solution)
for solution in population:
    print(solution)
    print("-----------------------------------")
# termination_flag = False
# t = 0
# fitnesses = calculate_fitness(population)

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