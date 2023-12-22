# IDA* with the min-out heuristic function. I will describe the details of the min-out heuristic function later.
import heapq
import random
import sys
import time

def generate_cost_matrix(num_cities, seed):
    """
    Tạo ma trận chi phí ngẫu nhiên cho các thành phố.

    Parameters:
        - num_cities (int): Số lượng thành phố.
        - seed (int): Hạt giống để có kết quả ngẫu nhiên nhất định.

    Returns:
        - List[List[int]]: Ma trận chi phí giữa các thành phố.
    """
    random.seed(seed)
    cost_matrix = [[0] * num_cities for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                cost = random.randint(1, 100)
                cost_matrix[i][j] = cost

    return cost_matrix


class Reached:
    def __init__(self, num_cities):
        """
        Khởi tạo đối tượng Reached để theo dõi trạng thái ghé thăm các thành phố.

        Parameters:
            - num_cities (int): Số lượng thành phố.
        """
        self.reached_array = [[0, 0] for _ in range(num_cities)]

    def set_reached(self, city_id, visited):
        """
        Đặt trạng thái ghé thăm của thành phố.

        Parameters:
            - city_id (int): ID của thành phố.
            - visited (bool): Trạng thái ghé thăm (True nếu đã ghé thăm, False nếu chưa).

        Returns:
            - None
        """
        if visited:
            self.reached_array[city_id][1] = 2
        else:
            self.reached_array[city_id][0] = 2

    def get_hash_value(self):
        """
        Tính giá trị hash của trạng thái ghé thăm.

        Returns:
            - int: Giá trị hash.
        """
        hash_value = 0
        for id_a, id_b in self.reached_array:
            hash_value += id_a + id_b
        return hash_value

def tsp_dijkstra(cost_matrix, time_limit_per_seed):
    num_cities = len(cost_matrix)
    
    # Tính thời điểm kết thúc tối đa
    end_time_limit = time.time() + time_limit_per_seed

    priority_queue = [(0, [0], 0, Reached(num_cities))]  # (g(n), path, cost, reached)
    optimal_path = []
    optimal_cost = sys.maxsize
    expanded_nodes = 0
    created_nodes = 0

    start_time = time.time()

    while priority_queue and time.time() < end_time_limit:
        current_cost, current_path, _, current_reached = heapq.heappop(priority_queue)

        current_node = current_path[-1]

        if len(current_path) == num_cities and current_cost + cost_matrix[current_node][0] < optimal_cost:
            optimal_cost = current_cost + cost_matrix[current_node][0]
            optimal_path = current_path + [0]

        for next_node in range(num_cities):
            if next_node not in current_path:
                new_cost = current_cost + cost_matrix[current_node][next_node]

                # Tạo một Reached mới để tránh sửa đổi REACHED ban đầu, nghĩa là mỗi thành phố chỉ đi 1
                new_reached = Reached(num_cities)
                for i in range(num_cities):
                    new_reached.reached_array[i] = current_reached.reached_array[i][:]

                new_reached.set_reached(next_node, True)

                heapq.heappush(priority_queue, (new_cost, current_path + [next_node], new_cost, new_reached))
                created_nodes += 1

        expanded_nodes += 1

    end_time = time.time()

    print(f"Optimal Path: {optimal_path}")
    print(f"Optimal Cost: {optimal_cost}")
    print(f"Running time: {end_time - start_time:.4f} seconds")
    print(f"Expanded Nodes: {expanded_nodes}")
    print(f"Created Nodes: {created_nodes}\n")
    return optimal_cost, end_time - start_time, expanded_nodes, created_nodes

# Example usage:
seeds = [1, 2, 3, 4, 5]
num_cities_values = [5, 10]
time_limit_per_seed = 1200  # 20 minutes for each seed

solved_problems = 0
total_running_time = 0
total_optimal_cost = 0
total_expanded_nodes = 0
total_created_nodes = 0

for num_cities in num_cities_values:
    for seed in seeds:
        try:
            cost_matrix = generate_cost_matrix(num_cities, seed)
            solved_problems += 1

            sys.stdout.reconfigure(encoding='utf-8')

            print(f"n = {num_cities}, Seed = {seed}")
            for row in cost_matrix:
                print(row)
            print()

            optimal_cost, running_time, expanded_nodes, created_nodes  = tsp_dijkstra(cost_matrix, time_limit_per_seed)
            total_optimal_cost += optimal_cost
            total_expanded_nodes += expanded_nodes
            total_created_nodes += created_nodes
            total_running_time += running_time

        except Exception as e:
            print(f"Error solving problem for n = {num_cities}, Seed = {seed}: {e}")

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