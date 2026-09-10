#! /usr/bin/env python


import sys

sys.path.insert(0, "..")

import os
import re
import time

# import pandas as pd
from datetime import datetime

import serial
import serial.threaded

try:
    import queue
except ImportError:
    pass


import argparse

parser = argparse.ArgumentParser(description='Usage: sudo python at_rm500q.py -a "Broadband" -p /dev/ttyUSB2')
parser.add_argument("-a", "--apn", help="apn to be loaded", default="aerpaw1")
parser.add_argument("-p", "--usbpath", help="Specify USB port, else /dev/ttyUSB2 or USB3 (if ttyUSB2 fails) will be used, if otherwise specify", default="/dev/ttyUSB2")
args = parser.parse_args()
config = vars(args)

# test Main
if __name__ == "__main__":

    def command_to_serial_read_response(command_with_read):
        ser.close()
        ser.open()
        payload = bytes(command_with_read + "\r\n", "utf-8")
        # payload = bytes("ATI\r\n", 'utf-8')
        ser.write(payload)
        time.sleep(0.1)
        read_val = ser.read_until(expected=b"OK").decode("utf-8")
        # read_val = ser.read_until(expected=b"OK")
        return os.linesep.join([s for s in "".join(read_val.removesuffix("OK")).splitlines() if s])

    def sleep_countdown(timer_count):
        while timer_count:
            mins, secs = divmod(timer_count, 60)
            timer = f"{mins:02d}:{secs:02d}"
            print(timer, end="\r")
            sys.stdout.flush()
            time.sleep(1)
            timer_count -= 1

    # Start MAIN

    ser = serial.Serial("/dev/ttyUSB4", baudrate=115200, bytesize=8, timeout=1)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    rows, columns = os.popen("stty size", "r").read().split()
    # print(rows) ; print(columns)

    connected_string = "========CONNECTED"
    spaces = "=".join([""] * (int(columns) - len(connected_string) - 10))
    empty_print = spaces
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), connected_string, empty_print, end="\n")

    # System Info
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), end=" ")
    print("".join(command_to_serial_read_response("ATI")))
    print("IMEI:", command_to_serial_read_response("AT+GSN"), end=" ")
    print("IMSI:", command_to_serial_read_response("AT+CIMI"))

    # Initialize the Modem

    # Step1 Set right APN
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Set Provided or default APN:", args.apn)
    Var_PDP_Type = "IPV4V6"
    Var_APN = args.apn
    APN_string = 'AT+CGDCONT=1,"%s","%s"' % (Var_PDP_Type, Var_APN)
    command_to_serial_read_response(APN_string)

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Also set all bands")
    # Step2 Set all bands
    command_to_serial_read_response('AT+QNWPREFCFG= "lte_band",1:2:3:4:5:7:8:12:13:14:18:19:20:25:26:28:29:30:32:34:38:39:40:41:42:43:46:48:66:71')
    command_to_serial_read_response('AT+QNWPREFCFG= "nsa_nr5g_band",1:2:3:5:7:8:12:20:25:28:38:40:41:48:66:71:77:78:79')
    command_to_serial_read_response('AT+QNWPREFCFG= "nr5g_band",1:2:3:5:7:8:12:20:25:28:38:40:41:48:66:71:77:78:79')
    command_to_serial_read_response('AT+QNWPREFCFG= "mode_pref",AUTO')
    command_to_serial_read_response('AT+QNWPREFCFG="ue_usage_setting",1')
    command_to_serial_read_response('AT+QNWPREFCFG="nr5g_disable_mode",0')
    command_to_serial_read_response('AT+QNWCFG="csi_ctrl",1,1')

    # Set USBnet status
    command_to_serial_read_response('AT+QCFG="usbnet",2')

    # Operator status
    Var_current_operator_status_and_mode = command_to_serial_read_response("AT+COPS?")
    # print(Var_current_operator_status_and_mode)

    # Try register if no operator/ no registration
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " Operator selected:", re.findall(r"(?<=\+COPS\:...).*", Var_current_operator_status_and_mode)[0])
    except:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Quectel modem not registered to network, trying now..")
        exit()
        # Either not in auto mode or NW not found
        # Set COPS =0 & CREG=1
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Set Auto selection mode to YES and Registration status to 1 and wait ~5 mins")
        command_to_serial_read_response("AT+COPS=0")
        command_to_serial_read_response("AT+CREG=1")
        sleep_countdown(300)

    # Operator status
    Var_current_operator_status_and_mode = command_to_serial_read_response("AT+COPS?")
    # Verify after reregister
    try:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " Operator selected:", re.findall(r"(?<=\+COPS\:...).*", Var_current_operator_status_and_mode)[0])
    except:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Network registration Failure: Try again later or with different parameters")
        quit()

    ################################
    # If Registartion succesful
    # MT in Auto mode and nw found
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Network already selected, Re-registration not required")
    Selection_and_registration_status = 2

    # Post self registration check
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Enter logging state")

    ################################
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "BASIC Params")
    # Line1 Basic params
    Var_CREG = command_to_serial_read_response("AT+CREG?")  # ; Quectel_module.sleep_countdown(2)
    Var_CSQ = command_to_serial_read_response("AT+CSQ")  # ; Quectel_module.sleep_countdown(2)
    Var_QNWINFO = command_to_serial_read_response("AT+QNWINFO")  # ; Quectel_module.sleep_countdown(2)
    Var_QSPN = command_to_serial_read_response("AT+QSPN")  # Quectel_module.sleep_countdown(2)
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " ", re.search(r"(?<=\+).*", Var_CREG).group(0), end=" ")
    print(re.search(r"(?<=\+).*", Var_CSQ).group(0), end=" ")
    print(" ", Var_QSPN, " ", Var_QNWINFO)
    print("\n")
    print("Started Logging now")
