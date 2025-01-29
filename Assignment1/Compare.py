from CityMatrix import road_map

from Greedy import GreedyBestFirst
from BFS import BFS
from DFS import DFS
from AStar import AStar

from timeit import timeit

if __name__ == "__main__":
    cities = road_map.roads.keys()
    greedy = GreedyBestFirst(road_map).find_path
    bfs = BFS(road_map).find_path
    dfs = DFS(road_map).find_path
    astar = AStar(road_map).find_path

    def measure_algorithm_time(algorithm, cities, iterations=100):
        def run_for_all_cities():
            for city in cities:
                algorithm(city)

        total_time = timeit.timeit(run_for_all_cities, number=iterations)
        average_time = total_time / iterations
        return average_time

    algorithms = [greedy, bfs, dfs, astar]
    for idx, algo in enumerate(algorithms, start=1):
        avg_time = measure_algorithm_time(algo, cities, iterations=100)
        print(f"Algorithm {idx}: Average time per iteration: {
              avg_time:.6f} seconds")
