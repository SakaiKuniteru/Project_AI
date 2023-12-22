import random
import sys
import time

def generate_cost_matrix(num_cities, seed):
    random.seed(seed)
    return [[0 if i == j else random.randint(1, 100) for j in range(num_cities)] for i in range(num_cities)]

def tsp_ida_star(cost_matrix):
    def dfs(node, path, cost, visited, REACHED):
        nonlocal num_cities, optimal_path, optimal_cost, expanded_nodes, created_nodes

        if len(path) == num_cities:
            total_cost = cost + cost_matrix[node][path[0]]
            if total_cost < optimal_cost:
                optimal_cost, optimal_path = total_cost, path + [path[0]]

        for next_node in range(num_cities):
            if next_node not in visited and cost_matrix[node][next_node] > 0:
                new_cost = cost + cost_matrix[node][next_node]
                heuristic = 0
                total_estimate = new_cost + heuristic
                
                # Kiểm tra nếu trạng thái đã đạt được
                if REACHED[next_node][0] is None or new_cost < REACHED[next_node][0]:
                    REACHED[next_node] = (new_cost, heuristic)

                    expanded_nodes += 1
                    created_nodes += 1
                    visited.add(next_node)
                    dfs(next_node, path + [next_node], new_cost, visited, REACHED)
                    visited.remove(next_node)

    num_cities = len(cost_matrix)
    optimal_path, optimal_cost = [], sys.maxsize
    expanded_nodes, created_nodes = 0, 0

    initial_node, initial_path, initial_cost = 0, [0], 0
    visited = {initial_node}

    # Khởi tạo REACHED với giá trị None cho tất cả các nút
    REACHED = {i: (None, 0) for i in range(num_cities)}
    REACHED[initial_node] = (0, 0)

    start_time = time.time()
    dfs(initial_node, initial_path, initial_cost, visited, REACHED)
    end_time = time.time()

    print(f"Optimal Path: {optimal_path}")
    print(f"Optimal Cost: {optimal_cost}")
    print(f"Running time: {end_time - start_time:.10f} seconds")
    print(f"Expanded Nodes: {expanded_nodes}")
    print(f"Created Nodes: {created_nodes}\n")
    return optimal_cost, end_time - start_time, expanded_nodes, created_nodes

seeds = [1, 2, 3, 4, 5]
num_cities_values = [5, 10, 11, 12]

solved_problems, total_running_time, total_optimal_cost, total_expanded_nodes, total_created_nodes = 0, 0, 0, 0, 0

for num_cities in num_cities_values:
    for seed in seeds:
        try:
            cost_matrix = generate_cost_matrix(num_cities, seed)
            solved_problems += 1

            print(f"n = {num_cities}, Seed = {seed}")
            for row in cost_matrix:
                print(row)
            print()

            optimal_cost, running_time, expanded_nodes, created_nodes = tsp_ida_star(cost_matrix)
            total_optimal_cost += optimal_cost
            total_expanded_nodes += expanded_nodes
            total_created_nodes += created_nodes
            total_running_time += running_time

        except Exception as e:
            print(f"Error solving problem for n = {num_cities}, Seed = {seed}: {e}")

average_running_time = total_running_time / solved_problems
average_optimal_cost = total_optimal_cost / solved_problems
average_expanded_nodes = total_expanded_nodes / solved_problems
average_created_nodes = total_created_nodes / solved_problems

print(f"The number of solved problems: {solved_problems}")
print(f"Average run time: {average_running_time:.10f} seconds")
print(f"Average optimal path cost: {average_optimal_cost}")
print(f"Average number of expanded nodes: {average_expanded_nodes}")
print(f"Average number of generated nodes: {average_created_nodes}")
