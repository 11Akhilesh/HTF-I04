import requests
import time
import math

# === Constants ===
TRUCK_CAPACITY_KG = 10000  # assumed
TRUCK_VOLUME_CUBIC_M = 60  # assumed

FUEL_COST_PER_KM = 7.5      # INR/km
LABOUR_COST = 500           # INR (fixed)
LOADING_COST = 300          # INR
UNLOADING_COST = 300        # INR
AVG_CO2_PER_KM = 0.31       # kg CO2/km
AVG_SPEED_KMPH = 50

API_KEY = "AIzaSyDzggQCozVlD6dhbw5JJYi5YC6YWT_25FU"  # replace with your actual API key

# === Helper Functions ===
def haversine_distance(coord1, coord2):
    R = 6371e3
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c / 1000  # return in km

def get_location_name(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "OK" and data["results"]:
        for comp in data["results"][0]["address_components"]:
            if "locality" in comp["types"] or "administrative_area_level_2" in comp["types"]:
                return comp["long_name"]
    return f"{lat:.2f},{lng:.2f}"

def fetch_routes(source, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={source}&destination={destination}&alternatives=false&key={API_KEY}"
    res = requests.get(url)
    return res.json()

# === Main Function ===
def main():
    source = input("Enter source location: ")
    destination = input("Enter destination location: ")

    response = fetch_routes(source, destination)
    if response["status"] != "OK":
        print("Error from API:", response["status"])
        return

    leg = response["routes"][0]["legs"][0]
    steps = leg["steps"]

    major_nodes = []
    for step in steps:
        lat = step["start_location"]["lat"]
        lng = step["start_location"]["lng"]
        name = get_location_name(lat, lng)
        if name not in major_nodes:
            major_nodes.append(name)
        time.sleep(0.1)  # To avoid API rate limit

    # Add final point
    end_lat = steps[-1]["end_location"]["lat"]
    end_lng = steps[-1]["end_location"]["lng"]
    end_name = get_location_name(end_lat, end_lng)
    if end_name not in major_nodes:
        major_nodes.append(end_name)

    output_segments = []

    for i in range(len(major_nodes) - 1):
        from_node = major_nodes[i]
        to_node = major_nodes[i + 1]

        # Estimate distance and duration
        dist_km = haversine_distance(
            (steps[i]["start_location"]["lat"], steps[i]["start_location"]["lng"]),
            (steps[i]["end_location"]["lat"], steps[i]["end_location"]["lng"])
        )
        duration_hr = dist_km / AVG_SPEED_KMPH
        cost = LABOUR_COST + LOADING_COST + UNLOADING_COST + (FUEL_COST_PER_KM * dist_km)
        emissions = AVG_CO2_PER_KM * dist_km

        segment = {
            "mode": "road",
            "from": from_node,
            "to": to_node,
            "distance_km": round(dist_km, 2),
            "duration_hr": round(duration_hr, 2),
            "cost_inr": round(cost, 2),
            "emissions_kg": round(emissions, 2),
            "source_model": "road"
        }
        output_segments.append(segment)

    print("\n🚀 Final Optimized Output:")
    import json
    print(json.dumps(output_segments, indent=2))

if __name__ == "__main__":
    main()
