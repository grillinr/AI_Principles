# In A* the queue is maintained in nondecreasing order of the evaluation function
# f(n) = g(n) + h(n) of the children of the current city to the goal city.
# (Note that there is some backtracking taking place here, because the algorithm
# may need to discard a current node and backtrack to a previous step.)

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from queue import PriorityQueue
from CityMatrix import Map, road_map, get_cities_input
import math

DEBUG = False

# Straight-line distances to Bucharest (our heuristic values)
SLD_TO_BUCHAREST = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374,
}


@dataclass(order=True)
class PrioritizedCity:
    priority: int
    city: str = None
    parent: str = None
    g_cost: int = 0  # Path cost from start to current node

    def __eq__(self, other):
        if not isinstance(other, PrioritizedCity):
            return NotImplemented
        return self.city == other.city


class AStar:
    def __init__(self, road_map: Map):
        self.road_map = road_map

    def heuristic(self, city: str, goal: str) -> int:
        """Straight-line distance heuristic."""
        if city == "Bucharest":
            return SLD_TO_BUCHAREST[goal]
        if goal == "Bucharest":
            return SLD_TO_BUCHAREST[city]

        d1, d2 = SLD_TO_BUCHAREST[city], SLD_TO_BUCHAREST[goal]

        # Approximate using the Euclidean distance formula and law of cosines
        estimated_dist = math.sqrt(
            d1**2 + d2**2 - 2 * d1 * d2 * math.cos(math.radians(60))
        )  # Assume 60° between vectors

        return estimated_dist.__ceil__()

    def find_path(self, start: str, goal: str) -> Tuple[List[str], int]:
        if start not in self.road_map.roads or goal not in self.road_map.roads:
            raise ValueError("Start or goal city not found in map")

        pqueue = PriorityQueue()
        pqueue.put(PrioritizedCity(
            self.heuristic(start, goal), start, None, 0))

        came_from: Dict[str, Optional[str]] = {start: None}
        cost_so_far: Dict[str, int] = {start: 0}

        while not pqueue.empty():
            current = pqueue.get()
            if DEBUG:
                print(f"Current city: {current.city}")
                print(f"Current queue: {pqueue}")
            current_city = current.city

            if current_city == goal:
                if DEBUG:
                    print("We are in the right city.")
                break

            # Get all neighbors of current city
            for next_city, distance in self.road_map.get_connections(
                current_city
            ).items():
                new_cost = cost_so_far[current_city] + distance

                if next_city not in cost_so_far or new_cost < cost_so_far[next_city]:
                    cost_so_far[next_city] = new_cost
                    # Pure greedy - only uses heuristic
                    priority = self.heuristic(next_city, goal)
                    pqueue.put(
                        PrioritizedCity(priority, next_city,
                                        current_city, new_cost)
                    )
                    came_from[next_city] = current_city

        # If we didn't reach the goal
        if goal not in came_from:
            return [], -1

        # Reconstruct path
        path = []
        current = goal
        total_cost = cost_so_far[goal]

        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path, total_cost  # Remove start city from path


def test_a_star():
    romania = AStar(road_map)

    # Test 1: Path from Arad to Bucharest
    path, cost = romania.find_path("Arad", "Bucharest")
    print("Test 1: Arad to Bucharest")
    print(f"Path: {path}")
    print(f"Cost: {cost}")
    assert path == [
        "Arad",
        "Sibiu",
        "Fagaras",
        "Bucharest",
    ], "Failed: Arad to Bucharest path incorrect"
    assert cost == 450, "Failed: Arad to Bucharest cost incorrect"

    # Test 2: Path from Timisoara to Bucharest
    path, cost = romania.find_path("Timisoara", "Bucharest")
    print("\nTest 2: Timisoara to Bucharest")
    print(f"Path: {path}")
    print(f"Cost: {cost}")
    assert path == [
        "Timisoara",
        "Lugoj",
        "Mehadia",
        "Drobeta",
        "Craiova",
        "Pitesti",
        "Bucharest",
    ], "Failed: Timisoara to Bucharest path incorrect"
    assert cost != -1, "Failed: Should find a path from Timisoara to Bucharest"

    # Test 3: Try invalid city
    print("\nTest 3: Invalid city test")
    try:
        romania.find_path("InvalidCity", "Bucharest")
        assert False, "Failed: Should raise error for invalid city"
    except ValueError as e:
        print(f"Successfully caught error: {e}")

    print("\nAll tests passed!")


if __name__ == "__main__":
    if DEBUG:
        test_a_star()
    else:
        romania_map = AStar(road_map)
        c1, c2 = get_cities_input()
        path, distance = romania_map.find_path(c1, c2)
        if path == [] and distance == -1:
            print(
                f"The greedy algorithm was unable to find a path between {c1} \
                        and {c2}, it is caught in a loop/cycle."
            )
        else:
            print(
                f"The corresponding greedy path is: {
                    path} with a cost of {distance}."
            )
