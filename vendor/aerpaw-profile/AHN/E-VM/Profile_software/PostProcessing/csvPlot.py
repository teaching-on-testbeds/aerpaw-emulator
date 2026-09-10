import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the Earth (specified in decimal degrees).
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of Earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


def plot_scatter(csv_file, x_column, y_column, y1_color="b", y2_color="r"):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    lon_column = "Longitude"
    lat_column = "Latitude"

    # Check if the columns exist in the CSV
    if x_column not in data.columns or y_column not in data.columns or lon_column not in data.columns or lat_column not in data.columns:
        print(f"Columns '{x_column}', '{y_column}', '{lon_column}', or '{lat_column}' not found in the CSV file.")
        return

    # Define starting position
    start_lon = data[lon_column].iloc[0]
    start_lat = data[lat_column].iloc[0]

    # Calculate distances from the starting position
    data["distance"] = data.apply(lambda row: haversine(start_lon, start_lat, row[lon_column], row[lat_column]) * 100, axis=1)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.scatter(data[x_column], data[y_column], color=y1_color, label=y_column, s=0.8)
    plt.scatter(data[x_column], data["distance"], color=y2_color, label="distance", s=0.8)
    plt.xlabel(x_column)
    plt.title(f"{y_column}(y1) and distance(y2) vs {x_column}")
    plt.grid(False)
    plt.legend()
    plt.show()


def plot_line(csv_file, x_column, y_column, y1_color="b", y2_color="r"):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    lon_column = "Longitude"
    lat_column = "Latitude"

    # Check if the columns exist in the CSV
    if x_column not in data.columns or y_column not in data.columns or lon_column not in data.columns or lat_column not in data.columns:
        print(f"Columns '{x_column}', '{y_column}', '{lon_column}', or '{lat_column}' not found in the CSV file.")
        return

    # Define starting position
    start_lon = data[lon_column].iloc[0]
    start_lat = data[lat_column].iloc[0]

    # Calculate distances from the starting position
    data["distance"] = data.apply(lambda row: (haversine(start_lon, start_lat, row[lon_column], row[lat_column]) * 100 - 35) * -1, axis=1)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    plt.plot(data[x_column], data[y_column], color=y1_color, label=y_column)
    plt.plot(data[x_column], data["distance"], color=y2_color, label="distance")
    plt.xlabel(x_column)
    plt.title(f"{y_column}(y1) and distance(y2) vs {x_column}")
    plt.grid(False)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot CSV data with Matplotlib.")
    parser.add_argument("logfile", type=str, help="Log file for CSV")
    parser.add_argument("-x", "--x_axis", default="time", help="Graph x axis")
    parser.add_argument("-y", "--y_axis", help="Graph y axis")
    parser.add_argument("-t", "--graph_type", type=str, default="scatter", help="The type of graph to be made (scatter/line)")
    parser.add_argument("--y1_color", default="b", help="x axis color")

    parser.add_argument("--y2_color", default="r", help="y axis color")

    args = parser.parse_args()

    if args.graph_type == "scatter":
        plot_scatter(args.logfile, args.x_axis, args.y_axis, y1_color=args.y1_color, y2_color=args.y2_color)
    elif args.graph_type == "line":
        plot_line(args.logfile, args.x_axis, args.y_axis, y1_color=args.y1_color, y2_color=args.y2_color)
    else:
        raise ValueError("Invalid graph type")
