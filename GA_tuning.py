from genetic_algorithm import ga
from matplotlib import pyplot as plt
import pandas as pd
import optuna

# Initialse df columns
columns = ["fitness", "iterations", "population_size", "mutation_rate", "tournament_size", "offspring_size", "penalty_weight" ]
df = pd.DataFrame(columns=columns)

def objective(trial):
    # Define parameter ranges
    iterations = trial.suggest_int('iterations', 10, 100)
    population_size = trial.suggest_int('population_size', 10, 100)
    mutation_rate = 1 / iterations
    tournament_size = trial.suggest_int('tournament_size', 2, 10)
    offspring_size = trial.suggest_int('offspring_size', 3, 20)
    penalty_weight = trial.suggest_int('penalty_weight', 1000, 5000 ) # higher means more penalty
    # Compute solution and fitness
    _, fitness = ga(iterations, population_size, mutation_rate, tournament_size, offspring_size, penalty_weight)
    df.loc[trial.number] = (fitness, iterations, population_size, mutation_rate, tournament_size, offspring_size, penalty_weight)
    return fitness

# Create tuning study
study = optuna.create_study()
# Optimise objective over 100 runs
study.optimize(objective, n_trials=100)

# Print best results
print(study.best_params)

# Sort all data by fitness
df = df.sort_values(by='fitness')
df.index.name = 'Index'

# Show whole dataframe
pd.set_option('display.max_rows', None)

# SHow dataframe
print(df)

# Filter to only see valid solutions
df = df[df['fitness']<999999]

print("Valid solutions generated: ", 100 - len(df))

# print mean and standard deviations
print(df.mean())
print(df.std())