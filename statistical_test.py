import pandas as pd
from scipy import stats

sa = pd.read_csv('Data\Simulated_Annealing.csv')
ga = pd.read_csv('Data\Genetic_Algorithm.csv')

sa_fitness = list(sa['fitness'])
ga_fitness = list(ga['fitness'])

print(sa_fitness)
print(ga_fitness)
# print(sa_fitness.mean())
# print(sa_fitness.std())

# print(ga_fitness.mean())
# print(ga_fitness.std())

statistic, p_val = stats.wilcoxon(sa_fitness, ga_fitness)

print(statistic)
print(p_val)