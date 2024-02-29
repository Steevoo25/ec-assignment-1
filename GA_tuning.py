from genetic_algorithm import ga
import matplotlib as plt

iterations = 1000
population_size = 50
mutation_rate = 1 // population_size
tournament_size = 2
offspring_size = 6
crossover_n = 5

print(f"Result for iterations: {iterations}, population_size: {population_size}, mutation_rate: {mutation_rate}, tournament_size: {tournament_size}, offspring_size: {offspring_size}, crossover_n: {crossover_n}")
print(ga(iterations, population_size, mutation_rate, tournament_size, offspring_size, crossover_n))