# In breadth first, all the children of the current node are put in the at the back of the queue.
from CityMatrix import road_map, Map, get_cities_input
from typing import List, Tuple

DEBUG = False


class BFS:
    def __init__(self, road_map):
        self.reset(road_map)

    def reset(self, road_map):
        self.road_map: Map = road_map
        self.distance_traveled: int = 0
        self.path = []
        self.visited = []
        self.queue = []
        self.parent = {}

    def get_sorted_city_dests(self, source) -> Tuple[List[str], int]:
        # sorts all of the connections by their costs before
        # adding them to the back of the queue
        connections = self.road_map.get_connections(source[0])
        return [city for city in sorted(connections.keys())
                if city not in self.visited]

    def find_path(self, source: str, destination: str) -> (List[str], int):
        # initial setup for queue and visited and first city
        currentCity = road_map.get_city(source)
        self.queue = [(source, None)]  # store (city, parent) pairs
        self.visited.append(source)

        while self.queue:
            if DEBUG:
                print(f"Queue: {[city for city, _ in self.queue]}")
                print(f"Visited: {self.visited}")

            current, parent = self.queue.pop(0)
            self.parent[current] = parent

            # if we made it to the correct city
            # then we need to reconstruct the path
            # backwards to see which way we went
            if current == destination:
                # Reconstruct path
                path = []
                current_city = destination
                while current_city is not None:
                    path.append(current_city)
                    current_city = self.parent[current_city]
                path.reverse()

                # calculate the path distance
                distance = 0
                for i in range(len(path)-1):
                    distance += self.road_map.get_distance(path[i], path[i+1])

                if DEBUG:
                    print("Found destination!")
                ret = path, distance
                print(ret)
                self.reset(road_map)
                return ret

            # get next cities to explore
            currentCity = road_map.get_city(current)
            next_cities = self.get_sorted_city_dests(currentCity)

            # add unvisited neighbors to queue
            for next_city in next_cities:
                if next_city not in self.visited:
                    self.visited.append(next_city)
                    self.queue.append((next_city, current))

            if DEBUG:
                print("continuing...")

        # no path found
        return [], 0


def test_bfs() -> None:
    romania_map = BFS(road_map)

    # Test Timisoara to Neamt
    assert romania_map.find_path("Timisoara", "Neamt") == ([
        'Timisoara', 'Arad', 'Sibiu', 'Fagaras', 'Bucharest', 'Urziceni', 'Vaslui', 'Iasi', 'Neamt'],
        974), "Timisoara to Neamt failed."

    print("\n\n")

    # Test Arad to Bucharest
    assert romania_map.find_path("Arad", "Bucharest") == ([
        'Arad', 'Sibiu', 'Fagaras', 'Bucharest'],
        450), "Arad to Bucharest failed."

    print("\n\n")

    # Test Arad to Eforie
    assert romania_map.find_path("Arad", "Eforie") == ([
        'Arad', 'Sibiu', 'Fagaras', 'Bucharest', 'Urziceni', 'Hirsova', 'Eforie'],
        719), "Arad to Eforie failed."

    # missing city
    try:
        romania_map.find_path("mycity", "Bucharest")
        assert False, "invalid city test failed"
    except Exception:
        # test passes
        pass

    print("\ntests pasted")


if __name__ == "__main__":
    if DEBUG:
        test_bfs()
    else:
        romania_map = BFS(road_map)
        c1, c2 = get_cities_input()
        path, distance = romania_map.find_path(c1, c2)
        if path:
            print(f"The corresponding BFS path is: {
                path} with a cost of {distance}")
        else:
            print(f"No path found between {c1} and {c2}.")
