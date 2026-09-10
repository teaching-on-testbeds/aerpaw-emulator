import json


def extract_waypoints(plan_file):
    # Load the plan file which is in JSON-like format
    print(type(plan_file))
    with open(plan_file) as f:
        data = json.load(f)

    # Check if 'mission' and 'items' are present in the data
    if "mission" in data and "items" in data["mission"]:
        waypoints = []
        for item in data["mission"]["items"]:
            if item["type"] == "SimpleItem":
                latitude = item["params"][4]
                longitude = item["params"][5]
                altitude = item["params"][6]
                waypoints.append({"latitude": latitude, "longitude": longitude, "altitude": altitude})
        return waypoints
    else:
        raise KeyError("The plan file does not contain the expected 'mission' or 'items' fields")


# Example usage
# plan_file = 'aadm.plan'  # Replace with the actual plan file path
# default_waypoints = extract_waypoints(plan_file)
# print(default_waypoints)
