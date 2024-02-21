import random

#--- Definitions
# Returns the objective function value for a given solution
def objective_function(solution) -> float:
    return -1

# describes how to decrease temperature from an initial temperature t_0
def temperature(t) -> int:
    return -1

# Returns a random neighbour solution of a given solution
def neighbour(solution):
    return -1

# returns the probability that we should move to new solution
def P(fitness_old, fitness_new, T) -> float:
    return 0.5

MAX_ITERATIONS = 100

#--- Initialisations
solution = []
fitness = objective_function(solution)

best_solution = solution
best_fitness = fitness

k = 0
temp = 100
#--- Main Loop
while (k<MAX_ITERATIONS):
    T = temperature(temp) # Calculate temperature
    proposed_solution = neighbour(solution) # Pick some neighbour
    proposed_fitness = objective_function(solution) # Compute its objective function value
    
    if P(fitness, proposed_fitness, T) > random.uniform(0,1): # Stochastically move to it
        solution = proposed_solution # Change state if yes
        fitness = proposed_fitness
        
    if proposed_fitness > best_fitness: # Is this a new best
        best_solution = proposed_solution # Update best found
        best_fitness = proposed_fitness
    
    k +=1
    
print(best_solution)

