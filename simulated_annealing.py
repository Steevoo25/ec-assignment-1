import random
from pickle import load
import math
import pandas as pd
#--- Constants
SOLUTION_SIZE = 47
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
    
    # enumerate solution, allows me to access the next solution
    for index, location in enumerate(solution):
        
        if index == SOLUTION_SIZE-1: # if we have reached the end of the solution, return the distance
            return total_distance
        else:
            # calculate distance between next 2 locations and add to total
            total_distance += calculate_distance(location, solution[index + 1]) # +1 because keys start at 1
    return -1

# Describes how to decrease temperature from an initial temperature t_0
def temperature(t, COOLING_FACTOR) -> int:
    return t * COOLING_FACTOR

# Returns a random neighbour solution of a given solution
def neighbour(solution):

    neighbour_solution = solution.copy()
    # swap 2 random locations
    rand1 = random.randint(1,SOLUTION_SIZE)
    rand2 = random.randint(1,SOLUTION_SIZE)
    
    # swap 2 cities
    neighbour_solution[rand1], neighbour_solution[rand2] = neighbour_solution[rand2] ,neighbour_solution[rand1]
    #print(f"Swapped locations {rand1} and {rand2}")
    return neighbour_solution
    
# returns the probability that we should move to new solution
def P(fitness_old, fitness_new, T) -> float:
    # always move to better solutions
    if fitness_new < fitness_old:
        #print("new is better taking it")
        return 1
    else:
    # sometimes move to worse solutions
        p = math.e**((fitness_old - fitness_new)/T)
        #print(f"p is {p}")
        return p
    
def sa(iterations, initial_temp, cooling_rate):

    T = initial_temp    
    #--- Initialisations
    with open(DATA_FILE, "rb") as file:
        solution = load(file)
        
    #solution = sorted(solution)
    fitness = objective_function(solution)
    
    best_solution = solution
    best_fitness = fitness

    k = 0
    #--- Main Loop
    
    while (k<iterations):
        T = temperature(T, cooling_rate) # Calculate temperature

        proposed_solution = neighbour(solution) # Pick some neighbour
        proposed_fitness = objective_function(solution) # Compute its objective function value
        
        if P(fitness, proposed_fitness, T) > random.uniform(0,1): # Stochastically move to it
            solution = proposed_solution # Change state if yes
            fitness = proposed_fitness
            
        if proposed_fitness < best_fitness: # Is this a new best
            best_solution = proposed_solution # Update best found
            best_fitness = proposed_fitness
            
        k +=1

        if T < 0.0001 : return best_solution, best_fitness

    return best_solution, best_fitness


def run_best_params(iterations, initial_temp, cooling_rate):

    columns = ["solution", "fitness"]

    # Initialise df columns
    df = pd.DataFrame(columns=columns)
    for i in range(30):
        solution, fitness = sa(iterations, initial_temp, cooling_rate)
        df.loc[i] = (solution, fitness)
    df = df.sort_values(by='fitness')
    print(df)
    df.to_csv('./Data/Simulated_Annealing.csv')
    # save to csv
    return

if __name__ == "__main__":
    # Update with results from study
    OPT_ITERATIONS = 107
    OPT_INIT_TEMP = 1131
    OPT_COOL_RATE = 0.95

    print(f"Running Simulated Annealing with parameters:\nIterations: {OPT_ITERATIONS}, Initial Temperature: {OPT_INIT_TEMP}, Cooling Rate: {OPT_COOL_RATE}")
    run_best_params(OPT_ITERATIONS, OPT_INIT_TEMP, OPT_COOL_RATE)
    
