from simulated_annealing import sa
from matplotlib import pyplot as plt
import pandas as pd
# Test different parameter setting and collect the data (plot)

iterations = 100
initial_temp = 100
cooling_rate = 0.95

trial_runs = list(range(10))
print(sa(iterations, initial_temp, cooling_rate))
columns = ["solution","fitness","iterations", "initial_temp", "cooling_rate"]

df = pd.DataFrame(columns=columns)

for i in trial_runs:
    # edit parameters

    # run SA
    solution, fitness = sa(iterations, initial_temp, cooling_rate)
    df.loc[i] = (solution, fitness, iterations, initial_temp, cooling_rate)
    
df.sort_values(by='fitness')
df.index.name = 'Index'
print(df)