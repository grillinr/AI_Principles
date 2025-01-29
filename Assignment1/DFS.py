# In Depth First Search, the first child of the current node is put
# in the front of the queue
from CityMatrix import Map, road_map, get_cities_input, DEBUG
from typing import List, Tuple


class DFS:
    def __init__(self, road_map) -> None:
        self.reset(road_map)

    def __repr__(self) -> None:
        return "DFS Algorithm"

    def reset(self, road_map):
        self.road_map: Map = road_map
        self.distance_traveled: int = 0
        self.path = []
        self.visited = []
        self.queue = []
        self.parent = {}

    def get_sorted_city_dests(self, source) -> Tuple[List[str], int]:
        # Sorts all the connections of the source city by name and returns the list of cities
        # In descending order, so that the closest city is at the front of the queue
        connections = self.road_map.get_connections(source[0])
        sorted_connections = {}
        for key in sorted(connections, key=connections.get, reverse=True):
            sorted_connections[key] = connections[key]

        return [city for city in sorted_connections if city not in self.visited]

    def find_path(self, source: str, destination: str) -> (List[str], int):
        # First City Setup
        self.reset(road_map)
        self.queue.append((source, 0))
        self.visited.append(source)

        while self.queue:
            if DEBUG:
                print(f"Queue: {self.queue}")
                print(f"Visited: {self.visited}")

            # Gets the current city that has just been visited from the queue
            current, parent = self.queue.pop(0)
            self.visited.append(current)
            self.parent[current] = parent

            # If the current city is the destination, break the loop and
            # return the path
            if current == destination:
                path = []
                while current != source:
                    path.append(current)
                    current = self.parent[current]
                path.append(source)
                path.reverse()

                # Calculate the distance traveled
                distance = 0
                for i in range(len(path)-1):
                    distance += self.road_map.get_distance(path[i], path[i+1])

                if DEBUG:
                    print("Found destination!")
                ret = path, distance
                self.reset(road_map)
                return ret

            # Get the sorted list of cities from the current city
            currentCity = road_map.get_city(current)
            next_cities = self.get_sorted_city_dests(currentCity)

            # Add the next cities to the front of the queue
            for next_city in next_cities:
                if next_city not in self.visited:
                    self.queue.insert(0, (next_city, current))

            if DEBUG:
                print("continuing...")

        # If no path is found
        return [], -1


def test_dfs() -> None:
    # Based off the way this DFS algorithm works(choosing the shortest path to continue down) these paths are not optimal
    # but they are the expected paths based on the algorithm implementation
    romania_map = DFS(road_map)

    # Test Oradea to Bucharest
    assert romania_map.find_path("Oradea", "Bucharest") == (['Oradea', 'Zerind', 'Arad', 'Timisoara', 'Lugoj', 'Mehadia',
                                                             'Drobeta', 'Craiova', 'Pitesti', 'Rimnicu Vilcea', 'Sibiu', 'Fagaras', 'Bucharest'], 1265), "Oradea to Bucharest failed."

    print("\n\n")

    # Test Arad to Hirsova
    assert romania_map.find_path("Arad", "Hirsova") == (
        ['Arad', 'Zerind', 'Oradea', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest', 'Urziceni', 'Hirsova'], 758), "Arad to Hirsova failed."

    print("\n\n")

    # Test Craiova to Neamt
    assert romania_map.find_path("Craiova", "Neamt") == (['Craiova', 'Drobeta', 'Mehadia', 'Lugoj', 'Timisoara', 'Arad', 'Zerind', 'Oradea',
                                                          'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest', 'Urziceni', 'Vaslui', 'Iasi', 'Neamt'], 1475), "Craiova to Neamt failed."

    print("\n\n")

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
        test_dfs()
    else:
        romania_map = DFS(road_map)
        c1, c2 = get_cities_input()
        path, distance = romania_map.find_path(c1, c2)
        if path:
            print(f"The corresponding DFS path is: {
                  path} with a cost of {distance}")
        else:
            print(f"No path found between {c1} and {c2}.")
