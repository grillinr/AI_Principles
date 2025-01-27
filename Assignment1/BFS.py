# In breadth first, all the children of the current node are put in the at the back of the queue.

from CityMatrix import road_map, Map, get_cities_input
from typing import List

DEBUG = True


class BFS:
    def __init__(self, road_map):
        self.reset(road_map)

    def reset(self, road_map):
        self.road_map: Map = road_map
        self.distance_traveled: int = 0
        self.path = []
        self.visited = []
        self.queue = []

    def get_sorted_city_dests(self, source) -> List[str]:
        sorted_cities = sorted(source[1].items(), key=lambda x: x[1])
        sorted_city_names = [
            city for city, distance in sorted_cities
            if city != source[0] and
            city not in self.queue
        ]
        return sorted_city_names

    def find_path(self, source: str, destination: str) -> (List[int], int):
        currentCity = road_map.get_city(source)
        self.queue = self.get_sorted_city_dests(currentCity)
        self.visited.append(currentCity[0])
        while self.queue:
            print(self.queue)
            # "pop" off the top of the queue
            currentCity = road_map.get_city(self.queue[0])
            self.queue = self.queue[1:]

            # ensure that we add each city to visited
            if currentCity[0] not in self.visited:
                self.visited.append(currentCity[0])

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

            # enqueue the next cities to visit
            self.queue += self.get_sorted_city_dests(currentCity)


if __name__ == "__main__":
    romania_map = BFS(road_map)
    romania_map.find_path("Arad", "Bucharest")
