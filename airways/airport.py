import googlemaps
from geopy.distance import geodesic
from pprint import pprint

# 🔐 Google Maps API Key
API_KEY = "AIzaSyDzggQCozVlD6dhbw5JJYi5YC6YWT_25FU"  # Replace with your actual API key
gmaps = googlemaps.Client(key=API_KEY)

# ✈️ IATA to Airport Full Location Map
iata_to_location = {
    "DEL": "Indira Gandhi International Airport, Delhi",
    "HYD": "Rajiv Gandhi International Airport, Hyderabad",
    "MAA": "Chennai International Airport, Chennai",
    "BLR": "Kempegowda International Airport, Bengaluru",
    "BOM": "Chhatrapati Shivaji Maharaj International Airport, Mumbai",
    "CCU": "Netaji Subhas Chandra Bose International Airport, Kolkata",
    "GOI": "Goa International Airport, Goa",
    "PNQ": "Pune Airport, Pune",
    "AMD": "Sardar Vallabhbhai Patel International Airport, Ahmedabad",
    "JAI": "Jaipur International Airport, Jaipur",
    "LKO": "Chaudhary Charan Singh International Airport, Lucknow",
    "IXC": "Chandigarh Airport, Chandigarh",
    "TRV": "Trivandrum International Airport, Thiruvananthapuram",
    "COK": "Cochin International Airport, Kochi",
    "IXM": "Madurai Airport, Madurai",
    "NAG": "Nagpur Airport, Nagpur",
    "VGA": "Vijayawada International Airport, Vijayawada"
}

# 📍 Get Coordinates from Location
def get_lat_lng(place):
    geocode_result = gmaps.geocode(place)
    if not geocode_result:
        raise Exception(f"❌ Could not find location: {place}")
    loc = geocode_result[0]["geometry"]["location"]
    return loc["lat"], loc["lng"]

# 📏 Get Road Distance
def get_road_distance(origin, destination):
    result = gmaps.distance_matrix(origin, destination, mode="driving")
    try:
        element = result["rows"][0]["elements"][0]
        dist_km = element["distance"]["value"] / 1000
        duration_hr = element["duration"]["value"] / 3600
        return dist_km, duration_hr
    except:
        raise Exception(f"⚠️ Road distance error from {origin} to {destination}")

# 🔍 Find Nearest Airport to a Given Location
def find_nearest_airport(place):
    place_latlng = get_lat_lng(place)
    min_distance = float('inf')
    nearest_airport = None

    for airport_name in iata_to_location.values():
        airport_latlng = get_lat_lng(airport_name)
        dist = geodesic(place_latlng, airport_latlng).km
        if dist < min_distance:
            min_distance = dist
            nearest_airport = airport_name

    return nearest_airport

# 🧠 Route Planner (Road → Air → Road)
def plan_air_route(source_place, destination_place):
    print(f"\n📦 Calculating Road + Air route from {source_place} to {destination_place}...\n")

    # ✈️ Dynamically find nearest airports
    source_airport = find_nearest_airport(source_place)
    dest_airport = find_nearest_airport(destination_place)

    # 🚗 Road 1: Source to Source Airport
    road1_km, road1_hr = get_road_distance(source_place, source_airport)
    road1_cost = road1_km * 5
    road1_emissions = road1_km * 0.15

    # ✈️ Air: Between Airports
    src_lat, src_lng = get_lat_lng(source_airport)
    dst_lat, dst_lng = get_lat_lng(dest_airport)
    air_km = geodesic((src_lat, src_lng), (dst_lat, dst_lng)).km
    air_speed_kmph = 800
    air_time_hr = air_km / air_speed_kmph
    air_cost = 6 * air_km
    air_emissions = air_km * 0.125

    # 🚗 Road 2: Destination Airport to Final Place
    road2_km, road2_hr = get_road_distance(dest_airport, destination_place)
    road2_cost = road2_km * 5
    road2_emissions = road2_km * 0.15

    # 📊 Build Output List
    route = [
        {
            "mode": "road",
            "from": source_place,
            "to": source_airport,
            "distance_km": round(road1_km, 2),
            "duration_hr": round(road1_hr, 2),
            "cost_inr": int(road1_cost),
            "emissions_kg": round(road1_emissions, 2),
            "source_model": "air"
        },
        {
            "mode": "air",
            "from": source_airport,
            "to": dest_airport,
            "distance_km": round(air_km, 2),
            "duration_hr": round(air_time_hr, 2),
            "cost_inr": int(air_cost),
            "emissions_kg": round(air_emissions, 2),
            "source_model": "air"
        },
        {
            "mode": "road",
            "from": dest_airport,
            "to": destination_place,
            "distance_km": round(road2_km, 2),
            "duration_hr": round(road2_hr, 2),
            "cost_inr": int(road2_cost),
            "emissions_kg": round(road2_emissions, 2),
            "source_model": "air"
        }
    ]

    return route

# 🧪 Run the planner
if __name__ == "__main__":
    src = input("Enter Source Address (e.g., Mangalore): ")
    dst = input("Enter Destination Address (e.g., Delhi): ")
    result = plan_air_route(src, dst)
    pprint(result)
