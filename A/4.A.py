import heapq
import random
import time

class State:
    def __init__(self, N):
        self.visited = [False]*N
        self.num_visited = 0
        self.current_id = 0
        self.path = [0]  # Bắt đầu đường đi từ 0
        self.cost = 0  # Add cost to state

    def __lt__(self, other):
        return False

def min_out_heuristic(costs, state):
    unvisited_cities = [costs[state.current_id][j] for j in range(len(costs)) if not state.visited[j]]
    return min(unvisited_cities) if unvisited_cities else 0

def generate_cost_matrix(num_cities, seed):
    random.seed(seed)
    cost_matrix = [[0] * num_cities for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                cost = random.randint(1, 100)
                cost_matrix[i][j] = cost

    return cost_matrix

def a_star(N, costs):
    start_state = State(N)
    frontier = [(0, start_state)]
    reached = [None]*(N*2**N)
    expanded_nodes = 0
    created_nodes = 1  # Bắt đầu với 1 nút, tức là trạng thái ban đầu

    while frontier:
        _, current_state = heapq.heappop(frontier)
        expanded_nodes += 1

        if all(current_state.visited):
            return current_state.cost, current_state.path, expanded_nodes, created_nodes  # Trả về chi phí, đường đi, số nút đã mở rộng và số nút đã tạo

        for next_city in range(N):
            if not current_state.visited[next_city]:
                created_nodes += 1
                next_state = State(N)
                next_state.visited = current_state.visited.copy()
                next_state.visited[next_city] = True
                next_state.num_visited = current_state.num_visited + 1
                next_state.current_id = next_city
                next_state.path = current_state.path + [next_city]  # Cập nhật đường đi từ trạng thái trước đó
                next_state.cost = current_state.cost + costs[current_state.current_id][next_city]  # Update cost
                next_cost = next_state.cost + min_out_heuristic(costs, next_state)  # Use cost + heuristic as key

                S = next_state.current_id * 2**N + sum(2**i if visited else 0 for i, visited in enumerate(next_state.visited))
                if reached[S] is None or next_state.cost < reached[S]:  # Check against cost, not cost + heuristic
                    reached[S] = next_state.cost
                    heapq.heappush(frontier, (next_cost, next_state))

def main():
    N_values = [5, 10, 11, 12]
    seeds = [1, 2, 3, 4, 5]
    for N in N_values:
        for seed in seeds:
            costs = generate_cost_matrix(N, seed)
            start_time = time.time()
            result, optimal_path, expanded_nodes, created_nodes = a_star(N, costs)
            end_time = time.time()
            for row in costs:
                print(row)
            print()

            print(f'N={N}, seed={seed}')
            print(f'result={result}')
            print(f'time={end_time - start_time}')
            print(f'path={optimal_path}')
            print(f'expanded_nodes={expanded_nodes}')
            print(f'created_nodes={created_nodes}')
            print(f'cost={result}\n')

if __name__ == "__main__":
    main()