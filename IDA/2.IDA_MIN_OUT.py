# IDA* with the min-out heuristic function. I will describe the details of the min-out heuristic function later.

# Import necessary libraries
import random
import sys
import time

# Function to generate a random cost matrix for the TSP problem
def generate_cost_matrix(num_cities, seed):
    random.seed(seed)
    cost_matrix = [[0] * num_cities for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                cost = random.randint(1, 100)
                cost_matrix[i][j] = cost

    return cost_matrix

# Function to solve the TSP problem using IDA* algorithm with a min-out heuristic
def tsp_ida_star(cost_matrix):
    # Helper function to calculate the min-out heuristic for a node
    def min_out_heuristic(node, remaining_cities):
        if remaining_cities:
            return min(cost_matrix[node][city] for city in remaining_cities)
        else:
            return 0

    # Recursive depth-first search function to explore the solution space
    def dfs(node, path, cost, remaining_cities):
        nonlocal cost_matrix, num_cities, optimal_path, optimal_cost, expanded_nodes, created_nodes

        # Check if the current path forms a complete tour
        if not remaining_cities:
            total_cost = cost + cost_matrix[node][path[0]]
            if total_cost < optimal_cost:
                optimal_cost = total_cost
                optimal_path = path + [path[0]]

        # Explore possible next nodes
        for next_node in remaining_cities:
            new_cost = cost + cost_matrix[node][next_node]
            heuristic_cost = new_cost + min_out_heuristic(next_node, remaining_cities - {next_node})
            expanded_nodes += 1
            created_nodes += 1
            # Recursive call to explore the next node
            dfs(next_node, path + [next_node], new_cost, remaining_cities - {next_node})

    num_cities = len(cost_matrix)
    optimal_path = []
    optimal_cost = sys.maxsize
    expanded_nodes = 0
    created_nodes = 0

    # Set initial values for the search
    initial_node = 0
    initial_path = [initial_node]
    initial_cost = 0
    remaining_cities = set(range(num_cities)) - {initial_node}  # Exclude the initial node

    start_time = time.time()
    # Start the depth-first search from the initial node
    dfs(initial_node, initial_path, initial_cost, remaining_cities)
    end_time = time.time()

    # Print the results
    print(f"Optimal Path: {optimal_path}")
    print(f"Optimal Cost: {optimal_cost}")
    print(f"Running time: {end_time - start_time:.4f} seconds")
    print(f"Expanded Nodes: {expanded_nodes}")
    print(f"Created Nodes: {created_nodes}\n")
    return optimal_cost, end_time - start_time, expanded_nodes, created_nodes

# Define a list of seeds and num_cities values for testing
seeds = [1, 2, 3, 4, 5]
num_cities_values = [5, 10, 11, 12]

# Initialize variables to track cumulative statistics
solved_problems = 0
total_running_time = 0
total_optimal_cost = 0
total_expanded_nodes = 0
total_created_nodes = 0

# Loop over num_cities and seeds to test the algorithm
for num_cities in num_cities_values:
    for seed in seeds:
        try:
            # Generate a random cost matrix for the current problem
            cost_matrix = generate_cost_matrix(num_cities, seed)
            solved_problems += 1

            sys.stdout.reconfigure(encoding='utf-8')

            # Print the problem instance (cost matrix)
            print(f"n = {num_cities}, Seed = {seed}")
            for row in cost_matrix:
                print(row)
            print()

            # Solve the TSP problem using IDA* algorithm and print results
            optimal_cost, running_time, expanded_nodes, created_nodes = tsp_ida_star(cost_matrix)
            total_optimal_cost += optimal_cost
            total_expanded_nodes += expanded_nodes
            total_created_nodes += created_nodes
            total_running_time += running_time

        except Exception as e:
            print(f"Error solving problem for n = {num_cities}, Seed = {seed}: {e}")

# Calculate and print average statistics for all solved problems
average_running_time = total_running_time / solved_problems
average_optimal_cost = total_optimal_cost / solved_problems
average_expanded_nodes = total_expanded_nodes / solved_problems
average_created_nodes = total_created_nodes / solved_problems

print(f"The number of solved problems: {solved_problems}")
print(f"Average run time: {average_running_time:.4f} seconds")
print(f"Average optimal path cost: {average_optimal_cost}")
print(f"Average number of expanded nodes: {average_expanded_nodes}")
print(f"Average number of generated nodes: {average_created_nodes}")