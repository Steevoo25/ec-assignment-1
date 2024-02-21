#--- Definitions
# Returns an array of fitnesses aligned to population of solutions
def calculate_fitness(population):
    return -1

#--- Initialisations
population = []
termination_flag = False
t = 0
fitnesses = calculate_fitness(population)

while not termination_flag:
    #--- Selection
    # Select parents from population basen on their fitness
    #--- Variation
    # Breed new individuals by applying operators
    #--- Fitness Calculation
    # Evaluate fitness of new individuals
    #--- Reproduction
    # Generate new populations by replacing least fit individuals
    t +=1
    