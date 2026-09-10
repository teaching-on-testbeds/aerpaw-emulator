def getSignalStrengths():
    """
    Read a text file containing token:signalstrength pairs and return them as a dictionary.

    :param file_path: The path to the text file.
    :return: A dictionary with tokens as keys and signal strengths as values.
    """
    signal_strengths = {}

    try:
        with open("ss.txt") as file:
            line = file.readline().strip()  # Read the first line and strip whitespace
            if line:  # Check if the line is not empty
                pairs = line.split(",")  # Split the line by commas
                for pair in pairs:
                    token, strength = pair.split(":")  # Split each pair by colon
                    signal_strengths[token.strip()] = float(strength.strip())  # Convert strength to float and store in the dictionary

    except FileNotFoundError:
        print("Do you want to know the signal strength? Please wait for the controller's reply.")
        signal_strengths["1"] = -99
        signal_strengths["2"] = -99
        signal_strengths["3"] = -99
        signal_strengths["4"] = -99
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return signal_strengths
