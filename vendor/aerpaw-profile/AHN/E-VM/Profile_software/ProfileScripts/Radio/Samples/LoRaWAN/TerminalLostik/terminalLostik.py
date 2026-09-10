"""
This script is designed to interact with a LoRaWAN RN2903 module over a serial connection.
It provides a terminal interface for sending AT-style commands to the module, while also logging
all interactions and errors to a timestamped log file.

The script performs the following actions:
1. Retrieves environment variables to determine the configuration directory and logging paths.
2. Dynamically constructs and inserts paths to shared helper modules, including a custom logger.
3. Reads LoRa configuration settings (serial port, baud rate) from a 'config.txt' file.
4. Sets up logging with a customizable prefix and filename for organized session logging.
5. Opens a serial connection to the RN2903 module using the configured port and baud rate.
6. Initializes a threaded reader to manage serial responses asynchronously.
7. Enters a loop that:
   - Checks LoRaWAN connection state.
   - Prompts the user for input commands.
   - Sends the input to the module via serial.
   - Logs command activity and errors for debugging and traceability.

Maintainer: Sergio Vargas <svargas3@ncsu.edu>
Last updated: 04-09-25
"""

import logging
import os
import sys
import time

import serial

# Resolve logging environment variables
results_dir = os.getenv("RESULTS_DIR")
log_prefix = os.getenv("LOG_PREFIX")
log_suffix = "lostik_logger.txt"
log_filename = f"{log_prefix}_{log_suffix}"
log_file_path = os.path.join(results_dir, log_filename)

# Resolve PROFILE_DIR to access helpers (and logger)
profile_dir = os.getenv("PROFILE_DIR")
if not profile_dir:
    raise OSError("The environment variable 'PROFILE_DIR' is not set.")

helpers_path = os.path.join(profile_dir, "ProfileScripts", "Radio", "Helpers", "LoRaWAN")
sys.path.insert(0, os.path.abspath(helpers_path))

from logger import setup_logger

setup_logger(log_file_path)
logging.info("Logger initialized. Log file path: %s", log_file_path)

profile_dir = os.getenv("PROFILE_DIR")
if not profile_dir:
    raise OSError("The environment variable 'PROFILE_DIR' is not set.")

helpers_path = os.path.join(profile_dir, "ProfileScripts", "Radio", "Helpers", "LoRaWAN")
sys.path.insert(1, os.path.abspath(helpers_path))

from config import read_config_file
from lora_connection import ConnectionState, PrintLines
from serial.threaded import ReaderThread

#  Serial config
config = read_config_file("config.txt")
ser = serial.Serial(config["LORA_PORT"], baudrate=config["LORA_BAUD"])

#  LoRaWAN terminal loop
with ReaderThread(ser, PrintLines) as protocol:
    time.sleep(2)
    logging.info("Entered LoRaWAN command loop.")
    while True:
        if protocol.state != ConnectionState.CONNECTED:
            logging.info("Not connected to LoRaWAN Network...")
            time.sleep(1)
            continue
        try:
            test = input("waiting for RN2903 command\n")
            logging.info(f"Sending command: {test}")
            protocol.send_cmd(test)
        except Exception as e:
            logging.error(f"Exception: {e}")
            time.sleep(5)
            sys.exit(1)
