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
            for c1 in cities:
                for c2 in cities:
                    algorithm(c1, c2)

        total_time = timeit(run_for_all_cities, number=iterations)
        average_time = total_time / iterations
        return average_time

    algorithms = [greedy, bfs, dfs, astar]
    times = []
    for idx, algo in enumerate(algorithms, start=1):
        times.append(measure_algorithm_time(
            algo, cities, iterations=100))
    for alg, time in zip(algorithms, times):
        print(f"{alg.__self__.__class__.__repr__(alg)} took an average of {time}s.")
