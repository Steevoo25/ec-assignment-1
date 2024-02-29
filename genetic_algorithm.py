import math
import random
import pickle
from simulated_annealing import objective_function, neighbour

#--- Constants
SOLUTION_SIZE = 47
DATA_FILE = "us_capitals.pkl"

#--- Definitions

# Checks if a proposed solution is a permutation of the sample soltion, ie. it contains all cities and visits each city once
def is_permutation(sample_solution : list, proposed_solution: list) -> bool:
    sample_solution.sort()
    proposed_solution.sort()
    return sample_solution == proposed_solution
    
# Filters a population removing any that violate constraints
def check_constraints(sample_solution, population):
    filtered_population = []
    #check every solution is a permutation of initial solution
    for proposed_solution in population:
        if is_permutation(sample_solution, proposed_solution):
            filtered_population.append(proposed_solution)
    
    return filtered_population
    
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
def generate_population(solution, population_size):
    population = []
    for _ in range(population_size):
        population.append(generate_random_solution(solution))
    return population

# Selects a subset of parents given their fitness values
def truncation_selection(population, fitnesses, truncation_n):
    # zip solutions and fitnesses together
    pop_and_fitness = list(zip(population, fitnesses))
    # rand by fitness
    ranked_solutions = sorted(pop_and_fitness, key= lambda x : x[1])
    return ranked_solutions[:truncation_n]

# 
def tournament_selection(population, fitnesses, offspring_size, tournament_size):
    parents = []
    # zip solutions and fitnesses together
    pop_and_fitness = list(zip(population, fitnesses))
    
    # generate n random points to perform selection
    for _ in range(offspring_size):
        tournament = []
        # randomly sample k solutions
        tournament = [pop_and_fitness[random.randint(0, SOLUTION_SIZE - 1)] for _ in range(tournament_size)]
        # sort the list
        tournament.sort(key = lambda x: x[1])
        parents.append(tournament[0][0])
        # select top solution
    # repeat until enough offspring are created
    return parents

# Applies the crossover variation operator
def n_point_crossover(parents, n):
    print(len(parents))
    # pick 2 random parents
    parent1 = parents[random.randint(0, len(parents) - 1)]
    parents.remove(parent1)
    parent2 = parents[random.randint(0, len(parents) - 1)]
    
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

# gives an offspring given a pair of parents
def ordered_crossover(parents):

    # pick 2 random parents
    parent1_index = random.randint(0, len(parents) - 1)
    parent2_index = random.randint(0, len(parents) - 1)
    
    while parent1_index == parent2_index:
        parent2_index = random.randint(0, len(parents) - 1)
        
    parent1, parent2 = parents[parent1_index], parents[parent2_index]
    
    # obtain 2 random crossover points
    point1 = random.randint(0, len(parent1) - 1)
    point2 = random.randint(0, len(parent1) - 1)
    
    # assure point1 < point2
    if point1 > point2:
        point1, point2 = point2, point1
    offspring = parent1.copy()
    
    # copy range between 2 parents
    offspring[point1:point2] = parent2[point1:point2]
    return offspring
    
# Applies the mutation variation operator
# swaps each location with a random location with probability P_m
def mutation(parents, mutation_rate):
    for solution in parents:
        if random.uniform(0,1) < mutation_rate:
            solution = neighbour(solution)
    return parents
    
# Generates new individuals by applying varation operators to parents
def generate_variations(parents, mutation_rate, crossover_n):
    # Mutation
    
    new_individuals = mutation(parents, mutation_rate)
    
    # Crossover
    for i, _ in enumerate(new_individuals[:-1]):
        new_individuals[i] = ordered_crossover(new_individuals)

    #new_individuals = n_point_crossover(parents, crossover_n)
    return new_individuals

# 
def generational_reproduction(population, fitnesses, new_individuals, new_fitnesses, offspring_size):
    # Take alll new individuals and replace with worse individuals in population
    population[-offspring_size:] = new_individuals
    fitnesses[-offspring_size:] = new_fitnesses
    return population, fitnesses

def ga(iterations, population_size, mutation_rate, tournament_size, offspring_size, crossover_n) -> tuple:

    #--- Initialisations
    with open(DATA_FILE, "rb") as file:
        sample_solution = pickle.load(file)
    
    population = generate_population(sample_solution, population_size)
    fitnesses = calculate_fitnesses(population)

    termination_flag = False
    t = 0
    
    #--- Main Loop
    while not termination_flag:
        #--- Selection
        # Select parents from population basen on their fitness
        parents = tournament_selection(population, fitnesses, offspring_size, tournament_size)
        #--- Variation
        # Breed new individuals by applying operators
        new_individuals = generate_variations(parents, mutation_rate, crossover_n)
        #--- Fitness Calculation
        # Evaluate fitness of new individuals
        new_fitnesses = calculate_fitnesses(new_individuals)
        #--- Reproduction
        # Generate new populations by replacing least fit individuals
        population, fitnesses = generational_reproduction(population, fitnesses, new_individuals, new_fitnesses, offspring_size)
        t +=1
        if t == iterations : termination_flag = True
        
    # sort population by fitness
    sorted_list = sorted(list(zip(population, fitnesses)), key= lambda x : x[1])
    #return first solution that doesnt violate constraints
    return next(((solution, fitness) for solution, fitness in sorted_list if is_permutation(sample_solution, solution)), None)