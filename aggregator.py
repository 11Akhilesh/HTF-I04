# hybrid_route_aggregator.py
import json
import subprocess
import sys


def get_base_model_output(script_path, args):
    process = subprocess.Popen([sys.executable, script_path],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True)

    # Send inputs as a single string
    input_data = "\n".join(args) + "\n"
    output, error = process.communicate(input=input_data)
    if error:
        print(f"Error from {script_path}:\n{error}")
    return output


def extract_json_segments(output):
    try:
        start = output.index("[")
        end = output.rindex("]") + 1
        json_str = output[start:end]
        return json.loads(json_str)
    except Exception as e:
        print("Failed to parse route segments:", e)
        return []


def calculate_score(route, weights):
    total = {"cost": 0, "time": 0, "emission": 0}
    for seg in route:
        total["cost"] += seg["cost_inr"]
        total["time"] += seg["duration_hr"]
        total["emission"] += seg["emissions_kg"]
    score = (weights["cost"] * total["cost"] +
             weights["time"] * total["time"] +
             weights["emission"] * total["emission"])
    return score, total


if __name__ == "__main__":
    source = input("Enter source location: ")
    destination = input("Enter destination location: ")
    length = input("Enter package length (cm): ")
    width = input("Enter package width (cm): ")
    height = input("Enter package height (cm): ")
    weight = input("Enter package weight (kg): ")

    print("\nGathering routes from all base models...\n")

    # Paths to base model scripts
    scripts = {
        "road": "./Roadways/roadway.py",
        "rail": "./RailRoute/rail_route.py",
        "sea": "./SeaRoute/sea_routes.py",
        "air": "./airways/airport.py"
    }

    # Collect all routes
    all_routes = []
    for mode, script in scripts.items():
        args = [source, destination]
        print(f"Calling {mode} model...")
        output = get_base_model_output(script, args)
        segments = extract_json_segments(output)
        if segments:
            all_routes.append({"mode": mode, "segments": segments})

    # Calculate 4 hybrid options
    optimization_weights = {
        "best": {"cost": 1, "time": 1, "emission": 1},
        "economic": {"cost": 3, "time": 1, "emission": 1},
        "fastest": {"cost": 1, "time": 3, "emission": 1},
        "emissionless": {"cost": 1, "time": 1, "emission": 3},
    }

    results = {}
    for key, weights in optimization_weights.items():
        best_score = float('inf')
        best_route = []
        for route in all_routes:
            score, _ = calculate_score(route["segments"], weights)
            if score < best_score:
                best_score = score
                best_route = route["segments"]
        results[key] = best_route

    print("\nOptimal Hybrid Routes (aggregated from base models):\n")
    print(json.dumps(results, indent=2))
    