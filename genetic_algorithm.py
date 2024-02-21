import math
#--- Constants
SOLUTION_SIZE = 48
DATA_FILE = "us_capitals.pkl"

#--- Definitions

# Returns the distance between 2 coordinates
def calculate_distance(start_coord, end_coord) -> float:
    start_x, start_y = start_coord
    end_x, end_y = end_coord
    return math.sqrt((start_x - end_x)**2 + (start_y - end_y)**2)

# Returns the objective function value for a given solution
# want to MINIMISE
def objective_function(solution) -> float:
    # Calculate total distance travelled for a solution
    total_distance = 0
    # enumerate solution, allows me to access the next solution once keys are not in order
    for index, location in enumerate(solution.items()):
        # extract key
        key, _ = location
        if key == SOLUTION_SIZE: # if we have reached the end of the solution, return the distance
            return total_distance
        else:
            # calculate distance between next 2 locations and add to total
            total_distance += calculate_distance(solution[index+1], solution[index + 2]) # +1 because keys start at 1
    return -1
# Returns an array of fitnesses aligned to population of solutions
def calculate_fitness(population):
    fitnesses = []
    fitnesses[0] = {'0': (0,0)}
    
    for solution in population:
        fitnesses.append(objective_function(solution))
    return fitnesses
    
# Generates an initial solution population given a sample solution
def generate_population(solution):
    return -1

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
    solution = file.load()  
    
population = generate_population(solution)
termination_flag = False
t = 0
fitnesses = calculate_fitness(population)

while not termination_flag:
    #--- Selection
    # Select parents from population basen on their fitness
    parents = select_parents(population, fitnesses)
    #--- Variation
    # Breed new individuals by applying operators
    new_individuals = generate_variations(parents)
    #--- Fitness Calculation
    # Evaluate fitness of new individuals
    new_fitnesses = calculate_fitness(new_individuals)
    #--- Reproduction
    # Generate new populations by replacing least fit individuals
    new_population = reproduce(population, fitnesses, new_individuals, fitnesses_new)
    t +=1
    termination_flag = check_termination()