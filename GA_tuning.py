from genetic_algorithm import ga
from matplotlib import pyplot as plt
import pandas as pd


iterations = 100
population_size = 50
mutation_rate = 1 // population_size
tournament_size = 2
offspring_size = 20
crossover_n = 5
trial_runs = 5

columns = ["solution","fitness","iterations", "population_size", "mutation_rate", "tournament_size", "offspring_size", "crossover_n" ]
df = pd.DataFrame(columns=columns)

for i in range(trial_runs):
    # edit parameters
    # run GA
    solution, fitness = ga(iterations, population_size, mutation_rate, tournament_size, offspring_size, crossover_n)
    df.loc[i] = (solution, fitness, iterations, population_size, mutation_rate, tournament_size, offspring_size, crossover_n)
    
df.index.name = 'Index'
print(df)