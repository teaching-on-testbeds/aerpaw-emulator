def getDownloadData():
    data_download = {}

    try:
        with open("dd.txt") as file:
            line = file.readline().strip()  # Read the first line and strip whitespace
            if line:  # Check if the line is not empty
                pairs = line.split(",")  # Split the line by commas
                for pair in pairs:
                    bs_id, download = pair.split(":")  # Split each pair by colon
                    data_download[bs_id.strip()] = float(download.strip())
    except FileNotFoundError:
        print("Do you want to know the downloaded data? Please wait for the controller's reply.")
        data_download["1"] = 0
        data_download["2"] = 0
        data_download["3"] = 0
        data_download["4"] = 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return data_download
