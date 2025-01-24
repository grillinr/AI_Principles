# In best first, the queue is maintained in nondecreasing order of
# the SLD, h(n), of the children of the current city to the goal city.

from CityMatrix import road_map, Map, get_cities_input

DEBUG = False


class Greedy:
    def __init__(self, road_map):
        self.reset(road_map)

    def reset(self, road_map):
        self.road_map: Map = road_map
        self.distance_traveled: int = 0
        self.path = []
        self.visited = []

    def find_path(self, source: str, destination: str):
        currentCity = road_map.get_city(source)

        # Distance to destination is 0, return path
        if currentCity[1].get(destination) == 0:
            self.visited = []
            ret = self.path, self.distance_traveled
            self.reset(self.road_map)
            if DEBUG:
                print("we are in the right city")
            return ret

        currentCity[1] = {
            key: value
            for key, value in currentCity[1].items()
            if value != 0 and key not in self.visited
        }

        # no unexplored cities left, cycle detected
        if currentCity[1] == {}:
            self.reset(self.road_map)
            if DEBUG:
                print("cycle detected")
            return [], -1

        min_distance = min(currentCity[1].values())
        min_city = [
            city
            for city, distance in currentCity[1].items()
            if distance == min_distance
        ]
        currentCity = road_map.get_city(min_city[0])
        self.distance_traveled += min_distance
        self.path.append(currentCity[0])
        self.visited.append(currentCity[0])

        if DEBUG:
            print("continuing...")
        return self.find_path(currentCity[0], destination)


def test_greedy():
    romania_map = Greedy(road_map)
    if DEBUG:
        print("\n")

    # path with a cycle
    assert romania_map.find_path("Timisoara", "Neamt") == (
        [], -1), "Cycle test failed."
    if DEBUG:
        print("\n\n")

    # regular test
    assert romania_map.find_path("Arad", "Bucharest") == ([
        'Zerind', 'Oradea', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest'],
        575), "Regular test failed"
    if DEBUG:
        print("\n\n")

    # long path
    assert romania_map.find_path("Arad", "Eforie") == ([
        'Zerind', 'Oradea', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest', 'Urziceni', 'Hirsova', 'Eforie'],
        844), "Long test failed"

    # missing city
    try:
        romania_map.find_path("mycity", "Bucharest")
        assert False, "invalid city test failed"
    except Exception:
        # test passes
        pass

    if DEBUG:
        print("\ntests pasted")


if __name__ == "__main__":
    if DEBUG:
        test_greedy()
    else:
        romania_map = Greedy(road_map)
        c1, c2 = get_cities_input()
        path_data = romania_map.find_path(c1, c2)
        if path_data[0] == [] and path_data[1] == -1:
            print(
                "The greedy algorithm was unable to find a path, it is caught \
                in a loop/cycle.")
        else:
            print(f"The corresponding greedy path is: {
                  path_data[0]} with a cost of {path_data[1]}")
