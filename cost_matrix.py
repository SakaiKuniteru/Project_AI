import random
import sys

def generate_cost_matrix(num_cities, seed):
    random.seed(seed)
    cost_matrix = [[0] * num_cities for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                cost = random.randint(1, 100)
                cost_matrix[i][j] = cost

    return cost_matrix

seeds = [1, 2, 3, 4, 5]
num_cities_values = [5, 10, 11, 12]

for num_cities in num_cities_values:
    for seed in seeds:
        cost_matrix = generate_cost_matrix(num_cities, seed)
        
        sys.stdout.reconfigure(encoding='utf-8')

        print(f"n = {num_cities}, Seed = {seed}")
        for row in cost_matrix:
            print(row)
        print()