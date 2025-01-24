# In Depth First Search, the first child of the current node is put
# in the front of the queue
from CityMatrix import road_map, Map


class DFS:
    def __init__(self, road_map) -> None:
        self.road_map: Map = road_map
        self.distance_traveled: int = 0
        self.path = []
        self.visited = []
