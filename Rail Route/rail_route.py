import requests
import json
from geopy.distance import geodesic

API_KEY = "AIzaSyDzggQCozVlD6dhbw5JJYi5YC6YWT_25FU"

# Sample freight-supporting railway junctions in India
FREIGHT_JUNCTIONS = [
    {"name": "Itarsi Junction", "lat": 22.6148, "lng": 77.7596},
    {"name": "Mughalsarai Junction", "lat": 25.2817, "lng": 83.1198},
    {"name": "Vijayawada Junction", "lat": 16.5184, "lng": 80.6185},
    {"name": "Kharagpur Junction", "lat": 22.3397, "lng": 87.3250},
    {"name": "Katni Junction", "lat": 23.8340, "lng": 80.3949},
    {"name": "Nagpur Junction", "lat": 21.1458, "lng": 79.0882},
    {"name": "Jhansi Junction", "lat": 25.4484, "lng": 78.5685},
    {"name": "Guntakal Junction", "lat": 15.1742, "lng": 77.3841},
    {"name": "Allahabad Junction", "lat": 25.4358, "lng": 81.8463}
]

def geocode_location(place):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place, "key": API_KEY}
    res = requests.get(url, params=params).json()
    if res["status"] == "OK":
        loc = res["results"][0]["geometry"]["location"]
        return res["results"][0]["formatted_address"], (loc["lat"], loc["lng"])
    return None, None

def get_nearest_junction(location_coords):
    return min(FREIGHT_JUNCTIONS, key=lambda j: geodesic(location_coords, (j["lat"], j["lng"])).km)

def fetch_route(start, end, mode="driving"):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {"origin": start, "destination": end, "mode": mode, "key": API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] != "OK":
        return None
    leg = data["routes"][0]["legs"][0]
    return {
        "from": leg["start_address"],
        "to": leg["end_address"],
        "distance_km": leg["distance"]["value"] / 1000,
        "duration_hr": round(leg["duration"]["value"] / 3600, 2),
    }

def estimate_rail_data(from_coords, to_coords):
    distance_km = geodesic(from_coords, to_coords).km
    duration_hr = round(distance_km / 45, 2)
    cost_inr = round(distance_km * 1.5, 2)
    emissions_kg = round(distance_km * 0.07, 2)
    return distance_km, duration_hr, cost_inr, emissions_kg

def main():
    print("🚆 Rail Route Finder with Freight Junctions (Segment Format)")
    src_input = input("Enter Start Location: ")
    dst_input = input("Enter End Location: ")

    src_addr, src_coords = geocode_location(src_input)
    dst_addr, dst_coords = geocode_location(dst_input)

    if not src_coords or not dst_coords:
        print("❌ Failed to compute route: Location not found.")
        return

    nearest_src_jn = get_nearest_junction(src_coords)
    nearest_dst_jn = get_nearest_junction(dst_coords)

    print(f"📍 Nearest Freight Junctions:")
    print(f"🔹 From '{src_input}': {nearest_src_jn['name']}")
    print(f"🔹 To   '{dst_input}': {nearest_dst_jn['name']}")

    segments = []

    # Road segment: source → source junction
    if src_input.lower() != nearest_src_jn["name"].lower():
        road1 = fetch_route(src_input, nearest_src_jn["name"])
        if road1:
            segments.append({
                "mode": "road",
                "from": road1["from"],
                "to": road1["to"],
                "distance_km": round(road1["distance_km"], 2),
                "duration_hr": road1["duration_hr"],
                "cost_inr": round(road1["distance_km"] * 3, 2),
                "emissions_kg": round(road1["distance_km"] * 0.21, 2),
                "capacity_ok": True,
                "source_model": "rail"
            })

    # Rail segment: source junction → destination junction
    rail_distance, rail_duration, rail_cost, rail_emissions = estimate_rail_data(
        (nearest_src_jn["lat"], nearest_src_jn["lng"]),
        (nearest_dst_jn["lat"], nearest_dst_jn["lng"])
    )
    segments.append({
        "mode": "rail",
        "from": nearest_src_jn["name"],
        "to": nearest_dst_jn["name"],
        "distance_km": round(rail_distance, 2),
        "duration_hr": rail_duration,
        "cost_inr": rail_cost,
        "emissions_kg": rail_emissions,
        "capacity_ok": True,
        "source_model": "rail"
    })

    # Road segment: destination junction → destination
    if dst_input.lower() != nearest_dst_jn["name"].lower():
        road2 = fetch_route(nearest_dst_jn["name"], dst_input)
        if road2:
            segments.append({
                "mode": "road",
                "from": road2["from"],
                "to": road2["to"],
                "distance_km": round(road2["distance_km"], 2),
                "duration_hr": road2["duration_hr"],
                "cost_inr": round(road2["distance_km"] * 3, 2),
                "emissions_kg": round(road2["distance_km"] * 0.21, 2),
                "capacity_ok": True,
                "source_model": "rail"
            })

    if segments:
        print("\n📦 Final Route Segments (JSON):")
        print(json.dumps(segments, indent=4))
    else:
        print("🚫 No valid rail route found via freight junctions.")

if __name__ == "__main__":
    main()
