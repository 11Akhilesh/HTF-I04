import requests
import csv
import math
import os
from dotenv import load_dotenv
import heapq

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("AIzaSyDzggQCozVlD6dhbw5JJYi5YC6YWT_25FU")

# Constants
CARGO_PLANE_SPEED_KMPH = 850
MAX_DIRECT_DISTANCE_KM = 1600  # Increased to allow realistic multi-hop routes

# Haversine formula
def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.asin(math.sqrt(a))

# Load airports from CSV
airports = {}
with open("airports.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        code = row["code"].strip().upper()
        lat, lon = float(row["lat"]), float(row["lon"])
        airports[code] = (lat, lon)

# Create graph using haversine distances
graph = {}
airport_codes = list(airports.keys())
for i in range(len(airport_codes)):
    for j in range(i + 1, len(airport_codes)):
        a, b = airport_codes[i], airport_codes[j]
        dist = haversine(airports[a], airports[b])

        if dist <= MAX_DIRECT_DISTANCE_KM:
            graph.setdefault(a, {})[b] = dist
            graph.setdefault(b, {})[a] = dist

# A* pathfinding
def astar(start, goal):
    open_set = [(0, start)]
    came_from = {}
    g_score = {node: float("inf") for node in graph}
    g_score[start] = 0

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor, dist in graph.get(current, {}).items():
            tentative = g_score[current] + dist
            if tentative < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative
                h = haversine(airports[neighbor], airports[goal])
                heapq.heappush(open_set, (tentative + h, neighbor))

    return None

# Calculate distance and time
def calculate_path_stats(path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += haversine(airports[path[i]], airports[path[i + 1]])
    time_hr = total_distance / CARGO_PLANE_SPEED_KMPH
    return total_distance, time_hr

# Main execution
if __name__ == "__main__":
    print("Available Airports:", ", ".join(sorted(airports.keys())))
    start = input("Enter START airport code: ").strip().upper()
    goal = input("Enter GOAL airport code: ").strip().upper()

    if start not in airports or goal not in airports:
        print("❌ Invalid airport code(s). Please check and try again.")
    elif start == goal:
        print("⚠️ Start and goal airports are the same.")
    else:
        path = astar(start, goal)
        if path:
            distance_km, time_hr = calculate_path_stats(path)
            print(f"\n🛫 Optimal Air Cargo Route: {' → '.join(path)}")
            print(f"📏 Total Distance: {distance_km:.2f} km")
            print(f"⏱️ Estimated Time: {time_hr:.2f} hours")
        else:
            print("🚫 No route found between the selected airports.")
