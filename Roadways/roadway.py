import requests
import heapq
import math
import time
import re

# === Utility Functions ===
def haversine_distance(coord1, coord2):
    R = 6371e3  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def reverse_geocode(lat, lng, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK" and data["results"]:
        components = data["results"][0].get("address_components", [])
        city = ""
        highway = ""
        for comp in components:
            if "route" in comp["types"]:
                if "NH" in comp["long_name"] or "SH" in comp["long_name"] or "Highway" in comp["long_name"]:
                    highway = comp["long_name"]
            if "locality" in comp["types"] or "administrative_area_level_2" in comp["types"]:
                city = comp["long_name"]
        result = []
        if highway:
            result.append(highway)
        if city:
            result.append(city)
        return " - ".join(result) if result else city or highway
    else:
        return f"{lat:.4f}, {lng:.4f}"

def fetch_routes_data(source, destination, api_key):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={source}&destination={destination}&alternatives=true&departure_time=now&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        print("Error from Google Maps API:", data["status"])
        return []

    return data["routes"]

def build_graph_from_steps(steps):
    graph = {}
    coords = []

    for step in steps:
        start = (step["start_location"]["lat"], step["start_location"]["lng"])
        end = (step["end_location"]["lat"], step["end_location"]["lng"])
        distance = step["distance"]["value"]

        coords.append(start)
        coords.append(end)

        if start not in graph:
            graph[start] = []
        graph[start].append((end, distance))

    return graph, coords[0], coords[-1]

def a_star(graph, start, end):
    open_set = [(0 + haversine_distance(start, end), 0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current_cost, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[end]

        for neighbor, weight in graph.get(current, []):
            tentative_g = current_cost + weight
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + haversine_distance(neighbor, end)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                came_from[neighbor] = current

    return [], float('inf')

def is_major_checkpoint(place_name):
    return (
        "NH" in place_name or
        "SH" in place_name or
        "Highway" in place_name
    )

def display_route_summary(route_data, route_number, checkpoints, api_key):
    leg = route_data["legs"][0]
    summary = route_data.get("summary", "Unnamed Route")
    distance = leg["distance"]["text"]
    duration = leg["duration"]["text"]
    traffic_time = leg.get("duration_in_traffic", {}).get("text", duration)

    print(f"\n🚚 Route {route_number + 1}: {summary}")
    print(f"   Total Distance: {distance}")
    print(f"   Estimated Duration: {duration} (with traffic: {traffic_time})")
    print("   🛑 Major Checkpoints (NH, SH + City):")

    shown_places = set()
    major_city = None
    displayed = 0

    for i, (lat, lng) in enumerate(checkpoints):
        if displayed >= 25:
            break

        place = reverse_geocode(lat, lng, api_key)
        if is_major_checkpoint(place) and place not in shown_places:
            print(f"     {displayed + 1}. {place}")
            shown_places.add(place)
            if not major_city:
                major_city = place
            displayed += 1
            time.sleep(0.1)

    return {
        "summary": summary,
        "distance": leg["distance"]["value"],
        "distance_text": distance,
        "duration": duration,
        "traffic_time": traffic_time,
        "major_city": major_city or "N/A"
    }

# === MAIN ===
if __name__ == "__main__":
    print("\n🔽 Route Optimizer 🔽")
    source = input("Enter source location (e.g., Bangalore): ")
    destination = input("Enter destination location (e.g., Mumbai): ")
    api_key = "AIzaSyDzggQCozVlD6dhbw5JJYi5YC6YWT_25FU"  # Replace with your actual Google Maps API key

    routes = fetch_routes_data(source, destination, api_key)
    if not routes:
        print("❌ No routes found. Exiting.")
        exit()

    print(f"\n✅ Found {len(routes)} route(s) from {source} to {destination}.")

    route_infos = []

    for i, route in enumerate(routes):
        steps = route["legs"][0]["steps"]
        graph, start_node, end_node = build_graph_from_steps(steps)
        path, total_distance = a_star(graph, start_node, end_node)
        info = display_route_summary(route, i, path, api_key)
        info["route_index"] = i
        route_infos.append(info)

    # Sort and select best route (shortest distance)
    best = min(route_infos, key=lambda x: x["distance"])

    print("\n📍 Final Optimized Route Selection:")
    print("===================================")
    print(f"✔️  Best Route: Route {best['route_index'] + 1} - {best['summary']}")
    print(f"📌 Source: {source}")
    print(f"📌 Destination: {destination}")
    print(f"🏙️  Major Checkpoint (first city/highway): {best['major_city']}")
    print(f"📏 Distance: {best['distance_text']}")
    print(f"⏱️  Estimated Duration: {best['traffic_time']}")
    print("===================================")
   