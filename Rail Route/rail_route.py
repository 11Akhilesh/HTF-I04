import requests

API_KEY = "AIzaSyBga1KLqo-AcAM_VdAlDwwAiSlHu0Mv_9E"

def fetch_route(start, end, mode, transit_mode=None):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": start,
        "destination": end,
        "key": API_KEY,
        "mode": mode,
        "alternatives": "false"
    }
    if mode == "transit" and transit_mode:
        params["transit_mode"] = transit_mode

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "OK":
        return None

    leg = data["routes"][0]["legs"][0]
    return {
        "mode": f"{mode} ({transit_mode})" if transit_mode else mode,
        "distance": leg["distance"]["text"],
        "duration": leg["duration"]["text"],
        "distance_value": leg["distance"]["value"],
        "duration_value": leg["duration"]["value"],
        "summary": data["routes"][0]["summary"]
    }

def compare_routes(start, end):
    print("\n🔎 Finding best route using road and rail...")

    road = fetch_route(start, end, mode="driving")
    rail = fetch_route(start, end, mode="transit", transit_mode="train")

    if not road and not rail:
        print("❌ No valid routes found.")
        return

    print("\n📊 Available Routes:")
    if road:
        print(f"🚗 Road: {road['distance']}, {road['duration']}, via {road['summary']}")
    else:
        print("🚗 Road: Not Available")

    if rail:
        print(f"🚆 Rail: {rail['distance']}, {rail['duration']}, via {rail['summary']}")
    else:
        print("🚆 Rail: Not Available")

    print("\n✅ Suggested Best Route:")
    if road and rail:
        best = min(road, rail, key=lambda r: r["duration_value"])
    else:
        best = road or rail

    print(f"👉 Mode: {best['mode']}")
    print(f"   Distance: {best['distance']}")
    print(f"   Duration: {best['duration']}")
    print(f"   Route Summary: {best['summary']}")

# 🧑‍💻 Input section
if __name__ == "__main__":
    print("🌍 Smart Multimodal Route Suggestion (Road vs Rail)")
    start_location = input("Enter Start Location: ")
    end_location = input("Enter End Location: ")
    compare_routes(start_location, end_location)
