import argparse

import matplotlib.pyplot as plt
import pandas as pd


def plot_rsrp(csv_path, plot_label, y_data):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], df[y_data], label="RSRP (dB)", color="blue", marker="o")

    plt.title("RSRP Over Time")
    plt.xlabel("Time")
    plt.ylabel("RSRP (dB)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot RSRP from CSV")
    parser.add_argument("csv", help="CSV file with RSRP data")
    parser.add_argument("--y_data", help="Data to plot on the Y axis")
    parser.add_argument("--plot_label", help="Label to put above the plot")
    args = parser.parse_args()

    plot_rsrp(args.csv, args.plot_label, args.y_data)
