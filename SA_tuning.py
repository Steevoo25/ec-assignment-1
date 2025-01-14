from simulated_annealing import sa
from matplotlib import pyplot as plt
import pandas as pd
import optuna

# Test different parameter setting and collect the data (plot)
columns = ["fitness","iterations", "initial_temp", "cooling_rate"]

# Initialise df columns
df = pd.DataFrame(columns=columns)

# Returns fitness of SA with randomly generated parameters
def objective(trial):
    # Define parameter ranges
    iterations = trial.suggest_int('iterations', 1000, 1000)
    initial_temp = trial.suggest_int('initial_temp', 800, 1200)
    cooling_rate = trial.suggest_float('cooling_rate', 0.8, 0.99)
    # Perform SA
    _, fitness = sa(iterations, initial_temp, cooling_rate)
    # Store results in df
    df.loc[trial.number] = (fitness, iterations, initial_temp, cooling_rate)
    return fitness

# Tune parameters
study = optuna.create_study()
study.optimize(objective, n_trials=100)

# Print best results
print(study.best_params)

# Show whole dataframe
pd.set_option('display.max_rows', None)

# Show all results
df = df.sort_values(by='fitness')
df.index.name = 'Index'
print(df)

# filter by <59026
df = df[df['fitness'] < 59026]
# print mean and standard deviations
print(df.mean())
print(df.std())

#observe results