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
    penalty_weight = trial.suggest_int('penalty_weight', 1, 50 ) # higher means more penalty
    # Compute solution and fitness
    _, fitness = ga(iterations, population_size, mutation_rate, tournament_size, offspring_size, penalty_weight)
    df.loc[trial.number] = (fitness, iterations, population_size, mutation_rate, tournament_size, offspring_size, penalty_weight)
    return fitness

study = optuna.create_study()
study.optimize(objective, n_trials=100)

print(study.best_params)

df = df.sort_values(by='fitness')
df.index.name = 'Index'
print(df)
print("Valid solutions generated: ", len(df[df['fitness']<999999]) )