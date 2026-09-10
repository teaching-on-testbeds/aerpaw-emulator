def getDataVolumes():
    data_volumes = {}

    try:
        with open("dv.txt") as file:
            line = file.readline().strip()  # Read the first line and strip whitespace
            if line:  # Check if the line is not empty
                pairs = line.split(",")  # Split the line by commas
                for pair in pairs:
                    bs_id, volume = pair.split(":")  # Split each pair by colon
                    data_volumes[bs_id.strip()] = float(volume.strip())
    except FileNotFoundError:
        print("Do you want to know the data volume? Please wait for the controller's reply.")
        data_volumes["1"] = 0
        data_volumes["2"] = 0
        data_volumes["3"] = 0
        data_volumes["4"] = 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return data_volumes
