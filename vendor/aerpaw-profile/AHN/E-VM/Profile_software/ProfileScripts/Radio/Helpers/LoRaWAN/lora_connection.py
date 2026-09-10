import logging
import time
from enum import IntEnum

from config import read_config_file
from logger import setup_logger
from serial.threaded import LineReader

"""

This Python script manages communication with a LoRaWAN device, automating network activation 
via OTAA (Over-The-Air Activation) or ABP (Activation By Personalization). It reads multiple 
parameters from `lora_config`, such as device keys, retry limits, and power settings, to 
dynamically configure the device. The script handles key tasks like setting up session keys, 
managing retries, and monitoring connection states using PySerial for serial communication. 
Responses from the device are processed to handle connection events, update states, and retry 
operations if needed. Additionally, it logs relevant information for debugging and ensures robust 
error handling. The `lora_config.txt` file,
located in /AERPAW-Dev/AHN/E-VM/Profile_software/ProfileScripts/Radio/Samples/LoRaWAN/SendPackageLostik/,
contains essential configuration parameters used by this script. For more details, visit: 
https://github.com/ronoth/LoStik/tree/master

Maintainer: Sergio Vargas, svargas3@ncsu.edu
last date updated: 04/02/2024

"""

lora_config = read_config_file("config.txt")
setup_logger()


class ConnectionState(IntEnum):
    SUCCESS = 0
    CONNECTING = 100
    CONNECTED = 200
    FAILED = 500
    TO_MANY_RETRIES = 520


class PrintLines(LineReader):
    retries = 0
    state = ConnectionState.CONNECTING
    response_buffer = []  # Buffer to store responses

    def retry(self, action):
        if self.retries >= lora_config["RETRIES"]:
            logging.info("Too many retries, exiting")
            self.state = ConnectionState.TO_MANY_RETRIES
            return
        self.retries = self.retries + 1
        action()

    def get_var(self, cmd):
        self.send_cmd(cmd)
        return self.transport.serial.readline()

    def join(self):
        if lora_config["JOIN_MODE"] == "abp":
            self.join_abp()
        elif lora_config["JOIN_MODE"] == "otaa":
            self.join_otaa()
        elif lora_config["JOIN_MODE"] == "none":
            logging.info("join mode disabled...")
            self.state = ConnectionState.CONNECTED

    def join_otaa(self):

        self.send_cmd("mac set appeui %s" % lora_config["APP_SESSION_KEY"])
        self.send_cmd("mac set appkey %s" % lora_config["NET_SESSION_KEY"])
        self.send_cmd("mac set deveui %s" % lora_config["DEVICE_ADDRESS"])
        self.send_cmd("mac join otaa")

    def join_abp(self):
        self.send_cmd("mac reset")
        self.send_cmd("mac set deveui %s" % lora_config["DEVICE_EUI"])
        self.send_cmd("mac set devaddr %s" % lora_config["DEVICE_ADDRESS"])
        self.send_cmd("mac set appskey %s" % lora_config["APP_SESSION_KEY"])
        self.send_cmd("mac set nwkskey %s" % lora_config["NET_SESSION_KEY"])
        self.send_cmd("mac get deveui")
        self.send_cmd("mac join abp")
        time.sleep(2)
        logging.info("Setting init variables...")
        self.send_cmd("mac set ar " + lora_config["ar"])
        self.send_cmd("mac set pwridx %d" % lora_config["pwridx"])
        #        self.send_cmd("mac set class " + lora_config['class'])
        self.send_cmd("mac set retx %d" % lora_config["retx"])
        self.send_cmd("mac set adr " + lora_config["adr"])
        logging.info("Done...")

    def connection_made(self, transport):
        logging.info("Connection to LoStik established")
        self.transport = transport
        self.retry(self.join)

    def handle_line(self, data):
        decoded_data = data.strip()
        logging.info("STATUS: %s" % decoded_data)
        self.response_buffer.append(decoded_data)

        if decoded_data == "denied" or decoded_data == "no_free_ch":
            logging.info("Retrying OTAA connection")
            self.retry(self.join)
        elif decoded_data == "accepted":
            logging.info("UPDATING STATE to connected")
            self.state = ConnectionState.CONNECTED

    def connection_lost(self, exc):
        if exc:
            logging.error(f"Serial port exception: {exc}")
        logging.error(f"Lost connection to LoRa serial device: {exc}")

    def send_cmd(self, cmd, delay=0.1):
        logging.info(cmd)
        self.transport.write(("%s\r\n" % cmd).encode("UTF-8"))
        time.sleep(delay)
        # Retrieve and return the last response
        return self.response_buffer.pop() if self.response_buffer else None
