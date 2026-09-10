import argparse
import datetime
import math
import socket
import sys
import threading
import time

import numpy as np
import psutil
from IP_trace import map_nodes_to_ips

snr_values = {}
data_rate_values = {}
data_rate_values_look_up_table = {}
# total_data_received = {}  # New dictionary to keep track of total data

total_data_received = {"1": 0, "2": 0, "3": 0, "4": 0}

download_complete = 0
dataVolume = None
bs_received_data = None
alt_req = 0.0

# Dictionary to store previous data rates for each base station (keyed by host)
previous_datarates_at_UAV = {}


bs_data_volume = {
    "1": 0,  # data volume for LW1
    "2": 0,  # data volume for LW2
    "3": 0,  # data volume for LW3
    "4": 0,  # data volume for LW4
}


def collect_info_from_BSs(info):
    for bs_id, bs in info.items():
        send_request_to_bs(bs_id, bs["host"], bs["port"])


def send_request_to_bs(bs_id, host, port):
    global previous_datarates_at_UAV
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        client_socket.sendall(str(bs_id).encode("utf-8"))

        data = client_socket.recv(1024)
        data_str = data.decode("utf-8")
        # print('data_str: ', data_str)

        if data_str:  # If there's data received
            values = data_str.split(",")
            if len(values) > 1:  # Ensure there are at least two parts
                bs_ID = values[0]  # This is presumably not used, but can be checked if needed

                # Clean the string to remove unwanted characters and then convert to float
                snr_value_str = values[1].strip()  # Strip square brackets and extra spaces
                try:
                    snr_value = float(snr_value_str)
                    # print('BS',bs_id, 'SNR:',snr_value)
                    snr_values[bs_id] = snr_value
                except ValueError:
                    # print(f"Error: Could not convert SNR value '{snr_value_str}' to float.")
                    # snr_value_str = -99
                    snr_values[bs_id] = 0  # 0 or -99 but it shows 0 from GNU radio
            else:
                print(f"Error: Received unexpected data from {host}.")
        else:
            print(f"Empty value at {host}")

    except Exception as e:
        print(f"Error communicating with {host}: {e}")
        # pass
    finally:
        client_socket.close()


# Data rate
def get_spectral_efficiency(snr):
    if 21.0 <= snr < 22.7:
        return 5.12
    elif snr >= 22.7:
        return 5.55
    elif 18.7 <= snr < 21.0:
        return 4.52
    elif 16.3 <= snr < 18.7:
        return 3.90
    elif 14.1 <= snr < 16.3:
        return 3.32
    elif 11.7 <= snr < 14.1:
        return 2.73
    elif 10.3 <= snr < 11.7:
        return 2.41
    elif 8.1 <= snr < 10.3:
        return 1.91
    elif 5.9 <= snr < 8.1:
        return 1.48
    elif 4.3 <= snr < 5.9:
        return 1.18
    elif 2.4 <= snr < 4.3:
        return 0.88
    elif 0.2 <= snr < 2.4:
        return 0.60
    elif -2.3 <= snr < 0.2:
        return 0.38
    elif -4.7 <= snr < -2.3:
        return 0.23
    elif -6.7 <= snr < -4.7:
        return 0.15
    else:
        return 0.0


def read_volumes_from_file(file_path):
    """Read data volumes from a file. Each line corresponds to a BS."""
    try:
        with open(file_path) as file:
            volumes = [float(line.strip()) for line in file.readlines()]
        return volumes
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def distribute_volumes(volumes, num_lws):
    """Distribute data volumes to LWs (including LW1)."""
    global dataVolume
    if len(volumes) < num_lws:
        print("Error: Not enough data volumes provided for all LWs.")
        sys.exit(1)

    # lw_volumes = {f"LW{i+1}": volumes[i] for i in range(num_lws)}
    lw_volumes = {f"{i + 1}": volumes[i] for i in range(num_lws)}
    # lw1_dataVolume = volumes.get(1, -99)
    # lw2_dataVolume = volumes.get(2, -99)
    # lw3_dataVolume = volumes.get(3, -99)
    # lw4_dataVolume = volumes.get(4, -99)
    # lw_volumes = f'1:{lw1_dataVolume:.3f},2:{lw2_dataVolume:.3f},3:{lw3_dataVolume:.3f},4:{lw4_dataVolume:.3f}'
    # Convert dictionary to formatted string for the global variable
    # lw_volumes_str = ','.join([f"{key}:{value:.3f}" for key, value in lw_volumes.items()])

    dataVolume = lw_volumes
    return lw_volumes


def send_volumes_to_lws(lw_volumes):
    """Simulate sending volumes to LWs."""
    for lw, volume in lw_volumes.items():
        bs_data_volume[lw] = volume
        print(f"{volume} units of data to LW{lw}.")


def get_ip_address(interface_name):
    # Get network interface details
    addrs = psutil.net_if_addrs()

    if interface_name in addrs:
        for addr in addrs[interface_name]:
            # Check if the address family is IPv4
            if addr.family == 2:  # AF_INET (IPv4)
                return addr.address
    return None


def modify_ip(ip_address, increment_value=0):
    # Split the IP into its components
    ip_parts = ip_address.split(".")
    # Extract the last portion, convert to an integer, and add the increment value
    ip_parts[-1] = str(int(ip_parts[-1]) + increment_value)
    # Reconstruct the IP address and return it
    return ".".join(ip_parts)


# def calculate_shannon_capacity(snr_dB):
#    bandwidth_MHz = 1.4
#    snr_linear = 10 ** (snr_dB / 10)  # Convert SNR from dB to linear scale
#    bandwidth_Hz = bandwidth_MHz * 1e6  # Bandwidth in Hz
#    capacity = bandwidth_Hz * math.log2(1 + snr_linear)  # Shannon Capacity calculation
#    # capacity = bandwidth_Hz * math.log2(1 + snr_linear[0])
#    return capacity


def calculate_shannon_capacity(snr_dB):
    bandwidth_MHz = 1.4
    # print('checking........')
    snr_linear = 10 ** (snr_dB / 10)  # Convert SNR from dB to linear scale
    # print('SNR_Linear: ',snr_linear)
    # Ensure snr_linear is a scalar or extract the value if it's an array
    if isinstance(snr_linear, np.ndarray) and snr_linear.size == 1:
        snr_linear = snr_linear.item()

    bandwidth_Hz = bandwidth_MHz * 1e6  # Bandwidth in Hz
    capacity = bandwidth_Hz * math.log2(1 + snr_linear)  # Shannon Capacity calculation

    return capacity


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371 * 1000  # Radius of the Earth in meter
    return c * r


def calScore(uav_land_lat, uav_land_lon):
    time.sleep(0.5)
    global t1
    uav_land_lat = float(uav_land_lat)
    uav_land_lon = float(uav_land_lon)

    # Calculate the sum of total data volume and the sum of downloaded data
    total_volume_sum = sum(bs_data_volume[t] for t in ["1", "2", "3", "4"])
    downloaded_data_sum = sum(total_data_received[t] for t in ["1", "2", "3", "4"])
    D_down = downloaded_data_sum
    D_tot = total_volume_sum
    if D_down == D_tot:
        download_complete = 1
    else:
        download_complete = 0

    # # distance between land and launch position
    uav_launch_lat = 35.7274824  # 35.727311810013255
    uav_launch_lon = -78.6962749  # -78.69612244618433
    # delta_lat = uav_land_lat - uav_launch_lat #Calculate the differences in coordinates
    # delta_lon = uav_land_lon - uav_launch_lon
    # distance = math.sqrt(delta_lat ** 2 + delta_lon ** 2) # Calculate the Euclidean distance
    # distance = distance * 1000
    # print('Distance: ', distance)

    # # Convert angular distance to meters
    # lat_in_meters = delta_lat * 111000  # Convert latitude difference to meters
    # lon_in_meters = delta_lon * 111000 * math.cos(math.radians(uav_land_lat))  # Adjusting longitude for latitude
    # distance = math.sqrt(lat_in_meters ** 2 + lon_in_meters ** 2)  # Distance in meters
    # print("Distance in meters:", distance)

    ## Distance using haversine formula
    distance = haversine(uav_launch_lon, uav_launch_lat, uav_land_lon, uav_land_lat)
    # print("Distance (UAV current to launch) in meters:", distance)

    s1 = (600 - t1) * download_complete  # download_complete is either 0 or 1
    s2 = 100 * (D_down / D_tot)

    if distance <= 3:
        penalty = 0
    else:
        penalty = 20 * distance
    score = s1 + s2 - penalty
    print("Your score: ", score)
    return score


# Report Generation
def get_downloadReport(snr_value, bs_no):
    global bs_received_data

    if bs_no == "":
        report = "[Controller-->UAV] Please wait for the UAV to reach the desired altitude.;"
        print("[Controller-->UAV] Please wait for the UAV to reach the desired altitude.")
    else:
        # datarate = calculate_shannon_capacity(snr_value)  # data rate in bits per second
        # datarate_mb = datarate / 1e6
        # data_rate_values[bs_no] = datarate_mb

        # From lookup table......................
        spectral_efficiency = get_spectral_efficiency(snr_value)
        # data_rate_values_look_up_table[bs_no] = spectral_efficiency * 1.4  # bandwidth_MHz = 1.4
        datarate_mb = spectral_efficiency * 1.4  # bandwidth_MHz = 1.4

        volume = bs_data_volume.get(bs_no)

        if bs_no in total_data_received:
            if total_data_received[bs_no] == volume:
                pass
                # print(f'No data left for download from BS{bs_id}')
            else:
                total_data_received[bs_no] += datarate_mb  # Add the new data to the total
                # print(f"Updated total data received for {bs_no}: {total_data_received[bs_no]} Mbps")
        else:
            total_data_received[bs_no] = datarate_mb  # Initialize with the new data
            # print(f"Initializing new entry for {bs_no} with data: {datarate_mb} Mbps")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # print(f"Generated timestamp: {timestamp}")  # Debug print to check if we reach here
        snr = snr_value
        dr = total_data_received[bs_no]
        # ip_addr = host

        # Check if the total data received exceeds the volume limit
        if total_data_received[bs_no] > volume and total_data_received[bs_no] != volume:
            # Round down to the exact volume
            excess = total_data_received[bs_no] - volume
            total_data_received[bs_no] = volume
            # print(dr)
            # print(excess)
            # if dr > excess:  # Only adjust if there was excess data
            #    dr -= excess  # Reduce data rate by the excess amount
            # print(dr)
            datarate_mb = datarate_mb - excess
            report = f"[Controller-->UAV] Report: ts>{timestamp}, bs>{bs_no}, snr>{snr:.6f} db, rate>{datarate_mb:.2f} mbps, RECV>{total_data_received[bs_no]:.2f} mbits"
            print(f"[Controller-->UAV] Report: ts>{timestamp}, bs>{bs_no}, snr>{snr:.6f} db, rate>{datarate_mb:.2f} mbps, RECV>{total_data_received[bs_no]:.2f} mbits")
            # bs_received_data = f'1:{total_data_received['1']:.3f},2:{total_data_received['2']:.3f},3:{total_data_received['3']:.3f},4:{total_data_received['4']:.3f}'
            # bs_received_data = f"1:{total_data_received.get('1', 0.0):.3f},2:{total_data_received.get('2', 0.0):.3f},3:{total_data_received.get('3', 0.0):.3f},4:{total_data_received.get('4', 0.0):.3f}"
            bs_received_data = f"1:{total_data_received.get('1', 0.0):.2f},2:{total_data_received.get('2', 0.0):.2f},3:{total_data_received.get('3', 0.0):.2f},4:{total_data_received.get('4', 0.0):.2f}"
            # setDownloadedData(str(bs_received_data))  # Send the signal strengths
        else:
            if total_data_received[bs_no] == volume:
                print(f"[Controller-->UAV] Report: ts>{timestamp}. No data left for download from BS{bs_no}")
                report = f"[Controller-->UAV] Report: ts>{timestamp}. No data left for download from BS{bs_no}"
            else:
                print(f"[Controller-->UAV] Report: ts>{timestamp}, bs>{bs_no}, snr>{snr:.6f} db, rate>{datarate_mb:.2f} mbps, RECV>{total_data_received[bs_no]:.2f} mbits")
                report = f"[Controller-->UAV] Report: ts>{timestamp}, bs>{bs_no}, snr>{snr:.6f} db, rate>{datarate_mb:.2f} mbps, RECV>{total_data_received[bs_no]:.2f} mbits"
                bs_received_data = f"1:{total_data_received.get('1', 0.0):.2f},2:{total_data_received.get('2', 0.0):.2f},3:{total_data_received.get('3', 0.0):.2f},4:{total_data_received.get('4', 0.0):.2f}"
            # bs_received_data = f'1:{total_data_received['1']:.3f},2:{total_data_received['2']:.3f},3:{total_data_received['3']:.3f},4:{total_data_received['4']:.3f}'
            # setDownloadedData(str(bs_received_data))  # Send the signal strengths
    return report


sec_intv = 0


def connect_uav():
    global on_off, my_score, land_alt, sec_intv, stop
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 8005))
    server_socket.listen(5)  # Max connections
    print("Listening on port 8005 for UAV")

    stop_server = False
    # start_time3 = time.time()

    while not stop_server:
        if sec_intv != 0:
            print("....................................................")
        sec_intv = 1
        start_time3 = time.time()
        # print('.......1 sec interval........')
        # if on_off == 'on' or land_alt >= 0.1:
        if on_off == "on" or stop == 0:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=handle_client_uav, args=(client_socket,)).start()
            # elapsed_time = time.time() - start_time3
            # print('Elaspsed time: ',elapsed_time)
            # print(e)
            # if elapsed_time < 1:
            #    time.sleep(1 - elapsed_time)

            elapsed_time = time.time() - start_time3
            # print(f"Elapsed time: {elapsed_time:.6f} seconds")
            if elapsed_time < 1:
                sleep_time = abs(1 - elapsed_time - 0.0001)
                # print(f"Sleeping for {sleep_time:.6f} seconds to ensure 1-second gap")
                time.sleep(sleep_time)

        else:
            start_time2 = time.time()
            while time.time() - start_time2 < 30:  # Loop for 20 seconds
                print("....................................................")
                start_time4 = time.time()
                client_socket, addr = server_socket.accept()
                try:
                    # Receive data
                    data = client_socket.recv(1024).decode("utf-8")
                    if not data:  # Handle client disconnection
                        print("Client disconnected.")
                        break

                    # Respond to client
                    response = "[Controller-->UAV] The system is currently off;"
                    print(response)
                    client_socket.sendall(response.encode("utf-8"))

                    # time.sleep(1)  # Sleep for 1 second before sending again
                    elapsed_time = time.time() - start_time4
                    if elapsed_time < 1:
                        sleep_time = abs(1 - elapsed_time - 0.0001)

                except Exception as e:
                    print(f"Error handling client: {e}")
                    break  # Exit the loop if there's an error
                finally:
                    # Close the socket after the loop finishes
                    try:
                        client_socket.close()
                        # print("Socket closed.")
                    except Exception as e:
                        print(f"Error closing the socket: {e}")
            stop_server = True

            # # Close the socket after the loop finishes
            # try:
            # client_socket.close()
            # print("Socket closed.")
            # except Exception as e:
            # print(f"Error closing the socket: {e}")
            # break


msg_cnt = 0
cnt = 0
dcnt = 0
getSNR = 0
time_diff = 0
pause_time = 0
uav_req_time = 0


def handle_client_uav(client_socket):
    global cnt, t1, download_complete, land_alt, stop
    global alt_req, time_data_volume_shared, dcnt, getSNR, time_diff
    try:
        # print(f"UAV-->Controller: Send data from BS")

        # start_time3 = time.time()
        data = client_socket.recv(1024).decode("utf-8")
        print("[UAV-->Controller] Send SNR and Downloaded Data")

        # print(f"[UAV-->Controller] {data}")
        # print('Alt. requirement: ', alt_req)
        alt_req_numeric = float(alt_req)
        # if alt_req_numeric > 24:
        getSNR = 1
        # if (alt_req_numeric > 24 and t1 <= 500) or land_alt >=0.1:
        # if (alt_req_numeric > 24 and t1 <= 500) or stop == 0:
        if (alt_req_numeric > 24 and t1 <= 500) or stop == 0:  # initially altitue > 24, then access. but when lands, altitude reduces <24, then also access.
            # when altitude > 24. But when disarmed will stop
            # print('alt_req_numeric:', alt_req_numeric)
            # if (alt_req_numeric > 24 and t1 <= 500) or land_alt >=0 :  # May be need to change this condition if an experimenter changes altitude less than 24 m
            # land_alt --> if download not complete
            # print(f"UAV-->Controller: Send data from BS -> "data)
            # if not data:
            #    print("No data received from UAV.")
            #    client_socket.close()
            #    return
            # time.sleep(.001)
            snr_lw1 = snr_values.get(1, -99)
            snr_lw2 = snr_values.get(2, -99)
            snr_lw3 = snr_values.get(3, -99)
            snr_lw4 = snr_values.get(4, -99)
            all_bs_snr = f"1:{snr_lw1:.6f},2:{snr_lw2:.6f},3:{snr_lw3:.6f},4:{snr_lw4:.6f}"

            # dataVolumeWithSNR = f'vol#{dataVolume} snr#{all_bs_snr}'
            # print(f"Controller Received from UAV: {data}")
            # client_socket.sendall(dataVolumeWithSNR.encode('utf-8'))

            if cnt == 0:
                # separate by ; Don't separate with , as it is used already in snr
                data_volume_with_snr = f"vol:{dataVolume};snr:{all_bs_snr}"
                print(f"[Controller-->UAV] Vol:{dataVolume}")
                # print(f'[Controller-->UAV] SNR:{all_bs_snr}')
                print("[Controller-->UAV] SNR:")

                # Print each SNR value on a new line without repeating the label
                for snr in all_bs_snr.split(","):
                    print(snr)

                time_data_volume_shared = datetime.datetime.now()
                cnt = 1
            else:
                data_volume_with_snr = f"download:{bs_received_data};snr:{all_bs_snr}"
                # print(f'[Controller-->UAV] Download:{bs_received_data}')

                print("[Controller-->UAV] Download:")
                for rd in bs_received_data.split(","):
                    print(rd)

                # print(f'[Controller-->UAV] SNR:{all_bs_snr}')
                # Print each SNR value on a new line without repeating the label
                print("[Controller-->UAV] SNR:")
                for snr in all_bs_snr.split(","):
                    print(snr)
            try:
                # print(f"Controller Received from UAV: {data}")
                # print('data_volume_with_snr: ', data_volume_with_snr)
                if download_complete == 1 and dcnt == 0:
                    data_volume_with_snr = f"download_complete:{download_complete};snr:{all_bs_snr}"
                    dcnt = 1
                    # print('.....................................')
                client_socket.sendall(data_volume_with_snr.encode("utf-8"))
            except Exception as e:
                print(f"Error sending data: {e}")

            # print(f"UAV-->Controller: Send data from BS")

            # Continue with the rest of your code

            #            time.sleep(.01)
            # time.sleep(1)
            bs_no = client_socket.recv(1024).decode("utf-8")
            # time.sleep(0.2)
            # print(bs_no)
            print(f"[UAV-->Controller] Send data from BS{bs_no}")
            if not bs_no:
                print("No BS number received from UAV.")
                client_socket.close()
                return

            # Handle BS number and generate report
            if bs_no == "1":
                report = get_downloadReport(snr_lw1, bs_no)  # Ensure this function is implemented correctly
            elif bs_no == "2":
                report = get_downloadReport(snr_lw2, bs_no)
            elif bs_no == "3":
                report = get_downloadReport(snr_lw3, bs_no)
            elif bs_no == "4":
                report = get_downloadReport(snr_lw4, bs_no)
            else:
                report = "Invalid BS Number"  # though should not happen, safe

            client_socket.sendall(report.encode("utf-8"))

            # time.sleep(1)
            # exactly 1 second pause
            # while (time.time() - uav_req_time) < 1:
            #    pause_time = time.time()
            #    pass  # This loop just waits
        else:
            report = "[Controller-->UAV] Cannot share now. Please wait for the UAV to reach the desired altitude.;"
            print("[Controller-->UAV] Cannot share now. Please wait for the UAV to reach the desired altitude.")
            bs_no = client_socket.sendall(report.encode("utf-8"))

            #           time.sleep(0.2)
            # time.sleep(1)
            bs_no = client_socket.recv(1024).decode("utf-8")
            # print("[UAV-->Controller] BS seleciton: ", bs_no)
            report = "[Controller-->UAV] Please wait for the UAV to reach the desired altitude."
            print("[Controller-->UAV] Please wait for the UAV to reach the desired altitude.")
            client_socket.sendall(report.encode("utf-8"))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def connect_OEO():
    global on_off
    server_socket_oeo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket_oeo.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket_oeo.bind(("", 8006))
    server_socket_oeo.listen(5)  # max connection
    print("\nListening on port 8006 for OEO")
    # i  = 0
    while True:
        if on_off == "on":  # or on_off =='off':
            client_socket_oeo, addr = server_socket_oeo.accept()
            threading.Thread(target=handle_client_oeo, args=(client_socket_oeo,)).start()
        else:
            start_time2 = time.time()

            while time.time() - start_time2 < 15:
                print("No action needed. System is currently off.")
                time.sleep(0.1)

            break
            # print('                              ')
            # time.sleep(.2)
            # if i <= 10:
            # print('                                                             ')
            # i= i+1


alt_value = 0
start_time = None
cnt_for_st = 0
cnt_for_st2 = 0
# flight_time = datetime.timedelta(minutes=10) # 10 minutes
time_max_download = 500  # datetime.timedelta(seconds=500) # 10 minutes
# print('Max download time: ', time_max_download, ' seconds')
flg = 0
flg2 = 0
flg3 = 0
lat_value = 0
lon_value = 0
rtl_value = "0"
land_value = "0"
t1 = 0
on_off = "on"
my_score = 0
download_complete = 0
time_data_volume_shared = None
time_data_download_complete = datetime.datetime.max
dCnt = 0
cnt1 = 0
stop = -99
land_alt = -99
land_alt2 = 99


# arm_value = 0
def handle_client_oeo(client_socket_oeo):
    global alt_req, alt_value, time_data_volume_shared, time_data_download_complete  # , arm_value
    #    global alt_value
    global start_time, cnt_for_st, cnt_for_st2, flg, flg2, flg3, lat_value, lon_value, dCnt, stop
    global rtl_value, land_value, t1, on_off, my_score, download_complete, land_alt, land_alt2, cnt1
    try:
        # Receive the message from the client
        msg = client_socket_oeo.recv(1024).decode("utf-8")
        # print(f"Controller Received from OEO: {msg}")

        # Split the string by commas
        parts = msg.split(",")
        arm_value = 0
        # Loop through the parts and extract the value for 'alt'
        for part in parts:
            if part.startswith("alt:"):
                alt_value = float(part.split(":")[1])  # Extract value after 'alt:'
                # print('Alt_value: ',alt_value)
                if alt_value > 24 and cnt1 == 0:  # when alt>24, will not stop downlowading and cnt1=1 prevents the problem of downloading when armed
                    stop = 0
                    cnt1 = 1
            elif part.startswith("arm:"):
                arm_value = part.split(":")[1]  # Extract value after 'alt:'
                # print('Arm_value: ',arm_value)
                if arm_value == "1" and cnt_for_st == 0:
                    start_time = datetime.datetime.now()
                    # print('Start time: ', start_time)
                    # stop = 0
                    cnt_for_st = 1
                elif cnt_for_st == 1 and arm_value == "0":
                    cnt_for_st2 = 1
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  UAV has disarmed xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                # elif arm_value == '1':
                #    print('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
                # elif arm_value == '0':
                #    print('okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            elif part.startswith("rtl:"):
                rtl_value = part.split(":")[1]
                # print('RTL_value: ',rtl_value)
            elif part.startswith("land:"):
                land_value = part.split(":")[1]
                # print('RTL_value: ',rtl_value
            elif part.startswith("lat:"):
                lat_value = part.split(":")[1]
                # print('lat_value: ',lat_value)
            elif part.startswith("lon:"):
                lon_value = part.split(":")[1]
                # print('lon_value: ',lon_value)

            # if land_value == '1':
            # land_alt = alt_value
            # land_alt2 = alt_value
            if cnt_for_st == 1 and cnt_for_st2 == 1:  # will stop when disarmed
                stop = 1

        alt_req = alt_value
        # if start_time is not None:  # Ensure start_time is set
        if time_data_volume_shared is not None:
            # if flg == 0:
            # t1 = datetime.datetime.now() - time_data_volume_shared
            # t1 = t1.total_seconds()  # Convert to seconds
            # #print('T1: ', t1)

            # if t1 >= flight_time and flg == 0:
            total_volume_sum = sum(bs_data_volume[t] for t in ["1", "2", "3", "4"])
            downloaded_data_sum = sum(total_data_received[t] for t in ["1", "2", "3", "4"])
            D_down = downloaded_data_sum
            D_tot = total_volume_sum

            if D_down == D_tot:  # and dCnt == 0:
                download_complete = 1
                time_data_download_complete = datetime.datetime.now()
                # print('Time data download is complete: ', time_data_download_complete)
                # print('Download is complete')
                # time_data_download_complete = time_data_download_complete - time_data_volume_shared
                # time_data_download_complete = time_data_download_complete.total_seconds
                # dCnt = 1
            else:
                download_complete = 0
                # if D_down == D_tot:
                #    download_complete = 1
                # else:
                #    download_complete = 0

            if dCnt == 1:
                download_complete = 1
            # Ensure comparison between time (in seconds)
            # flight_time_seconds = flight_time.total_seconds()  # Convert flight_time to seconds
            # flight_time_seconds = flight_time.total_seconds()  # Convert flight_time to seconds

            # if (t1 >= time_max_download or download_complete == 1 or
            # (land_value == '1' or rtl_value == '1')) and flg == 0:
            # flg = 1
            # reply = 'rtl'
            # #reply = 'stop'
            # my_score = calScore(lat_value, lon_value)

            # on_off = 'off'

            # t_m = time_max_download #500 seconds
            # t_m = datetime.timedelta(seconds=time_max_download)  # convert 500 seconds to timedelta
            # t_m = datetime.timedelta(seconds=time_max_download)  # convert 500
            # t_d = min((t_m - t_a), t_c)

            t_a = time_data_volume_shared  # time stamp
            t_m = datetime.datetime.now()
            t_c = time_data_download_complete  # Inf. time: t_c:9999-12-31 23:59:59.999999 if not complete;
            t_d = min(t_m, t_c)
            t1 = (t_d - t_a).total_seconds()  # total download time in seconds # remains 500 seconds max
            # print(t1)
            # Calculate S1 and S2
            # s1 = (500 - t1) * download_complete #download_complete is either 0 or 1
            s1 = max(0, (500 - t1) * download_complete)
            s2 = 100 * (D_down / D_tot)
            score = s1 + s2
            # print(f't_a:{t_a}; t_m:{t_m}; t_c:{t_c}; t_d:{t_d}; t1:{t1}; s1: {s1}; s2:{s2}; score:{score} ')

            if t1 <= 500:
                if flg3 == 0:
                    reply = f"Download starts at {t_a}"
                    flg3 = 1
                    print(reply)
                # if download_complete == 0 and land_value == '1' and flg == 0: # Every second a message will be shown in the OEO console
                # if download_complete == 0 and land_value == '1' and land_alt2 <=0.1 and flg == 0:
                if download_complete == 0 and stop == 1 and flg == 0:
                    reply = f"T1: {t1:.2f} seconds, S1:{s1:.2f}, S2:{s2:.2f}, Score:{score:.2f}"
                    flg = 1
                    on_off = "off"
                    # time.sleep(.1)
                    print(reply)
                    print()
                elif download_complete == 1 and flg == 0:  # send only once to OEO console as download is complete.
                    reply = f"T1: {t1:.2f} seconds, S1:{s1:.2f}, S2:{s2:.2f}, Score:{score:.2f}"
                    flg = 1
                    on_off = "off"
                    # #time.sleep(.1)
                    print(reply)
                    print()
                else:  # Done. Nothing will be printed in OEO
                    reply = "None"
            else:
                if flg2 == 0:  # send only once to OEO console as time is expired.
                    reply = f"T1: {t1} seconds, S1:{s1:.2f}, S2:{s2:.2f}, Score:{score:.2f}"
                    on_off = "off"
                    flg2 = 1
                    # time.sleep(.1)
                    print(reply)
                    print()
                else:  # Done. Nothing will be printed in OEO
                    reply = "None"

        else:
            reply = "Start time not initialized."
            # print('Start time is not initialized as the UAV is not armed.')
        # Send a response back to the client (OEO)
        client_socket_oeo.sendall(reply.encode("utf-8"))
    except Exception as e:
        # Catch any exceptions and print an error message
        print(f"Error occurred: {e}")
        client_socket_oeo.sendall(f"Error: {e!s}".encode())  # Send the error message to the client

    finally:
        # Ensure the socket is always closed
        client_socket_oeo.close()


def run_servers():
    # # Start both servers in separate threads
    # threading.Thread(target=connect_OEO).start()
    # threading.Thread(target=connect_uav).start()
    threading.Thread(target=connect_OEO, daemon=True).start()
    threading.Thread(target=connect_uav, daemon=True).start()


if __name__ == "__main__":
    # #########################
    parser = argparse.ArgumentParser(description="LW1 as a controller")

    # Existing arguments
    parser.add_argument("--volumes", nargs="+", type=float, help="Data volumes for each LW")
    parser.add_argument("--file", type=str, help="Path to a file containing data volumes")
    parser.add_argument("--num_lws", type=int, default=4, help="Number of LWs (default is 4)")

    args = parser.parse_args()

    # Ensure either volumes or file is provided, but not both
    if args.volumes and args.file:
        print("Error: Provide either --volumes or --file, not both.")
        sys.exit(1)
    elif not args.volumes and not args.file:
        print("Error: You must provide data volumes using --volumes or --file.")
        sys.exit(1)

    # Get data volumes
    if args.volumes:
        volumes = args.volumes
    elif args.file:
        volumes = read_volumes_from_file(args.file)

    # Distribute volumes to LWs
    lw_volumes = distribute_volumes(volumes, args.num_lws)

    # Send volumes to LWs
    print("Data distribution:")
    send_volumes_to_lws(lw_volumes)

    # interface = "eth-XM-EVM"
    # ip_address = get_ip_address(interface)

    # uav_ip = modify_ip(ip_address, increment_value=-1)
    # lw1_ip = ip_address
    # lw2_ip = modify_ip(ip_address, increment_value=1)
    # lw3_ip = modify_ip(ip_address, increment_value=2)
    # lw4_ip = modify_ip(ip_address, increment_value=3)

    node_to_ip = map_nodes_to_ips()
    for node, ip in node_to_ip.items():
        # print(node, ':', ip)
        if node == "0":
            uav_ip = ip
        elif node == "LW1":
            lw1_ip = ip
        elif node == "LW2":
            lw2_ip = ip
        elif node == "LW3":
            lw3_ip = ip
        elif node == "LW4":
            lw4_ip = ip

    # Print the IP addresses
    # print("IP addresses: UAV:", uav_ip, " LW1:", lw1_ip, " LW2:", lw2_ip, " LW3:", lw3_ip, " LW4:", lw4_ip)

    bs_info = {
        1: {"host": lw1_ip, "port": 8001},
        2: {"host": lw2_ip, "port": 8002},
        3: {"host": lw3_ip, "port": 8003},
        4: {"host": lw4_ip, "port": 8004},
    }

    run_servers()

    while True:
        try:
            # if on_off == 'on' or on_off =='off':
            if getSNR == 1:
                collect_info_from_BSs(bs_info)
                getSNR = 0

            # time.sleep(0.7)  # This line must align with the above lines in the `try` block
        except Exception as e:
            print(f"Error: {e}")
