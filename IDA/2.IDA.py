# IDA* with the mi
import sys
import time
import numpy as np

def generate_cost_matrix(num_cities, seed):
    np.random.seed(seed)
    cost_matrix = np.random.randint(1, 100, size=(num_cities, num_cities))
    np.fill_diagonal(cost_matrix, 0)
    return cost_matrix

def min_out_heuristic(matrix, current_city, visited_cities):
    return np.min([cost for j, cost in enumerate(matrix[current_city]) if j not in visited_cities])

def ida_star(matrix, current_city, visited_cities, path_cost, threshold, path, expanded_nodes, created_nodes):
    h = min_out_heuristic(matrix, current_city, visited_cities)
    f = path_cost + h
    expanded_nodes[0] += 1

    if f > threshold:
        return f, path

    if len(visited_cities) == len(matrix) - 1:
        return path_cost + matrix[current_city][0], path + [0]

    min_cost = sys.maxsize
    next_city = -1

    for j, cost in enumerate(matrix[current_city]):
        if j not in visited_cities and j != current_city:
            next_visited = visited_cities.copy()
            next_visited.add(j)
            created_nodes[0] += 1
            next_cost, next_path = ida_star(matrix, j, next_visited, path_cost + cost, threshold, path + [j], expanded_nodes, created_nodes)

            if next_cost < min_cost:
                min_cost = next_cost
                next_city = j

    return min_cost, path + [next_city]

def tsp_ida_star(matrix):
    size = len(matrix)
    start_city = 0
    visited = {start_city}
    threshold = min_out_heuristic(matrix, start_city, visited)

    expanded_nodes = [0]
    created_nodes = [1]  # The starting node is created

    start_time = time.time()
    optimal_cost, optimal_path = ida_star(matrix, start_city, visited, 0, threshold, [start_city], expanded_nodes, created_nodes)
    end_time = time.time()

    runtime = end_time - start_time

    return optimal_path, optimal_cost, runtime, expanded_nodes[0], created_nodes[0]

seeds = [1, 2, 3, 4, 5]
num_cities_values = [5, 10, 11, 12]

total_solved_problems = 0
total_runtime = 0
total_optimal_path_cost = 0
total_expanded_nodes = 0
total_created_nodes = 0

for num_cities in num_cities_values:
    num_solved_problems = 0
    sum_runtime = 0
    sum_optimal_path_cost = 0
    sum_expanded_nodes = 0
    sum_created_nodes = 0
    
    for seed in seeds:
        cost_matrix = generate_cost_matrix(num_cities, seed)
        
        print(f"\nn = {num_cities}, Seed = {seed}")
        print("Cost Matrix:")
        print(cost_matrix)

        optimal_path, optimal_cost, runtime, expanded_nodes, created_nodes = tsp_ida_star(cost_matrix)
        print("Optimal Hamiltonian Cycle Path:", optimal_path)
        print("Optimal Hamiltonian Cycle Cost:", optimal_cost)
        print("Runtime:", runtime, "seconds")
        print("Expanded Nodes:", expanded_nodes)
        print("Created Nodes:", created_nodes)

        if optimal_cost < sys.maxsize:
            num_solved_problems += 1
            sum_runtime += runtime
            sum_optimal_path_cost += optimal_cost
            sum_expanded_nodes += expanded_nodes
            sum_created_nodes += created_nodes

    if num_solved_problems > 0:
        avg_runtime = sum_runtime / num_solved_problems
        avg_optimal_path_cost = sum_optimal_path_cost / num_solved_problems
        avg_expanded_nodes = sum_expanded_nodes / num_solved_problems
        avg_created_nodes = sum_created_nodes / num_solved_problems

        print("\nSummary for n =", num_cities)
        print("Number of solved problems:", num_solved_problems)
        print("Average run time:", avg_runtime, "seconds")
        print("Average optimal path cost:", avg_optimal_path_cost)
        print("Average number of expanded nodes:", avg_expanded_nodes)
        print("Average number of generated nodes:", avg_created_nodes)

        total_solved_problems += num_solved_problems
        total_runtime += sum_runtime
        total_optimal_path_cost += sum_optimal_path_cost
        total_expanded_nodes += sum_expanded_nodes
        total_created_nodes += sum_created_nodes

if total_solved_problems > 0:
    avg_total_runtime = total_runtime / total_solved_problems
    avg_total_optimal_path_cost = total_optimal_path_cost / total_solved_problems
    avg_total_expanded_nodes = total_expanded_nodes / total_solved_problems
    avg_total_created_nodes = total_created_nodes / total_solved_problems

    print("\nTotal Summary")
    print("Total number of solved problems:", total_solved_problems)
    print("Average total run time:", avg_total_runtime, "seconds")
    print("Average total optimal path cost:", avg_total_optimal_path_cost)
    print("Average total number of expanded nodes:", avg_total_expanded_nodes)
    print("Average total number of generated nodes:", avg_total_created_nodes)

