import requests
import json
from geopy.distance import geodesic
import sys
sys.stdout.reconfigure(encoding='utf-8')


API_KEY = "AIzaSyDzggQCozVlD6dhbw5JJYi5YC6YWT_25FU"

# Sample freight-supporting railway junctions in India
FREIGHT_JUNCTIONS = [
{"name": "Howrah Junction", "lat": 22.5769, "lng": 88.3448},
{"name": "New Delhi", "lat": 28.6416, "lng": 77.2211},
{"name": "Chhatrapati Shivaji Maharaj Terminus", "lat": 18.9399, "lng": 72.8353},
{"name": "Chennai Central", "lat": 13.0827, "lng": 80.2753},
{"name": "Sealdah", "lat": 22.5667, "lng": 88.3703},
{"name": "Kanpur Central", "lat": 26.4499, "lng": 80.3319},
{"name": "Vijayawada Junction", "lat": 16.5194, "lng": 80.6304},
{"name": "Allahabad Junction", "lat": 25.4535, "lng": 81.8462},
{"name": "Itarsi Junction", "lat": 22.6148, "lng": 77.7596},
{"name": "Vadodara Junction", "lat": 22.3072, "lng": 73.1799},
{"name": "Lucknow Charbagh", "lat": 26.8450, "lng": 80.9431},
{"name": "Mughalsarai Junction", "lat": 25.2833, "lng": 83.1167},
{"name": "Bangalore City", "lat": 12.9784, "lng": 77.5900},
{"name": "Secunderabad Junction", "lat": 17.4364, "lng": 78.4983},
{"name": "Gorakhpur Junction", "lat": 26.7587, "lng": 83.3736},
{"name": "Patna Junction", "lat": 25.6119, "lng": 85.1361},
{"name": "Bhusaval", "lat": 21.0450, "lng": 75.7880},
{"name": "Chennai Egmore", "lat": 13.0693, "lng": 80.2638},
{"name": "Okhla", "lat": 28.5670, "lng": 77.2833},
{"name": "Barkakana", "lat": 23.7150, "lng": 85.9650},
{"name": "Ahmedabad Junction", "lat": 23.0300, "lng": 72.5800},
{"name": "Kharagpur Junction", "lat": 22.3300, "lng": 87.3200},
{"name": "Nagpur Junction", "lat": 21.1458, "lng": 79.0882},
{"name": "Bilaspur Junction", "lat": 21.2611, "lng": 82.1394},
{"name": "Jabalpur Junction", "lat": 23.1776, "lng": 79.9431},
{"name": "Bhopal Junction", "lat": 23.2599, "lng": 77.4029},
{"name": "Jaipur Junction", "lat": 26.9210, "lng": 75.8080},
{"name": "Ajmer Junction", "lat": 26.4514, "lng": 74.6399},
{"name": "Udaipur City", "lat": 24.5833, "lng": 73.6833},
{"name": "Surat", "lat": 21.1702, "lng": 72.8311},
{"name": "Rajkot Junction", "lat": 22.2989, "lng": 70.8022},
{"name": "Bhavnagar Terminus", "lat": 21.7625, "lng": 72.1517},
{"name": "Visakhapatnam Junction", "lat": 17.6868, "lng": 83.2185},
{"name": "Hyderabad Deccan", "lat": 17.3850, "lng": 78.4767},
{"name": "Warangal", "lat": 17.9900, "lng": 79.5900},
{"name": "Tirupati", "lat": 13.6355, "lng": 79.4192},
{"name": "Madurai Junction", "lat": 9.9252, "lng": 78.1198},
{"name": "Coimbatore Junction", "lat": 11.0139, "lng": 76.9558},
{"name": "Ernakulam Junction", "lat": 9.9717, "lng": 76.2933},
{"name": "Thiruvananthapuram Central", "lat": 8.4893, "lng": 76.9485},
{"name": "Kolkata Shalimar", "lat": 22.5650, "lng": 88.2700},
{"name": "Asansol Junction", "lat": 23.6736, "lng": 86.9480},
{"name": "Durgapur", "lat": 23.5233, "lng": 87.3167},
{"name": "Ranchi Junction", "lat": 23.3556, "lng": 85.3311},
{"name": "Jamshedpur", "lat": 22.7923, "lng": 86.1851},
{"name": "Bhagalpur", "lat": 25.2411, "lng": 86.9744},
{"name": "Muzaffarpur Junction", "lat": 26.1194, "lng": 85.3647},
{"name": "Darbhanga Junction", "lat": 26.1522, "lng": 85.8994},
{"name": "Guwahati", "lat": 26.1806, "lng": 91.7478},
{"name": "Dibrugarh", "lat": 27.4794, "lng": 94.9036},
{"name": "Siliguri Junction", "lat": 26.7099, "lng": 88.4289},
{"name": "Jodhpur Junction", "lat": 26.2793, "lng": 73.0239},
{"name": "Bikaner Junction", "lat": 28.0181, "lng": 73.3119},
{"name": "Kota Junction", "lat": 25.1825, "lng": 75.8390},
{"name": "Indore Junction", "lat": 22.7196, "lng": 75.8577},
{"name": "Ujjain Junction", "lat": 23.1774, "lng": 75.7850},
{"name": "Gwalior Junction", "lat": 26.2183, "lng": 78.1828},
{"name": "Agra Cantt", "lat": 27.1833, "lng": 77.9833},
{"name": "Mathura Junction", "lat": 27.4928, "lng": 77.6733},
{"name": "Aligarh Junction", "lat": 27.8980, "lng": 78.0800},
{"name": "Bareilly Junction", "lat": 28.3644, "lng": 79.4156},
{"name": "Moradabad Junction", "lat": 28.8417, "lng": 78.7667},
{"name": "Roorkee", "lat": 29.8547, "lng": 77.8889},
{"name": "Haridwar", "lat": 29.9450, "lng": 78.1644},
{"name": "Dehradun", "lat": 30.3244, "lng": 78.0339},
{"name": "Amritsar Junction", "lat": 31.6357, "lng": 74.8723},
{"name": "Ludhiana Junction", "lat": 30.9000, "lng": 75.8500},
{"name": "Jalandhar City", "lat": 31.3261, "lng": 75.5764},
{"name": "Chandigarh", "lat": 30.7333, "lng": 76.7794},
{"name": "Ambala Cantt", "lat": 30.3781, "lng": 76.8492},
{"name": "Kurukshetra Junction", "lat": 29.9767, "lng": 76.8311},
{"name": "Panipat Junction", "lat": 29.3889, "lng": 76.9683},
{"name": "Sonipat", "lat": 28.9944, "lng": 77.0189},
{"name": "Ghaziabad Junction", "lat": 28.6694, "lng": 77.4533},
{"name": "Faridabad", "lat": 28.4067, "lng": 77.3056},
{"name": "Gurgaon", "lat": 28.4600, "lng": 77.0264},
{"name": "Rewari Junction", "lat": 28.1989, "lng": 76.6200},
{"name": "Hisar Junction", "lat": 29.1450, "lng": 75.7211},
{"name": "Bhatinda Junction", "lat": 30.2194, "lng": 74.9483},
{"name": "Firozpur Cantt", "lat": 30.9367, "lng": 74.6167},
{"name": "Jammu Tawi", "lat": 32.7172, "lng": 74.8586},
{"name": "Udhampur", "lat": 32.9236, "lng": 75.1333},
{"name": "Srinagar", "lat": 34.0837, "lng": 74.7973},
{"name": "Kollam Junction", "lat": 8.8933, "lng": 76.5917},
{"name": "Trivandrum Pett", "lat": 8.4889, "lng": 76.9472},
{"name": "Kozhikode", "lat": 11.2583, "lng": 75.7806},
{"name": "Mangalore Junction", "lat": 12.9144, "lng": 74.8556},
{"name": "Hubli Junction", "lat": 15.3647, "lng": 75.1244},
{"name": "Belgaum", "lat": 15.8494, "lng": 74.4983},
{"name": "Dharwad", "lat": 15.4578, "lng": 75.0017},
{"name": "Solapur", "lat": 17.6711, "lng": 75.9100},
{"name": "Pune Junction", "lat": 18.5214, "lng": 73.8542},
{"name": "Nashik Road", "lat": 19.9511, "lng": 73.7917},
{"name": "Aurangabad", "lat": 19.8762, "lng": 75.3433},
{"name": "Akola Junction", "lat": 20.7094, "lng": 77.0211},
{"name": "Amravati", "lat": 20.9317, "lng": 77.7678},
{"name": "Raipur Junction", "lat": 21.2511, "lng": 81.6294},
{"name": "Durg", "lat": 21.1894, "lng": 81.2850},
{"name": "Bhilai", "lat": 21.2167, "lng": 81.4333},
{"name": "Rourkela", "lat": 22.2494, "lng": 84.8833},
{"name": "Sambalpur", "lat": 21.4667, "lng": 83.9833},
{"name": "Cuttack", "lat": 20.4617, "lng": 85.8828},
{"name": "Bhubaneswar", "lat": 20.2961, "lng": 85.8400},
{"name": "Puri", "lat": 19.8083, "lng": 85.8311},
{"name": "Berhampur", "lat": 19.3117, "lng": 84.7889},
{"name": "Balasore", "lat": 21.4944, "lng": 86.9300},
{"name": "Jamshedpur", "lat": 22.7923, "lng": 86.1851},
{"name": "Dhanbad Junction", "lat": 23.7994, "lng": 86.4300},
{"name": "Bokaro Steel City", "lat": 23.6694, "lng": 86.1494},
{"name": "Hazaribagh", "lat": 23.9917, "lng": 85.3611},
{"name": "Giridih", "lat": 24.1817, "lng": 86.3083},
{"name": "Deoghar", "lat": 24.4767, "lng": 86.6378},
{"name": "Gaya Junction", "lat": 24.7967, "lng": 85.0039},
{"name": "Buxar", "lat": 25.5744, "lng": 83.9789},
{"name": "Ara Junction", "lat": 25.5517, "lng": 84.6694},
{"name": "Sasaram", "lat": 24.9517, "lng": 83.9500},
{"name": "Varanasi Junction", "lat": 25.3189, "lng": 82.9733},
{"name": "Lucknow Junction", "lat": 26.8494, "lng": 80.9236},
{"name": "Agra Fort", "lat": 27.1833, "lng": 78.0167},
{"name": "Jaipur", "lat": 26.9156, "lng": 75.8183},
{"name": "Jodhpur", "lat": 26.2389, "lng": 73.0244},
{"name": "Bharatpur Junction", "lat": 27.2167, "lng": 77.4833},
{"name": "Alwar Junction", "lat": 27.5667, "lng": 76.6333},
{"name": "Sikar", "lat": 27.6111, "lng": 75.1394},
{"name": "Bhiwani", "lat": 28.7933, "lng": 76.1333},
{"name": "Rohtak Junction", "lat": 28.8950, "lng": 76.5944},
{"name": "Karnal", "lat": 29.6833, "lng": 76.9833},
{"name": "Ambala City", "lat": 30.3333, "lng": 76.8333},
{"name": "Pathankot Junction", "lat": 32.2644, "lng": 75.6528},
{"name": "Jalandhar Cantt", "lat": 31.3017, "lng": 75.5833},
{"name": "Hoshiarpur", "lat": 31.5322, "lng": 75.9094},
{"name": "Phagwara Junction", "lat": 31.2189, "lng": 75.7700},
{"name": "Kapurthala", "lat": 31.3800, "lng": 75.3833},
{"name": "Moga", "lat": 30.8167, "lng": 75.1667},
{"name": "Fazilka", "lat": 30.4028, "lng": 74.0289},
{"name": "Abohar", "lat": 30.1450, "lng": 74.1950},
{"name": "Sri Ganganagar", "lat": 29.9167, "lng": 73.8833},
{"name": "Hanumangarh Junction", "lat": 29.5833, "lng": 74.3333},
{"name": "Bikaner Cantt", "lat": 28.0350, "lng": 73.3233},
{"name": "Churu", "lat": 28.3000, "lng": 74.9667},
{"name": "Ratangarh Junction", "lat": 28.0833, "lng": 74.6167},
{"name": "Sardarshahar", "lat": 28.4433, "lng": 74.4917},
{"name": "Nokha", "lat": 27.5611, "lng": 73.4717},
{"name": "Nagaur", "lat": 27.2028, "lng": 73.7333},
{"name": "Merta Road Junction", "lat": 26.6483, "lng": 74.0333},
{"name": "Kishangarh", "lat": 26.5917, "lng": 74.8667},
{"name": "Sawai Madhopur", "lat": 26.0433, "lng": 76.3667},
{"name": "Dausa", "lat": 26.8939, "lng": 76.3361},
{"name": "Tonk", "lat": 26.1667, "lng": 75.7889},
{"name": "Bundi", "lat": 25.4389, "lng": 75.6417},
{"name": "Kota", "lat": 25.1825, "lng": 75.8390},
{"name": "Baran", "lat": 25.0989, "lng": 76.5144},
{"name": "Jhalawar City", "lat": 24.5967, "lng": 76.1650},
{"name": "Ratlam Junction", "lat": 23.3311, "lng": 75.0400},
{"name": "Neemuch", "lat": 24.4733, "lng": 74.8633},
{"name": "Mandsaur", "lat": 24.0717, "lng": 75.0694},
{"name": "Jaora", "lat": 23.6389, "lng": 75.1278},
{"name": "Dahod", "lat": 22.8333, "lng": 74.2500},
{"name": "Godhra Junction", "lat": 22.7817, "lng": 73.6167},
{"name": "Anand Junction", "lat": 22.5567, "lng": 72.9517},
{"name": "Nadiad Junction", "lat": 22.6944, "lng": 72.8700},
{"name": "Kheda", "lat": 22.7500, "lng": 72.6833},
{"name": "Mahesana Junction", "lat": 23.5989, "lng": 72.3917},
{"name": "Palanpur Junction", "lat": 24.1717, "lng": 72.4333},
{"name": "Abu Road", "lat": 24.4794, "lng": 72.7817},
{"name": "Sirohi Road", "lat": 24.8850, "lng": 72.8472},
{"name": "Pali Marwar", "lat": 25.7717, "lng": 73.3233},
{"name": "Sojat Road", "lat": 25.9244, "lng": 73.6667},
{"name": "Marwar Junction", "lat": 25.7333, "lng": 73.6167},
{"name": "Beawar", "lat": 26.1017, "lng": 74.3200},
{"name": "Nasirabad", "lat": 26.3044, "lng": 74.7333},
{"name": "Hubballi Junction (Shree Siddharoodha Swamiji)", "lat": 15.3647, "lng": 75.1244},
{"name": "Bangalore City Junction", "lat": 12.9784, "lng": 77.5900},
{"name": "Yesvantpur Junction", "lat": 13.0219, "lng": 77.5533},
{"name": "Mangalore Junction", "lat": 12.9144, "lng": 74.8556},
{"name": "Mysore Junction", "lat": 12.3083, "lng": 76.6528},
{"name": "Belgaum", "lat": 15.8494, "lng": 74.4983},
{"name": "Dharwad", "lat": 15.4578, "lng": 75.0017},
{"name": "Hospet Junction", "lat": 15.2689, "lng": 76.3889},
{"name": "Bellary Junction", "lat": 15.1389, "lng": 76.9172},
{"name": "Bijapur", "lat": 16.8200, "lng": 75.7167},
{"name": "Gadag Junction", "lat": 15.4294, "lng": 75.6294},
{"name": "Davangere", "lat": 14.4667, "lng": 75.9167},
{"name": "Hassan", "lat": 13.0122, "lng": 76.0967},
{"name": "Shimoga Town", "lat": 13.9294, "lng": 75.5678},
{"name": "Tumkur", "lat": 13.3417, "lng": 77.1017},
{"name": "Kolar", "lat": 13.1350, "lng": 78.1300},
{"name": "Chikballapur", "lat": 13.4333, "lng": 77.7167},
{"name": "Krishnarajapuram", "lat": 13.0061, "lng": 77.6792},
{"name": "Whitefield", "lat": 12.9694, "lng": 77.7494},
{"name": "Hosur", "lat": 12.7400, "lng": 77.8200},
{"name": "Karwar", "lat": 14.8117, "lng": 74.1211},
{"name": "Udupi", "lat": 13.3400, "lng": 74.7433},
{"name": "Kundapura", "lat": 13.6289, "lng": 74.6917},
{"name": "Honnavar", "lat": 14.2817, "lng": 74.4417},
{"name": "Bhatkal", "lat": 13.9800, "lng": 74.5517},
{"name": "Ankola", "lat": 14.6667, "lng": 74.3000},
{"name": "Canacona", "lat": 15.0100, "lng": 74.0500},
{"name": "Madgaon", "lat": 15.2767, "lng": 73.9611},
{"name": "Londa Junction", "lat": 15.4517, "lng": 74.5017},
{"name": "Castlerock", "lat": 15.4033, "lng": 74.3167},
{"name": "Alnavar Junction", "lat": 15.4250, "lng": 74.7350},
{"name": "Dandeli", "lat": 15.2667, "lng": 74.6167},
{"name": "Haliyal", "lat": 15.3333, "lng": 74.7500},
{"name": "Yellapur", "lat": 14.9667, "lng": 74.7167},
{"name": "Sirsi", "lat": 14.6167, "lng": 74.8333},
{"name": "Sagara", "lat": 14.1667, "lng": 75.0333},
{"name": "Chikmagalur", "lat": 13.3167, "lng": 75.7833},
{"name": "Holenarasipur", "lat": 12.8117, "lng": 76.2411},
{"name": "Arsikere Junction", "lat": 13.3117, "lng": 76.2611},
{"name": "Tiptur", "lat": 13.2567, "lng": 76.4778},
{"name": "Channapatna", "lat": 12.6533, "lng": 77.2083},
{"name": "Ramanagara", "lat": 12.7200, "lng": 77.2833},
{"name": "Mandya", "lat": 12.5217, "lng": 76.8994},
{"name": "Srirangapatna", "lat": 12.4167, "lng": 76.6833},
{"name": "Nanjangud Town", "lat": 12.1200, "lng": 76.6833},
{"name": "Chamarajanagar", "lat": 11.9250, "lng": 76.9417},
{"name": "Gokak", "lat": 16.1689, "lng": 74.8233},
{"name": "Athani", "lat": 16.7267, "lng": 75.0639},
{"name": "Bagalkot", "lat": 16.1833, "lng": 75.7000},
{"name": "Hospet", "lat": 15.2689, "lng": 76.3889},
{"name": "Koppal", "lat": 15.3500, "lng": 76.1533},
{"name": "Raichur", "lat": 16.2083, "lng": 77.3542}
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

def get_rail_route(source, destination):
    src_addr, src_coords = geocode_location(source)
    dst_addr, dst_coords = geocode_location(destination)

    if not src_coords or not dst_coords:
        return None

    nearest_src_jn = get_nearest_junction(src_coords)
    nearest_dst_jn = get_nearest_junction(dst_coords)

    segments = []

    # Road segment: source → source junction
    if source.lower() != nearest_src_jn["name"].lower():
        road1 = fetch_route(source, nearest_src_jn["name"])
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
    if destination.lower() != nearest_dst_jn["name"].lower():
        road2 = fetch_route(nearest_dst_jn["name"], destination)
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

    return segments

def main():
    print(" Rail Route Finder with Freight Junctions (Segment Format)")
    src_input = input("Enter Start Location: ")
    dst_input = input("Enter End Location: ")

    src_addr, src_coords = geocode_location(src_input)
    dst_addr, dst_coords = geocode_location(dst_input)

    if not src_coords or not dst_coords:
        print(" Failed to compute route: Location not found.")
        return

    nearest_src_jn = get_nearest_junction(src_coords)
    nearest_dst_jn = get_nearest_junction(dst_coords)

    print(f" Nearest Freight Junctions:")
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
        print("\n Final Route Segments (JSON):")
        print(json.dumps(segments, indent=4))
    else:
        print("No valid rail route found via freight junctions.")

if __name__ == "__main__":
    main()
