import math
import random
import pickle
from simulated_annealing import objective_function, neighbour
#--- Constants
SOLUTION_SIZE = 48
DATA_FILE = "us_capitals.pkl"
POPULATION_SIZE = 50

# Variation
MUTATION_RATE = 1/POPULATION_SIZE
CROSSOVER_N = 3


# Selection
TOURNAMENT_SIZE = 2
OFFSPRING_SIZE = 6
TRUNCATION_N = POPULATION_SIZE/2

#--- Definitions

# Returns an array of fitnesses aligned to population of solutions
def calculate_fitnesses(population):
    fitnesses = []
    #fitnesses[0] = {'0': (0,0)}
    
    for solution in population:
        fitnesses.append(objective_function(solution))
    return fitnesses
    
# Generates a random candidate solution
def generate_random_solution(solution):
    random_solution = solution.copy()
    random.shuffle(random_solution)
    return random_solution

# Generates an initial solution population given a sample solution
def generate_population(solution):
    population = []
    for _ in range(POPULATION_SIZE):
        population.append(generate_random_solution(solution))
    return population

# Selects a subset of parents given their fitness values
def truncation_selection(population, fitnesses):
    # zip solutions and fitnesses together
    pop_and_fitness = list(zip(population, fitnesses))
    # rand by fitness
    ranked_solutions = sorted(pop_and_fitness, key= lambda x : x[1])
    return ranked_solutions[:TRUNCATION_N]

def tournament_selection(population, fitnesses):
    parents = []
    # zip solutions and fitnesses together
    pop_and_fitness = list(zip(population, fitnesses))
    
    # generate n random points to perform crossover
    for _ in range(OFFSPRING_SIZE):
        tournament = []
        # randomly sample k solutions
        tournament = [pop_and_fitness[random.randint(0, SOLUTION_SIZE - 1)] for _ in range(TOURNAMENT_SIZE)]
        # sort the list
        tournament.sort(key = lambda x: x[1])
        parents.append(tournament[0][0])
        # select top solution
    # repeat until enough offspring are created
    return parents



# Applies the crossover variation operator
def crossover(parent1, parent2, n):
    point_list = []
    temp = []
    # generate n random points to perform crossover
    for _ in range(n):
        point_list.append(random.randint(0,SOLUTION_SIZE))
    # sort the list
    point_list.sort()

    # for each point, swap the rest of the arrays
    for point in point_list:
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
    #new_individuals = crossover(new_individuals, CROSSOVER_N)
    return new_individuals

# 
def reproduce(population, fitnesses, new_individuals, new_fitnesses):
    # Take alll new individuals and replace with worse individuals in population
    population[-OFFSPRING_SIZE:] = new_individuals
    fitnesses[-OFFSPRING_SIZE:] = new_fitnesses
    return population, fitnesses


def check_termination():
    return False

#--- Initialisations
with open(DATA_FILE, "rb") as file:
    solution = pickle.load(file)
    
population = generate_population(solution)
fitnesses = calculate_fitnesses(population)

parents = tournament_selection(population, fitnesses)

# for index, solution in enumerate(population):
#     print(solution)
#     print(fitnesses[index])
#     print("-----------------------------------")
    
termination_flag = False
t = 0


while not termination_flag:
    #--- Selection
    # Select parents from population basen on their fitness
    parents = tournament_selection(population, fitnesses)
    #--- Variation
    # Breed new individuals by applying operators
    new_individuals = generate_variations(parents)
    #--- Fitness Calculation
    # Evaluate fitness of new individuals
    new_fitnesses = calculate_fitnesses(new_individuals)
    #--- Reproduction
    # Generate new populations by replacing least fit individuals
    population, fitnesses = reproduce(population, fitnesses, new_individuals, new_fitnesses)
    t +=1
    termination_flag = check_termination()
    if t == 10 : termination_flag = True
print(f"GA terminated with best fitness: {sorted(fitnesses)[0]}")