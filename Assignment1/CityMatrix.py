from dataclasses import dataclass
from typing import Union, List, Dict


@dataclass
class Map:
    roads: dict[str, dict[str, int]]

    def get_city(self, city: str) -> List[Union[Dict[str, int], str]]:
        if city not in self.roads:
            raise ValueError(f"City '{city}' not found")
        return [city, self.roads[city]]

    def get_distance(self, source: str, destination: str) -> int:
        if source not in self.roads:
            raise ValueError(f"Source city '{source}' not found")
        if destination not in self.roads:
            raise ValueError(f"Destination city '{destination}' not found")

        distance = self.roads[source].get(destination)
        if distance is None:
            raise ValueError(f"No direct route from {source} to {destination}")

        return distance

    def list_cities(self) -> list[str]:
        return sorted(self.roads.keys())

    def get_connections(self, city: str) -> dict[str, int]:
        if city not in self.roads:
            raise ValueError(f"City '{city}' not found")
        return {dest: dist for dest, dist in self.roads[city].items() if dest != city}


road_map = Map(
    roads={
        "Arad": {"Arad": 0, "Timisoara": 118, "Zerind": 75, "Sibiu": 140},
        "Bucharest": {
            "Bucharest": 0,
            "Fagaras": 211,
            "Giurgiu": 90,
            "Pitesti": 101,
            "Urziceni": 85,
        },
        "Craiova": {
            "Craiova": 0,
            "Drobeta": 120,
            "Pitesti": 138,
            "Rimnicu Vilcea": 146,
        },
        "Drobeta": {"Drobeta": 0, "Mehadia": 75, "Craiova": 120},
        "Eforie": {"Eforie": 0, "Hirsova": 86},
        "Fagaras": {"Bucharest": 211, "Fagaras": 0, "Sibiu": 99},
        "Giurgiu": {"Bucharest": 90, "Giurgiu": 0},
        "Hirsova": {"Eforie": 86, "Hirsova": 0, "Urziceni": 98},
        "Iasi": {"Iasi": 0, "Neamt": 87, "Vaslui": 92},
        "Lugoj": {"Lugoj": 0, "Mehadia": 70, "Timisoara": 111},
        "Mehadia": {"Drobeta": 75, "Lugoj": 70, "Mehadia": 0},
        "Neamt": {"Iasi": 87, "Neamt": 0},
        "Oradea": {"Oradea": 0, "Sibiu": 151, "Zerind": 71},
        "Pitesti": {
            "Bucharest": 101,
            "Craiova": 138,
            "Pitesti": 0,
            "Rimnicu Vilcea": 97,
        },
        "Rimnicu Vilcea": {
            "Craiova": 146,
            "Pitesti": 97,
            "Rimnicu Vilcea": 0,
            "Sibiu": 80,
        },
        "Sibiu": {
            "Arad": 140,
            "Fagaras": 99,
            "Oradea": 151,
            "Rimnicu Vilcea": 80,
            "Sibiu": 0,
        },
        "Timisoara": {"Arad": 118, "Lugoj": 111, "Timisoara": 0},
        "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Urziceni": 0, "Vaslui": 142},
        "Vaslui": {"Iasi": 92, "Urziceni": 142, "Vaslui": 0},
        "Zerind": {"Arad": 75, "Oradea": 71, "Zerind": 0},
    }
)


def get_cities_input():
    city1 = input("Input your first city > ")
    while city1 not in road_map.roads.keys():
        city1 = input(f"Invalid city: {city1}. Try again > ")

    city2 = input("Input your second city > ")
    while city2 not in road_map.roads.keys():
        city2 = input(f"Invalid city: {city2}. Try again > ")

    return city1, city2


if __name__ == "__main__":
    print("Available cities:")
    for i, city in enumerate(road_map.list_cities(), 1):
        connections = road_map.get_connections(city)
        print(
            f"{i}. {city} -> Connected to: {
                ', '.join(f'{dest}({dist}km)' for dest, dist in connections.items())}"
        )

    print("\nEnter city names exactly as shown above")
    try:
        source_city = input("Enter Source City: ")
        destination_city = input("Enter Destination City: ")
        distance = road_map.get_distance(source_city, destination_city)
        print(f"\nDistance from {source_city} to {
              destination_city}: {distance} km")
    except ValueError as e:
        print(f"Error: {e}")
