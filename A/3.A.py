# A* with h(n)=0 (i.e., Dijkstra’s algorithm).
import time
import statistics
import random
import heapq

class State:
    def __init__(self, num_cities):
        self.visited = [False] * num_cities
        self.num_visited = 0
        self.current_id = 0
        self.path = []

    def __lt__(self, other):
        return 0  # You can customize this based on your comparison logic

def tsp_dijkstra(graph, seed, num_cities):
    initial_state = State(num_cities)
    priority_queue = [(0, 0, initial_state)]  

    num_problems_solved = 0
    total_cost = 0
    total_nodes_expanded = 0
    total_nodes_generated = 0
    total_time = 0

    while priority_queue:
        start_time = time.time()
        cost, _, current_state = heapq.heappop(priority_queue)
        end_time = time.time()
        current_city = current_state.current_id

        if current_state.num_visited == num_cities and current_city == 0:
            # Problem solved
            num_problems_solved += 1
            total_cost += cost
            total_time += end_time - start_time

            # Print current and next paths, total cost, and time
            print(f"Problem {num_problems_solved}")
            print(f"Current Path: {current_state.path}")
            print(f"Next Path: {current_state.path + [0]}")  # Add the starting city (0)
            print(f"Total Cost: {cost:.2f}")
            print(f"Time: {end_time - start_time:.6f} seconds\n")
            continue

        for next_city in range(num_cities):
            if not current_state.visited[next_city]:
                new_cost = cost + graph[current_city][next_city]
                new_state = State(num_cities)
                new_state.visited = current_state.visited.copy()
                new_state.visited[next_city] = True
                new_state.num_visited = current_state.num_visited + 1
                new_state.current_id = next_city
                new_state.path = current_state.path + [current_city]  # Update the path

                priority = new_cost
                total_nodes_expanded += 1
                total_nodes_generated += 1
                heapq.heappush(priority_queue, (new_cost, priority, new_state))

    average_cost = total_cost / num_problems_solved if num_problems_solved > 0 else float('inf')
    average_nodes_expanded = total_nodes_expanded / num_problems_solved if num_problems_solved > 0 else 0
    average_nodes_generated = total_nodes_generated / num_problems_solved if num_problems_solved > 0 else 0
    average_time = total_time / num_problems_solved if num_problems_solved > 0 else float('inf')

    return num_problems_solved, average_cost, average_nodes_expanded, average_nodes_generated, average_time

def run_experiments_dijkstra(num_cities_list, seeds):
    results = []

    for num_cities in num_cities_list:
        for seed in seeds:
            graph = generate_random_graph(num_cities, seed)
            num_problems_solved, average_cost, average_nodes_expanded, average_nodes_generated, average_time = tsp_dijkstra(graph, seed, num_cities)
            results.append((num_cities, seed, num_problems_solved, average_cost, average_nodes_expanded, average_nodes_generated, average_time))

    return results

def generate_random_graph(num_cities, seed):
    random.seed(seed)
    graph = [[0] * num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            cost = random.randint(1, 100)
            graph[i][j] = cost
            graph[j][i] = cost
    return graph

def display_performance_summary(results):
    # Print the header of the summary table
    print("{:<10} {:<10} {:<20} {:<20} {:<25} {:<25} {:<25}".format("N", "Seed", "Problems Solved", "Avg Cost", "Avg Nodes Expanded", "Avg Nodes Generated", "Avg Time"))
    
    # Iterate through the results and print the summary for each N and algorithm
    for result in results:
        num_cities, seed, num_problems_solved, average_cost, average_nodes_expanded, average_nodes_generated, average_time = result
        print("{:<10} {:<10} {:<20} {:<20.2f} {:<25.2f} {:<25.2f} {:<25.6f}".format(
            num_cities, seed, num_problems_solved, average_cost, average_nodes_expanded, average_nodes_generated, average_time))

# Example usage:
num_cities = int(input("Enter the number of cities (N): "))
num_seeds = int(input("Enter the number of seeds: "))

results = run_experiments_dijkstra([num_cities], range(1, num_seeds + 1))
display_performance_summary(results)
