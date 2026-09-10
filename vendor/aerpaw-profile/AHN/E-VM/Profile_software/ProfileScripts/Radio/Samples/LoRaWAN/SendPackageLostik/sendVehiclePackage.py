"""
The provided code establishes a comprehensive system for real-time monitoring and transmission
of package number and timestamp data over LoRaWAN. Initially, the script configures a serial
reader thread to communicate with a LoStik device, ensuring seamless interaction for data exchange.
Subsequently, it sets up the LoRaWAN protocol, enabling transmission of packages to a designated
LoRa cloud server.

The core functionality revolves around continuous monitoring of a specified folder — in this case,
the AERPAW UAV Results folder — where a log file containing timestamp and package number data is
updated. Upon detecting new entries in the log file, the script parses the data (package_id +
timestamp) into Hexadecimal HEX format, generating a unique ID for post-processing.

The script dynamically adjusts the data rate for each transmission based on the configured range
specified in the config.txt file. The config.txt file also contains various parameters for device
operation, including session keys, device addresses, adaptive data rate settings, and more.

In cases where a "busy" status is returned multiple times (threshold defined in `max_busy_count`),
the script automatically restarts to ensure continuity in data transmission.

Maintainer: Sergio Vargas <svargas3@ncsu.edu>
Last updated: 2025-04-02
"""

# Import necessary modules
import logging
import os
import sys
import time

import serial

# Resolve log path using environment variables
results_dir = os.getenv("RESULTS_DIR")
log_prefix = os.getenv("LOG_PREFIX")
log_suffix = "lostik_tx.txt"
log_filename = f"{log_prefix}_{log_suffix}"
log_file_path = os.path.join(results_dir, log_filename)

# Resolve $PROFILE_DIR environment variable
profile_dir = os.getenv("PROFILE_DIR")
if not profile_dir:
    raise OSError("The environment variable 'PROFILE_DIR' is not set.")

# Construct the absolute path to the target directory where helpers (like logger.py) live
helpers_path = os.path.join(profile_dir, "ProfileScripts", "Radio", "Helpers", "LoRaWAN")

# Insert the helpers directory into sys.path to allow module imports
sys.path.insert(1, os.path.abspath(helpers_path))

from logger import setup_logger

# Set up logging using the custom logger (logs to both file and console)
setup_logger(log_file_path)
logging.info("Logger initialized. Log file path: %s", log_file_path)


# Import custom modules
from datetime import datetime

from config import read_config_file
from lora_connection import ConnectionState, PrintLines
from read_last_line_uav_results_folder import monitor_folder
from serial.threaded import ReaderThread

# Read configuration from config.txt
config = read_config_file("config.txt")

# Open a serial connection to the LoRaWAN device
ser = serial.Serial(config["LORA_PORT"], baudrate=config["LORA_BAUD"])

# Set the folder to watch for new UAV result logs
folder_to_watch = config["RESULTS_DIRECTORY"]
folder_monitor = monitor_folder(folder_to_watch)

# Initialize busy counter
busy_count = 0
max_busy_count = 3  # Threshold for restarting on repeated 'busy' responses


# Define a function to restart the script
def restart_script():
    logging.info("Restarting the script...")
    python = sys.executable
    os.execl(python, python, *sys.argv)


# Start the main loop with the ReaderThread for serial communication
with ReaderThread(ser, PrintLines) as protocol:
    time.sleep(2)

    # Set initial data rate
    dr = config["MIN_DR"]
    dr_delay = [2.5, 2.5, 2.5, 2.5, 2.5]  # Transmission delay per DR
    f_port = config["portno"]

    # Main execution loop
    while True:
        # Check if the device is connected to the LoRaWAN network
        if protocol.state != ConnectionState.CONNECTED:
            logging.info("Not Connected to LoRaWAN Network...")
            time.sleep(1)
            continue

        try:
            # Read the last line from the monitored UAV results folder
            last_line = next(folder_monitor)

            if last_line is not None:
                # Remove unnecessary characters for parsing
                last_line = last_line.replace('"', "").replace("(", "").replace(")", "")

                # Split the cleaned line into components using comma as the separator
                components = last_line.split(",")

                # Parse the timestamp (assuming it's at index 11)
                timestamp_obj = datetime.strptime(components[11], "%Y-%m-%d %H:%M:%S.%f")
                timestamp_ms = int(timestamp_obj.timestamp() * 1000)  # Convert to milliseconds

                # Extract and convert the package number to hexadecimal
                package_number = int(components[0])
                package_hex = hex(package_number)[2:]  # Remove '0x' prefix

                # Convert timestamp to hexadecimal
                timestamp_hex = hex(timestamp_ms)[2:]  # Remove '0x' prefix

                # Concatenate package number and timestamp in HEX format
                data_hex = package_hex + timestamp_hex

                # Log the generated message
                msg_to_log = f"Package number: {package_number} | Package HEX: {data_hex} | timestamp: {timestamp_ms} | DR: {dr}"
                logging.info(msg_to_log)

                # Set LoRaWAN data rate and transmit data
                protocol.send_cmd("mac set dr %d" % dr, 0.01)
                response = protocol.send_cmd(f"mac tx uncnf {f_port} {data_hex}", dr_delay[dr])

                # Update DR (loop between MIN and MAX)
                dr = dr + 1 if dr < config["MAX_DR"] else config["MIN_DR"]

                # Check for 'busy' status in the response
                if response and "busy" in response.lower():
                    busy_count += 1
                    logging.info(f"'busy' status received {busy_count} times")
                    if busy_count >= max_busy_count:
                        logging.info("Received 'busy' status 3 times - Restarting the script.")
                        restart_script()
                else:
                    busy_count = 0  # Reset on success

        except Exception as e:
            logging.error(f"Exception: {e}")
            time.sleep(5)
            sys.exit(1)
