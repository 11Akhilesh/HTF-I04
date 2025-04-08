import json
from Roadways.roadway import get_road_route
from RailRoute.rail_route import get_rail_route
from SeaRoute.sea_routes import get_sea_route
from airways.airport import get_air_route


def aggregate_routes(source, destination):
    print("\n🧠 Aggregator: Collecting all possible routes...")

    all_routes = []

    try:
        road = get_road_route(source, destination)
        if road:
            all_routes.extend(road)
    except Exception as e:
        print(f"❌ Road error: {e}")

    try:
        rail = get_rail_route(source, destination)
        if rail:
            all_routes.extend(rail)
    except Exception as e:
        print(f"❌ Rail error: {e}")

    try:
        sea = get_sea_route(source, destination)
        if sea:
            all_routes.extend(sea)
    except Exception as e:
        print(f"❌ Sea error: {e}")

    try:
        air = get_air_route(source, destination)
        if air:
            all_routes.extend(air)
    except Exception as e:
        print(f"❌ Air error: {e}")

    return all_routes


def display_routes(routes):
    print("\n📦 Final Aggregated Route Options:")
    for idx, segment in enumerate(routes, 1):
        print(f"\n🔹 Route {idx}: [{segment['mode'].upper()}]")
        print(f"   From       : {segment['from']}")
        print(f"   To         : {segment['to']}")
        print(f"   Distance   : {segment['distance_km']} km")
        print(f"   Duration   : {segment['duration_hr']} hrs")
        print(f"   Cost       : ₹{segment['cost_inr']}")
        print(f"   Emissions  : {segment['emissions_kg']} kg CO₂")
        print(f"   Capacity OK: {segment['capacity_ok']}")
        print(f"   Source     : {segment['source_model']}")

    with open("aggregated_routes.json", "w") as f:
        json.dump(routes, f, indent=4)
        print("\n💾 Saved all routes to 'aggregated_routes.json'")


if __name__ == "__main__":
    print("🌐 Smart Transport Aggregator")
    src = input("Enter Source Location: ")
    dst = input("Enter Destination Location: ")

    routes = aggregate_routes(src, dst)

    if not routes:
        print("\n❌ No valid routes found by any model.")
    else:
        display_routes(routes)