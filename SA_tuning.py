from simulated_annealing import sa
from matplotlib import pyplot as plt
import pandas as pd
import optuna
# Test different parameter setting and collect the data (plot)

iteration_list = range(1,1001,5)
initial_temp_list = range(50,150,5)
cooling_rate_list = range(500, 750, 25)

trial_runs = len(iteration_list)
columns = ["solution","fitness","iterations", "initial_temp", "cooling_rate"]

df = pd.DataFrame(columns=columns)

# for i in range(trial_runs):
#     # edit parameters
#     iterations = iteration_list[i]
#     initial_temp = initial_temp_list[i]
#     cooling_rate = 0.95
#     cooling_rate = cooling_rate_list[i] / 1000
#     # run SA

    


def objective(trial):

    iterations = trial.suggest_int('iterations', 10, 100)
    initial_temp = trial.suggest_int('initial_temp',10, 50 )
    cooling_rate = trial.suggest_float('cooling_rate', 0.5, 1)
    
    solution, fitness = sa(iterations, initial_temp, cooling_rate)
    df.loc[trial.number] = (solution, fitness, iterations, initial_temp, cooling_rate)
    
    return fitness

study = optuna.create_study()
study.optimize(objective, n_trials=100)

print(study.best_params)

df = df.sort_values(by='fitness')
df.index.name = 'Index'
print(df)