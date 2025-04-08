import googlemaps
import math
from geopy.distance import geodesic
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')


# === Your Google Maps API Key ===
API_KEY = "AIzaSyBlC9_QicFifEy84f-XqgkKQ2IjyLFMYaM"
gmaps = googlemaps.Client(key=API_KEY)

# === All Major Indian Cargo Ports with Coordinates ===
ports = {
    "Deendayal Port Authority (Kandla)": (23.0333, 70.2167),
    "Paradip Port Authority": (20.3167, 86.6167),
    "Visakhapatnam Port Authority": (17.7041, 83.2977),
    "V.O. Chidambaranar Port Authority (Tuticorin)": (8.7642, 78.1348),
    "Cochin Port Authority (Kochi)": (9.9312, 76.2673),
    "New Mangalore Port Authority": (12.94416, 74.816899),
    "Chennai Port Authority": (13.0827, 80.2707),
    "Ennore Port Limited (Kamarajar Port)": (13.2516, 80.3268),
    "Jawaharlal Nehru Port Authority (Nhava Sheva)": (18.9633, 72.9510),
    "Mormugao Port Authority": (15.4095, 73.8057),
    "Mumbai Port Authority": (18.9498, 72.8355),
    "Syama Prasad Mookerjee Port Authority (Kolkata)": (22.5728, 88.3522),
    "Haldia Dock Complex": (22.0667, 88.0695),
    "Mundra Port": (22.8394, 69.7096),
    "Hazira Port": (21.1167, 72.6167),
    "Krishnapatnam Port": (14.25, 80.1333),
    "Port Pipavav": (20.9064, 71.5076),
    "Dhamra Port": (20.7966, 86.9064),
    "Karaikal Port": (10.8322, 79.8450),
    "Dahej Port": (21.7167, 72.5333),
    "Bedi Port": (22.4833, 70.0333),
    "Okha Port": (22.4667, 69.0700),
    "Porbandar Port": (21.6428, 69.6097),
    "Veraval Port": (20.9000, 70.3667),
    "Jafarabad Port": (20.8333, 71.3833),
    "Diu Port": (20.7133, 70.9833),
    "Navlakhi Port": (22.9667, 70.4500),
    "Sikka Port": (22.4333, 69.8500),
    "Vadinar Port": (22.4167, 69.3333),
    "Salaya Port": (22.3167, 69.6167),
    "Mandvi Port": (22.8333, 69.3500),
    "Rozi Port": (22.4667, 69.0667),
    "Ghogha Port": (21.6900, 72.2750),
    "Bhavnagar Port": (21.7625, 72.1517),
    "Dahanu Port": (19.9667, 72.7333),
    "Dighi Port": (18.3167, 73.1333),
    "Jaigarh Port": (17.2833, 73.2167),
    "Redi Port": (15.9667, 73.7167),
    "Vengurla Port": (15.8500, 73.6333),
    "Belekeri Port": (14.8167, 74.2333),
    "Karwar Port": (14.8117, 74.1211),
    "Gangavali Port": (14.7167, 74.1333),
    "Bhatkal Port": (13.9800, 74.5517),
    "Honnavar Port": (14.2817, 74.4417),
    "Kundapura Port": (13.6289, 74.6917),
    "Malpe Port": (13.3500, 74.7000),
    "Udupi Port": (13.3400, 74.7433),
    "Padubidri Port": (13.1500, 74.7667),
    "Mangalore Old Port": (12.8667, 74.8333),
    "Kozhikode Port": (11.2583, 75.7806),
    "Beypore Port": (11.1667, 75.8167),
    "Azhikode Port": (10.1833, 76.1833),
    "Quilon Port": (8.8833, 76.5917),
    "Neendakara Port": (8.9333, 76.5333),
    "Alappuzha Port": (9.5000, 76.3500),
    "Kayamkulam Port": (9.1667, 76.5000),
    "Thangassery Port": (8.8833, 76.5833),
    "Varkala Port": (8.7333, 76.7167),
    "Colachel Port": (8.1833, 77.2500),
    "Kanyakumari Port": (8.0833, 77.5500),
    "Rameswaram Port": (9.2833, 79.3167),
    "Pamban Port": (9.2889, 79.2083),
    "Nagapattinam Port": (10.7667, 79.8500),
    "Cuddalore Port": (11.7333, 79.7667),
    "Pondicherry Port": (11.9333, 79.8333),
    "Ennore Port": (13.2516, 80.3268),
    "Kattupalli Port": (13.2667, 80.3000),
    "Machilipatnam Port": (16.1833, 81.1333),
    "Nizampatnam Port": (15.9167, 80.7167),
    "Gangavaram Port": (17.6333, 83.2667),
    "Kalingapatnam Port": (18.3333, 84.0667),
    "Gopalpur Port": (19.2500, 84.9167),
    "Chandbali Port": (20.7667, 86.7333),
    "Astaranga Port": (20.2333, 86.1833),
    "Baitarani Port": (20.8333, 86.5167),
    "Balasore Port": (21.4944, 86.9300),
    "Contai Port": (21.7833, 87.7500),
    "Sagar Island Port": (21.6500, 88.0833)
}

# === Port Address Map (for better API results) ===
port_address_map = {
    "Deendayal Port Authority (Kandla)": "Kandla Port Trust, Gandhidham",
    "Paradip Port Authority": "Paradip Port Trust, Odisha",
    "Visakhapatnam Port Authority": "Visakhapatnam Port Trust, Andhra Pradesh",
    "V.O. Chidambaranar Port Authority (Tuticorin)": "V.O. Chidambaranar Port, Thoothukudi",
    "Cochin Port Authority (Kochi)": "Cochin Port Trust, Willingdon Island, Kochi",
    "New Mangalore Port Authority": "New Mangalore Port Trust, Mangaluru",
    "Chennai Port Authority": "Chennai Port Trust, Chennai",
    "Ennore Port Limited (Kamarajar Port)": "Ennore Port, Tamil Nadu",
    "Jawaharlal Nehru Port Authority (Nhava Sheva)": "Jawaharlal Nehru Port Trust, Navi Mumbai",
    "Mormugao Port Authority": "Mormugao Port, Goa",
    "Mumbai Port Authority": "Mumbai Port Trust, Mumbai",
    "Syama Prasad Mookerjee Port Authority (Kolkata)": "Kolkata Port Trust, Kolkata",
    "Haldia Dock Complex": "Haldia Port, West Bengal",
    "Mundra Port": "Mundra Port, Gujarat",
    "Hazira Port": "Hazira Port, Surat",
    "Krishnapatnam Port": "Krishnapatnam Port, Andhra Pradesh",
    "Port Pipavav": "Pipavav Port, Gujarat",
    "Dhamra Port": "Dhamra Port Trust, Odisha",
    "Karaikal Port": "Karaikal Port, Tamil Nadu",
    "Dahej Port": "Dahej Port, Gujarat",
    "Bedi Port": "Bedi Port, Gujarat",
    "Okha Port": "Okha Port, Gujarat",
    "Porbandar Port": "Porbandar Port, Gujarat",
    "Veraval Port": "Veraval Port, Gujarat",
    "Jafarabad Port": "Jafarabad Port, Gujarat",
    "Diu Port": "Diu Port, Daman and Diu",
    "Navlakhi Port": "Navlakhi Port, Gujarat",
    "Sikka Port": "Sikka Port, Gujarat",
    "Vadinar Port": "Vadinar Port, Gujarat",
    "Salaya Port": "Salaya Port, Gujarat",
    "Mandvi Port": "Mandvi Port, Gujarat",
    "Rozi Port": "Rozi Port, Gujarat",
    "Ghogha Port": "Ghogha Port, Gujarat",
    "Bhavnagar Port": "Bhavnagar Port, Gujarat",
    "Dahanu Port": "Dahanu Port, Maharashtra",
    "Dighi Port": "Dighi Port, Maharashtra",
    "Jaigarh Port": "Jaigarh Port, Maharashtra",
    "Redi Port": "Redi Port, Maharashtra",
    "Vengurla Port": "Vengurla Port, Maharashtra",
    "Belekeri Port": "Belekeri Port, Karnataka",
    "Karwar Port": "Karwar Port, Karnataka",
    "Gangavali Port": "Gangavali Port, Karnataka",
    "Bhatkal Port": "Bhatkal Port, Karnataka",
    "Honnavar Port": "Honnavar Port, Karnataka",
    "Kundapura Port": "Kundapura Port, Karnataka",
    "Malpe Port": "Malpe Port, Karnataka",
    "Udupi Port": "Udupi Port, Karnataka",
    "Padubidri Port": "Padubidri Port, Karnataka",
    "Mangalore Old Port": "Mangalore Old Port, Karnataka",
    "Kozhikode Port": "Kozhikode Port, Kerala",
    "Beypore Port": "Beypore Port, Kerala",
    "Azhikode Port": "Azhikode Port, Kerala",
    "Quilon Port": "Quilon Port, Kerala",
    "Neendakara Port": "Neendakara Port, Kerala",
    "Alappuzha Port": "Alappuzha Port, Kerala",
    "Kayamkulam Port": "Kayamkulam Port, Kerala",
    "Thangassery Port": "Thangassery Port, Kerala",
    "Varkala Port": "Varkala Port, Kerala",
    "Colachel Port": "Colachel Port, Tamil Nadu",
    "Kanyakumari Port": "Kanyakumari Port, Tamil Nadu",
    "Rameswaram Port": "Rameswaram Port, Tamil Nadu",
    "Pamban Port": "Pamban Port, Tamil Nadu",
    "Nagapattinam Port": "Nagapattinam Port, Tamil Nadu",
    "Cuddalore Port": "Cuddalore Port, Tamil Nadu",
    "Pondicherry Port": "Pondicherry Port, Puducherry",
    "Ennore Port": "Ennore Port, Tamil Nadu",
    "Kattupalli Port": "Kattupalli Port, Tamil Nadu",
    "Machilipatnam Port": "Machilipatnam Port, Andhra Pradesh",
    "Nizampatnam Port": "Nizampatnam Port, Andhra Pradesh",
    "Gangavaram Port": "Gangavaram Port, Andhra Pradesh",
    "Kalingapatnam Port": "Kalingapatnam Port, Andhra Pradesh",
    "Gopalpur Port": "Gopalpur Port, Odisha",
    "Chandbali Port": "Chandbali Port, Odisha",
    "Astaranga Port": "Astaranga Port, Odisha",
    "Baitarani Port": "Baitarani Port, Odisha",
    "Balasore Port": "Balasore Port, Odisha",
    "Contai Port": "Contai Port, West Bengal",
    "Sagar Island Port": "Sagar Island Port, West Bengal"
}


# ===  Get Lat/Lng of a Location ===
def get_lat_lng(place):
    geocode_result = gmaps.geocode(place)
    if not geocode_result:
        raise Exception(f"Could not find location: {place}")
    return geocode_result[0]["geometry"]["location"]["lat"], geocode_result[0]["geometry"]["location"]["lng"]

# ===  Find Nearest Port ===
def find_nearest_port(lat, lng):
    min_dist = float("inf")
    nearest = None
    for port, (plat, plng) in ports.items():
        dist = geodesic((lat, lng), (plat, plng)).km
        if dist < min_dist:
            min_dist = dist
            nearest = port
    return nearest

# ===  Get Road Distance Using Distance Matrix API ===
def get_road_distance(origin, destination):
    result = gmaps.distance_matrix(origin, destination, mode="driving")
    try:
        element = result["rows"][0]["elements"][0]
        dist_km = element["distance"]["value"] / 1000
        duration_hr = element["duration"]["value"] / 3600
        return dist_km, duration_hr
    except Exception as e:
        print("Distance Matrix API error:", result)
        raise Exception("Invalid route. Check input or API limits.")

# ===  Estimate Sea Distance (great-circle) ===
def sea_distance(from_port, to_port):
    return geodesic(ports[from_port], ports[to_port]).km

# ===  Route Planner ===
def plan_route(source, destination):
    print(f"\nCalculating hybrid sea-based route from {source} to {destination}...\n")

    try:
        # Get coordinates
        src_lat, src_lng = get_lat_lng(source)
        dst_lat, dst_lng = get_lat_lng(destination)

        # Nearest ports
        src_port = find_nearest_port(src_lat, src_lng)
        dst_port = find_nearest_port(dst_lat, dst_lng)

        if src_port == dst_port:
            print("Sea route not applicable (same source and destination port).")
            return None

        # Road distances
        road_to_port_km, time_to_port_hr = get_road_distance(source, port_address_map[src_port])
        road_from_port_km, time_from_port_hr = get_road_distance(port_address_map[dst_port], destination)

        # Sea distance and time
        sea_km = sea_distance(src_port, dst_port)
        sea_speed_kmph = 37
        sea_time_hr = sea_km / sea_speed_kmph
        
        # Cost & emissions (dummy values)
        road_cost_per_km = 5
        sea_cost_per_km = 2
        road_emission_per_km = 0.15
        sea_emission_per_km = 0.05

        segments = []

        segments.append({
            "mode": "road",
            "from": source,
            "to": f"{src_port} Port",
            "distance_km": round(road_to_port_km, 2),
            "duration_hr": round(time_to_port_hr, 2),
            "cost_inr": round(road_to_port_km * road_cost_per_km, 2),
            "emissions_kg": round(road_to_port_km * road_emission_per_km, 2),
            "capacity_ok": True,
            "source_model": "sea"
        })

        segments.append({
            "mode": "sea",
            "from": f"{src_port} Port",
            "to": f"{dst_port} Port",
            "distance_km": round(sea_km, 2),
            "duration_hr": round(sea_time_hr, 2),
            "cost_inr": round(sea_km * sea_cost_per_km, 2),
            "emissions_kg": round(sea_km * sea_emission_per_km, 2),
            "capacity_ok": True,
            "source_model": "sea"
        })

        segments.append({
            "mode": "road",
            "from": f"{dst_port} Port",
            "to": destination,
            "distance_km": round(road_from_port_km, 2),
            "duration_hr": round(time_from_port_hr, 2),
            "cost_inr": round(road_from_port_km * road_cost_per_km, 2),
            "emissions_kg": round(road_from_port_km * road_emission_per_km, 2),
            "capacity_ok": True,
            "source_model": "sea"
        })

        return segments

    except Exception as e:
        print(f"Route calculation failed: {e}")
        return None

def get_sea_route(source, destination):
    try:
        # Get coordinates
        src_lat, src_lng = get_lat_lng(source)
        dst_lat, dst_lng = get_lat_lng(destination)

        # Nearest ports
        src_port = find_nearest_port(src_lat, src_lng)
        dst_port = find_nearest_port(dst_lat, dst_lng)

        if src_port == dst_port:
            return None

        # Road to first port
        road_to_port_km, time_to_port_hr = get_road_distance(source, port_address_map[src_port])

        # Sea distance
        sea_km = sea_distance(src_port, dst_port)
        sea_speed_kmph = 37  # avg cargo ship ~20 knots
        sea_time_hr = sea_km / sea_speed_kmph

        # Road from last port
        road_from_port_km, time_from_port_hr = get_road_distance(port_address_map[dst_port], destination)

        segments = []

        # Road to port segment
        segments.append({
            "mode": "road",
            "from": source,
            "to": f"{src_port} Port",
            "distance_km": round(road_to_port_km, 2),
            "duration_hr": round(time_to_port_hr, 2),
            "cost_inr": round(road_to_port_km * 5, 2),
            "emissions_kg": round(road_to_port_km * 0.15, 2),
            "capacity_ok": True,
            "source_model": "sea"
        })

        # Sea segment
        segments.append({
            "mode": "sea",
            "from": f"{src_port} Port",
            "to": f"{dst_port} Port",
            "distance_km": round(sea_km, 2),
            "duration_hr": round(sea_time_hr, 2),
            "cost_inr": round(sea_km * 2, 2),
            "emissions_kg": round(sea_km * 0.05, 2),
            "capacity_ok": True,
            "source_model": "sea"
        })

        # Road from port segment
        segments.append({
            "mode": "road",
            "from": f"{dst_port} Port",
            "to": destination,
            "distance_km": round(road_from_port_km, 2),
            "duration_hr": round(time_from_port_hr, 2),
            "cost_inr": round(road_from_port_km * 5, 2),
            "emissions_kg": round(road_from_port_km * 0.15, 2),
            "capacity_ok": True,
            "source_model": "sea"
        })

        return segments
    except Exception as e:
        print(f" Sea route error: {e}")
        return None

# ===  Run It ===
if __name__ == "__main__":
    src = input("Enter Source Location: ")
    dst = input("Enter Destination Location: ")

    result = plan_route(src, dst)

    if result is None:
        print("No valid multi-modal route found.")
    else:
        print("\nFinal Route Segments (JSON):")
        print(json.dumps(result, indent=4))
