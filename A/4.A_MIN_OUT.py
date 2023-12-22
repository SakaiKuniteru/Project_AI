# A* with the min-out heuristic function

# Import necessary libraries
import heapq
import random
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

# Class to represent the state of the TSP problem
class State:
    def __init__(self, N):
        self.visited = [False]*N
        self.num_visited = 0
        self.current_id = 0
        self.path = [0]
        self.cost = 0

    def __lt__(self, other):
        return self.cost < other.cost

# Heuristic function for the A* algorithm
def min_out_heuristic(costs, state):
    unvisited_cities = [costs[state.current_id][j] for j in range(len(costs)) if not state.visited[j]]
    return min(unvisited_cities) if unvisited_cities else 0

# A* algorithm to solve the TSP problem
def a_star(N, costs):
    start_state = State(N)
    frontier = [(0, start_state)]
    reached = [None] * (N * 2**N)
    expanded_nodes = 0
    created_nodes = 0

    while frontier:
        _, current_state = heapq.heappop(frontier)
        expanded_nodes += 1

        if current_state.num_visited == N and current_state.current_id == 0:
            return current_state.cost, current_state.path, expanded_nodes, created_nodes

        for next_city in range(N):
            if not current_state.visited[next_city]:
                next_state = State(N)
                created_nodes += 1
                next_state.visited = current_state.visited.copy()
                next_state.visited[next_city] = True
                next_state.num_visited = current_state.num_visited + 1
                next_state.current_id = next_city
                next_state.path = current_state.path + [next_city]
                next_state.cost = current_state.cost + costs[current_state.current_id][next_city]
                next_cost = next_state.cost + min_out_heuristic(costs, next_state)

                # Hash value to check if the state has been reached before
                S = next_state.current_id * 2**N + sum(2**i if visited else 0 for i, visited in enumerate(next_state.visited))
                if reached[S] is None or next_cost < reached[S]:
                    reached[S] = next_cost
                    heapq.heappush(frontier, (next_cost, next_state))

    return None

# Main function to test the A* algorithm for different problem sizes and seeds
def main():
    N_values = [5, 10, 11, 12]
    seeds = [1, 2, 3, 4, 5]

    total_problems_solved = 0
    total_running_time = 0
    total_optimal_cost = 0
    total_expanded_nodes = 0
    total_created_nodes = 0

    for N in N_values:
        for seed in seeds:
            costs = generate_cost_matrix(N, seed)
            start_time = time.time()
            result, optimal_path, expanded_nodes, created_nodes = a_star(N, costs)
            end_time = time.time()

            print(f'N= {N}, Seed= {seed}')
            for row in costs:
                print(row)
            print()

            total_problems_solved += 1
            total_running_time += end_time - start_time
            total_optimal_cost += result
            total_expanded_nodes += expanded_nodes
            total_created_nodes += created_nodes

            print(f'Optimal Path: {optimal_path}')
            print(f'Optimal Cost: {result}')
            print(f'Running time: {end_time - start_time:.10f}')
            print(f'Expanded Nodes: {expanded_nodes}')
            print(f'Created Nodes: {created_nodes} \n')

    average_running_time = total_running_time / total_problems_solved
    average_optimal_cost = total_optimal_cost / total_problems_solved
    average_expanded_nodes = total_expanded_nodes / total_problems_solved
    average_created_nodes = total_created_nodes / total_problems_solved

    print(f'The number of solved problems: {total_problems_solved}')
    print(f'Average run time: {average_running_time:.10f}')
    print(f'Average optimal path cost: {average_optimal_cost}')
    print(f'Average number of expanded nodes: {average_expanded_nodes}')
    print(f'Average number of generated nodes: {average_created_nodes}')

# Entry point to the script
if __name__ == "__main__":
    main()