import math
import random
import pickle
from simulated_annealing import objective_function, neighbour
#--- Constants
SOLUTION_SIZE = 47
DATA_FILE = "us_capitals.pkl"

#--- Definitions

# Filters a population removing any that violate constraints
def check_constraints(population):
    #check every solution is a permutation of initial solution
    return population
    
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
def generate_population(solution, POPULATION_SIZE):
    population = []
    for _ in range(POPULATION_SIZE):
        population.append(generate_random_solution(solution))
    return population

# Selects a subset of parents given their fitness values
def truncation_selection(population, fitnesses, TRUNCATION_N):
    # zip solutions and fitnesses together
    pop_and_fitness = list(zip(population, fitnesses))
    # rand by fitness
    ranked_solutions = sorted(pop_and_fitness, key= lambda x : x[1])
    return ranked_solutions[:TRUNCATION_N]

def tournament_selection(population, fitnesses, OFFSPRING_SIZE, TOURNAMENT_SIZE):
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
def mutation(parents, MUTATION_RATE):
    for solution in parents:
        if random.uniform(0,1) < MUTATION_RATE:
            solution = neighbour(solution)
    return parents
    
# Generates new individuals by applying varation operators to parents
def generate_variations(parents, MUTATION_RATE):
    new_individuals = mutation(parents, MUTATION_RATE)
    #new_individuals = crossover(new_individuals, CROSSOVER_N)
    return new_individuals

# 
def generational_reproduction(population, fitnesses, new_individuals, new_fitnesses, OFFSPRING_SIZE):
    # Take alll new individuals and replace with worse individuals in population
    population[-OFFSPRING_SIZE:] = new_individuals
    fitnesses[-OFFSPRING_SIZE:] = new_fitnesses
    return population, fitnesses



def ga(iterations, population_size, mutation_rate, tournament_size, offspring_size):

    GA_ITERATIONS = iterations

    POPULATION_SIZE = population_size
    
    # Variation
    MUTATION_RATE = mutation_rate
    #CROSSOVER_N = 3

    # Selection
    TOURNAMENT_SIZE = tournament_size
    OFFSPRING_SIZE = offspring_size
    #TRUNCATION_N = POPULATION_SIZE/2


    #--- Initialisations
    with open(DATA_FILE, "rb") as file:
        solution = pickle.load(file)
        
    population = generate_population(solution, POPULATION_SIZE)
    fitnesses = calculate_fitnesses(population)

    termination_flag = False
    t = 0
    
    #--- Main Loop
    while not termination_flag:
        #--- Selection
        # Select parents from population basen on their fitness
        parents = tournament_selection(population, fitnesses, OFFSPRING_SIZE, TOURNAMENT_SIZE)
        #--- Variation
        # Breed new individuals by applying operators
        new_individuals = generate_variations(parents, MUTATION_RATE)
        #--- Fitness Calculation
        # Evaluate fitness of new individuals
        new_fitnesses = calculate_fitnesses(new_individuals)
        #--- Reproduction
        # Generate new populations by replacing least fit individuals
        population, fitnesses = generational_reproduction(population, fitnesses, new_individuals, new_fitnesses, OFFSPRING_SIZE)
        t +=1
        if t == GA_ITERATIONS : termination_flag = True
        
    #print(f"GA terminated with best fitness: {sorted(fitnesses)[0]}")

    # return solution with lowest fitness value
    return sorted(list(zip(population, fitnesses)), key= lambda x : x[1])[0]