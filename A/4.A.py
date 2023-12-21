# A* with the min-out heuristic function.
import heapq
import random
import time


class State:
    def __init__(self, N):
        self.visited = [False]*N
        self.num_visited = 0
        self.current_id = 0
        self.path = []  # Thêm đường đi
        self.cost = 0  # Add cost to state

    def __lt__(self, other):
        return False


def min_out_heuristic(costs, state):
    unvisited_cities = [costs[state.current_id][j] for j in range(len(costs)) if not state.visited[j]]
    return min(unvisited_cities) if unvisited_cities else 0


def a_star(N, costs):
    start_state = State(N)
    frontier = [(0, start_state)]
    reached = [None]*(N*2**N)

    while frontier:
        _, current_state = heapq.heappop(frontier)
        if all(current_state.visited):
            return current_state.cost, current_state.path  # Trả về chi phí và đường đi

        for next_city in range(N):
            if not current_state.visited[next_city]:
                next_state = State(N)
                next_state.visited = current_state.visited.copy()
                next_state.visited[next_city] = True
                next_state.num_visited = current_state.num_visited + 1
                next_state.current_id = next_city
                next_state.path = current_state.path + [next_city]  # Cập nhật đường đi
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
            random.seed(seed)
            costs = [[random.randint(1, 100) for _ in range(N)] for _ in range(N)]
            start_time = time.time()
            result, optimal_path = a_star(N, costs)
            end_time = time.time()
            for row in costs:
                print(row)
            print()

            print(f'N={N}, seed={seed}')
            print(f'result={result}')
            print(f'time={end_time - start_time}')
            print(f'path={optimal_path}\n')


if __name__ == "__main__":
    main()
