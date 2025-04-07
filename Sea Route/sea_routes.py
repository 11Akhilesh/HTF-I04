import googlemaps
import math
from geopy.distance import geodesic

# === ✅ Your Google Maps API Key ===
API_KEY = "AIzaSyBlC9_QicFifEy84f-XqgkKQ2IjyLFMYaM"
gmaps = googlemaps.Client(key=API_KEY)

# === ✅ All Major Indian Cargo Ports with Coordinates ===
ports = {
    "Nhava Sheva": (18.9633, 72.9510),
    "Kandla": (23.0333, 70.2167),
    "Mundra": (22.8394, 69.7096),
    "Hazira": (21.1167, 72.6167),
    "Mumbai": (18.9498, 72.8355),
    "Mormugao": (15.4095, 73.8057),
    "Kochi": (9.9312, 76.2673),
    "Tuticorin": (8.7642, 78.1348),
    "Chennai": (13.0827, 80.2707),
    "Visakhapatnam": (17.7041, 83.2977),
    "Paradip": (20.3167, 86.6167),
    "Haldia": (22.0667, 88.0695)
}

# === ✅ Port Address Map (for better API results) ===
port_address_map = {
    "Nhava Sheva": "Jawaharlal Nehru Port Trust, Navi Mumbai",
    "Kandla": "Kandla Port Trust, Gandhidham",
    "Mundra": "Mundra Port, Gujarat",
    "Hazira": "Hazira Port, Surat",
    "Mumbai": "Mumbai Port Trust, Mumbai",
    "Mormugao": "Mormugao Port, Goa",
    "Kochi": "Cochin Port Trust, Willingdon Island, Kochi",
    "Tuticorin": "V.O. Chidambaranar Port, Thoothukudi",
    "Chennai": "Chennai Port Trust, Chennai",
    "Visakhapatnam": "Visakhapatnam Port Trust, Andhra Pradesh",
    "Paradip": "Paradip Port Trust, Odisha",
    "Haldia": "Haldia Port, West Bengal"
}


# === 🔍 Get Lat/Lng of a Location ===
def get_lat_lng(place):
    geocode_result = gmaps.geocode(place)
    if not geocode_result:
        raise Exception(f"Could not find location: {place}")
    return geocode_result[0]["geometry"]["location"]["lat"], geocode_result[0]["geometry"]["location"]["lng"]


# === 📏 Find Nearest Port ===
def find_nearest_port(lat, lng):
    min_dist = float("inf")
    nearest = None
    for port, (plat, plng) in ports.items():
        dist = geodesic((lat, lng), (plat, plng)).km
        if dist < min_dist:
            min_dist = dist
            nearest = port
    return nearest


# === 🚗 Get Road Distance Using Distance Matrix API ===
def get_road_distance(origin, destination):
    result = gmaps.distance_matrix(origin, destination, mode="driving")
    try:
        element = result["rows"][0]["elements"][0]
        dist_km = element["distance"]["value"] / 1000
        duration_hr = element["duration"]["value"] / 3600
        return dist_km, duration_hr
    except Exception as e:
        print("⚠️ Distance Matrix API error:", result)
        raise Exception("Invalid route. Check input or API limits.")


# === 🚢 Estimate Sea Distance (great-circle) ===
def sea_distance(from_port, to_port):
    return geodesic(ports[from_port], ports[to_port]).km


# === 🧠 Route Planner ===
def plan_route(source, destination):
    print(f"\n🔍 Calculating route from {source} to {destination}...\n")

    # Get coordinates
    src_lat, src_lng = get_lat_lng(source)
    dst_lat, dst_lng = get_lat_lng(destination)

    # Nearest ports
    src_port = find_nearest_port(src_lat, src_lng)
    dst_port = find_nearest_port(dst_lat, dst_lng)

    # Road to first port
    road_to_port_km, time_to_port_hr = get_road_distance(source, port_address_map[src_port])

    # Sea distance
    sea_km = sea_distance(src_port, dst_port)
    sea_speed_kmph = 37  # avg cargo ship ~20 knots
    sea_time_hr = sea_km / sea_speed_kmph

    # Road from last port
    road_from_port_km, time_from_port_hr = get_road_distance(port_address_map[dst_port], destination)

    # === 📦 Final Output ===
    print("🧭 Route Summary:")
    print(f"  🛣  Road: {source} → {src_port} Port = {road_to_port_km:.2f} km ({time_to_port_hr:.2f} hrs)")
    print(f"  🚢  Sea: {src_port} Port → {dst_port} Port = {sea_km:.2f} km ({sea_time_hr:.2f} hrs)")
    print(f"  🛣  Road: {dst_port} Port → {destination} = {road_from_port_km:.2f} km ({time_from_port_hr:.2f} hrs)")

    total_dist = road_to_port_km + sea_km + road_from_port_km
    total_time = time_to_port_hr + sea_time_hr + time_from_port_hr

    print("\n🌊 Full Route:")
    print(f"{source} → {src_port} → {dst_port} → {destination}")
    print(f"\n📏 Total Distance: {total_dist:.2f} km")
    print(f"⏱ Estimated Time: {total_time:.2f} hours")


# === 🚀 Run It ===
if __name__ == "__main__":
    src = input("Enter Source Location: ")
    dst = input("Enter Destination Location: ")
    plan_route(src, dst)
