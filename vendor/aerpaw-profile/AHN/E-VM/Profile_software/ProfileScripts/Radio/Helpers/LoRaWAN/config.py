"""
This function reads a configuration file and parses its contents into a dictionary. The file is
expected to have key-value pairs in the format `key=value`, with one pair per line. Lines starting
with `#` (comments) or empty lines are ignored. The function handles numeric values by converting
them to integers, while other values are stored as strings. The resulting dictionary can be used
to dynamically configure various aspects of an application. This approach ensures flexibility and
makes it easy to manage configurations in an external file.

Maintainer: Sergio Vargas, svargas3@ncsu.edu
last date updated: 04/02/2024


"""


def read_config_file(filename):
    # Create an empty dictionary to store the variables
    config_vars = {}

    # Open the file and read each line
    with open(filename) as f:
        lines = f.readlines()

    # Process each line
    for line in lines:
        # Ignore comments and empty lines
        if line.startswith("#") or line.strip() == "":
            continue

        # Split the line into variable and value
        var, val = line.split("=")

        # Store the variable and value in the dictionary
        val = val.strip()
        if val.isdigit():
            config_vars[var.strip()] = int(val)
        else:
            config_vars[var.strip()] = val

    return config_vars
