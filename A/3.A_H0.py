# A* with h(n)=0 (i.e., Dijkstra’s algorithm).

# Import necessary libraries
import random
import sys
import time
from queue import PriorityQueue

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

# Class to represent the state of reached cities during the search
class Reached:
    def __init__(self, num_cities):
        self.reached_array = [[0, 0] for _ in range(num_cities)]

    def set_reached(self, city_id, visited):
        if visited:
            self.reached_array[city_id][1] = 2
        else:
            self.reached_array[city_id][0] = 2

    def get_hash_value(self):
        hash_value = 0
        for id_a, id_b in self.reached_array:
            hash_value += id_a + id_b
        return hash_value

# Function to solve the TSP problem using Dijkstra's algorithm with time constraint
def tsp_dijkstra(cost_matrix):
    num_cities = len(cost_matrix)

    # Set a time limit for the algorithm to run
    end_time_limit = time.time() + 60

    # Initialize priority queue for Dijkstra's algorithm
    priority_queue = PriorityQueue()
    priority_queue.put((0, [0], 0, Reached(num_cities)))

    optimal_path = None
    optimal_cost = float('inf')
    expanded_nodes = 0
    created_nodes = 0

    start_time = time.time()

    # Dijkstra's algorithm loop
    while not priority_queue.empty() and time.time() < end_time_limit:
        current_cost, current_path, _, current_reached = priority_queue.get()

        current_node = current_path[-1]

        # Check if the current path forms a complete tour
        if len(current_path) == num_cities and current_cost + cost_matrix[current_node][0] < optimal_cost:
            optimal_cost = current_cost + cost_matrix[current_node][0]
            optimal_path = current_path + [0]

        # Explore possible next nodes
        for next_node in range(num_cities):
            if next_node not in current_path:
                new_cost = current_cost + cost_matrix[current_node][next_node]

                # Update the reached cities state for the next node
                new_reached = Reached(num_cities)
                for i in range(num_cities):
                    new_reached.reached_array[i] = current_reached.reached_array[i][:]

                new_reached.set_reached(next_node, True)

                # Add the new state to the priority queue
                priority_queue.put((new_cost, current_path + [next_node], new_cost, new_reached))
                created_nodes += 1

        expanded_nodes += 1

    end_time = time.time()

    # Print the results
    if optimal_path:
        print(f"Optimal Path: {optimal_path}")
        print(f"Optimal Cost: {optimal_cost}")
    else:
        print("No optimal path found within the time limit.")

    print(f"Running time: {end_time - start_time:.4f} seconds")
    print(f"Expanded Nodes: {expanded_nodes}")
    print(f"Created Nodes: {created_nodes}\n")
    return optimal_cost, end_time - start_time, expanded_nodes, created_nodes

# Define a list of seeds and num_cities values for testing
seeds = [1, 2, 3, 4, 5]
num_cities_values = [5, 10, 11, 12]

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

            # Solve the TSP problem using Dijkstra's algorithm and print results
            optimal_cost, running_time, expanded_nodes, created_nodes = tsp_dijkstra(cost_matrix)
            total_optimal_cost += optimal_cost
            total_expanded_nodes += expanded_nodes
            total_created_nodes += created_nodes
            total_running_time += running_time

        except Exception as e:
            print(f"Error solving problem for n = {num_cities}, Seed = {seed}: {e}")

# Calculate and print average statistics for all solved problems
if solved_problems > 0:
    average_running_time = total_running_time / solved_problems
    average_optimal_cost = total_optimal_cost / solved_problems
    average_expanded_nodes = total_expanded_nodes / solved_problems
    average_created_nodes = total_created_nodes / solved_problems

    print(f"The number of solved problems: {solved_problems}")
    print(f"Average run time: {average_running_time:.4f} seconds")
    print(f"Average optimal path cost: {average_optimal_cost}")
    print(f"Average number of expanded nodes: {average_expanded_nodes}")
    print(f"Average number of generated nodes: {average_created_nodes}")
else:
    print("No problems were solved.")
