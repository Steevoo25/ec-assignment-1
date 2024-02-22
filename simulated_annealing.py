import random
from pickle import load
import math
#--- Constants

MAX_ITERATIONS = 100
DATA_FILE = "us_capitals.pkl"
SOLUTION_SIZE = 48
INITIAL_TEMP = 100
COOLING_FACTOR = 0.95 * INITIAL_TEMP
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

# Describes how to decrease temperature from an initial temperature t_0
def temperature(t) -> int:
    return t * COOLING_FACTOR

# Returns a random neighbour solution of a given solution
def neighbour(solution):

    neighbour_solution = solution.copy()
    # swap 2 random locations
    rand1 = random.randint(1,SOLUTION_SIZE)
    rand2 = random.randint(1,SOLUTION_SIZE)
    
    temp = neighbour_solution[rand1]
    neighbour_solution[rand1] = neighbour_solution[rand2]
    neighbour_solution[rand2] = temp
    #print(f"Swapped locations {rand1} and {rand2}")
    return neighbour_solution
    
# returns the probability that we should move to new solution
def P(fitness_old, fitness_new, T) -> float:
    if fitness_new < fitness_old:
        #print("new is better taking it")
        return 1
    else:
        p = math.e**((fitness_old - fitness_new)/T)
        #print(f"p is {p}")
        return p

#--- Initialisations

with open(DATA_FILE, "rb") as file:
    solution = load(file)
fitness = objective_function(solution)
#print(f"Initial solution: {solution} \nInitial Fitness: {fitness}")
best_solution = solution
best_fitness = fitness
k = 0

#--- Main Loop
while (k<MAX_ITERATIONS):
    T = temperature(INITIAL_TEMP) # Calculate temperature
    proposed_solution = neighbour(solution) # Pick some neighbour
    proposed_fitness = objective_function(solution) # Compute its objective function value
    
    if P(fitness, proposed_fitness, T) > random.uniform(0,1): # Stochastically move to it
        solution = proposed_solution # Change state if yes
        fitness = proposed_fitness
        
    if proposed_fitness < best_fitness: # Is this a new best
        best_solution = proposed_solution # Update best found
        best_fitness = proposed_fitness
    k +=1
    
#print(f"Final solution after {k} iterations was: {best_solution} \nwith fitness of {best_fitness}")