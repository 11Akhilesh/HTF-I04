import googlemaps
from geopy.distance import geodesic

# === 🔐 Google Maps API Key ===
API_KEY = "AIzaSyDzggQCozVlD6dhbw5JJYi5YC6YWT_25FU"
gmaps = googlemaps.Client(key=API_KEY)

# === ✈️ IATA to Airport Full Location Map ===
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

# === 📍 Get Coordinates from Location ===
def get_lat_lng(place):
    geocode_result = gmaps.geocode(place)
    if not geocode_result:
        raise Exception(f"❌ Could not find location: {place}")
    loc = geocode_result[0]["geometry"]["location"]
    return loc["lat"], loc["lng"]

# === 📏 Get Road Distance ===
def get_road_distance(origin, destination):
    result = gmaps.distance_matrix(origin, destination, mode="driving")
    try:
        element = result["rows"][0]["elements"][0]
        dist_km = element["distance"]["value"] / 1000
        duration_hr = element["duration"]["value"] / 3600
        return dist_km, duration_hr
    except:
        raise Exception(f"⚠️ Road distance error from {origin} to {destination}")

# === 🧠 Route Planner (Road + Air + Road) ===
def plan_air_route(source_place, destination_place):
    print(f"\n📦 Calculating Road + Air route from {source_place} to {destination_place}...\n")

    # Get nearest airports (you can customize this further)
    source_iata = "DEL"  # Replace with logic if needed
    destination_iata = "MAA"  # Replace with logic if needed

    source_airport = iata_to_location[source_iata]
    dest_airport = iata_to_location[destination_iata]

    # Road 1: Source to Source Airport
    road1_km, road1_hr = get_road_distance(source_place, source_airport)

    # Air: Between Airports (we'll use geodesic)
    src_lat, src_lng = get_lat_lng(source_airport)
    dst_lat, dst_lng = get_lat_lng(dest_airport)
    air_km = geodesic((src_lat, src_lng), (dst_lat, dst_lng)).km
    air_speed_kmph = 800  # Average commercial flight speed
    air_time_hr = air_km / air_speed_kmph

    # Road 2: Destination Airport to Final Place
    road2_km, road2_hr = get_road_distance(dest_airport, destination_place)

    # === 📊 Output Summary ===
    print(f"🛣 Road: {source_place} → {source_airport} = {road1_km:.2f} km ({road1_hr:.2f} hrs)")
    print(f"✈️ Air: {source_airport} → {dest_airport} = {air_km:.2f} km ({air_time_hr:.2f} hrs)")
    print(f"🛣 Road: {dest_airport} → {destination_place} = {road2_km:.2f} km ({road2_hr:.2f} hrs)")

    total_km = road1_km + air_km + road2_km
    total_hr = road1_hr + air_time_hr + road2_hr

    print("\n🌐 Total Distance:", f"{total_km:.2f} km")
    print("⏱ Estimated Total Time:", f"{total_hr:.2f} hours")

# === 🧪 Run the planner ===
if __name__ == "__main__":
    src = input("Enter Source Address (e.g., Connaught Place, Delhi): ")
    dst = input("Enter Destination Address (e.g., T. Nagar, Chennai): ")
    plan_air_route(src, dst)
