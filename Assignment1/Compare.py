from CityMatrix import road_map, get_cities_input

from Greedy import GreedyBestFirst
from BFS import BFS
from DFS import DFS
from AStar import AStar

from time import time

if __name__ == "__main__":
    cities = road_map.roads.keys()
    greedy = GreedyBestFirst(road_map).find_path
    bfs = BFS(road_map).find_path
    dfs = DFS(road_map).find_path
    astar = AStar(road_map).find_path

    algorithms = [greedy, bfs, dfs, astar]
    res = []
    c1, c2 = get_cities_input()
    for alg in algorithms:
        start = time()
        path, cost = alg(c1, c2)
        dur = time() - start
        res.append([path, cost, dur])

    print("")
    for alg, pathdata in zip(algorithms, res):
        print(f"{alg.__self__.__class__.__repr__(
            alg)} found path {pathdata[0]} in {pathdata[1]} cost in " +
            f"{pathdata[2]} seconds.")
