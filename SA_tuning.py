from simulated_annealing import sa
from matplotlib import pyplot as plt
import pandas as pd
import optuna

# Test different parameter setting and collect the data (plot)
columns = ["solution","fitness","iterations", "initial_temp", "cooling_rate"]

# Initialise df columns
df = pd.DataFrame(columns=columns)

# Returns fitness of SA with randomly generated parameters
def objective(trial):
    # Define parameter ranges
    iterations = trial.suggest_int('iterations', 10, 100)
    initial_temp = trial.suggest_int('initial_temp', 10, 50)
    cooling_rate = trial.suggest_float('cooling_rate', 0.5, 1)
    # Perform SA
    solution, fitness = sa(iterations, initial_temp, cooling_rate)
    # Store results in df
    df.loc[trial.number] = (solution, fitness, iterations, initial_temp, cooling_rate)
    return fitness

# Tune parameters
study = optuna.create_study()
study.optimize(objective, n_trials=100)

# Print best results
print(study.best_params)

# Show all results
df = df.sort_values(by='fitness')
df.index.name = 'Index'
print(df)