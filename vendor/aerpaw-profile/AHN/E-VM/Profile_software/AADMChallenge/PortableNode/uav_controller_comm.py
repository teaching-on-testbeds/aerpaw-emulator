import socket
import time

import psutil
from IP_trace import map_nodes_to_ips

snr_values = {}
data_rate_values = {}
data_rate_values_look_up_table = {}

visited_bs = None

previous_datarates_at_UAV = {}

msg_cnt = 0
cnt = 0
time_pause = 0


def communicate_controller(host):
    global msg_cnt, cnt, time_pause
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # req_send_time = time_pause
        # print('req_send_time: ',req_send_time)

        client_socket.connect((host, 8005))
        print("[UAV-->Controller] Send SNR and Downloaded Data.")

        client_socket.sendall(b"snr_dd")
        data = client_socket.recv(1024)
        decoded_data = data.decode("utf-8")  # Decode bytes to string
        # print('Decode: ', decoded_data)

        try:
            # Split the decoded data into parts
            parts = decoded_data.split(";")

            # Process each part
            for part in parts:
                if part.startswith("snr:"):
                    # Process SNR
                    snr_clean = part.replace("snr:", "")
                    print(f"[Controller-->UAV] SNR:{snr_clean}")
                    setSignalStrengths(snr_clean)  # Make signal strengths visible to the experimenter

                elif part.startswith("vol:") or part.startswith("download:"):
                    # Identify the type (vol or download) and process
                    key = part.split(":")[0]
                    volumes_raw = part.replace(f"{key}:", "").replace("}", "").replace("'", "").strip("{}")
                    volumes_clean = ", ".join([f"{k.strip()}:{v.strip()}" for k, v in [item.split(":") for item in volumes_raw.split(",")]])

                    print(f"[Controller-->UAV] {key.capitalize()}:{volumes_clean}")

                    # Call the appropriate function
                    if key == "vol":
                        setDataVolume(volumes_clean)
                    elif key == "download":
                        setDownloadedData(volumes_clean)
                elif part.strip().startswith("download_complete:") and cnt == 0:
                    download_complete = part.replace("download_complete:", "")
                    # print('-------download complete: ', download_complete)
                    setBSForVehicleUse("-1")
                    cnt == 1
                    # msg_cnt == 1
                else:
                    print(part)

        except Exception as e:
            print(f"Error processing data_volume_with_snr: {e}")

        time.sleep(0.2)

        bs_id = getBSFromExperimenter()
        # print(bs_id)
        if not bs_id:  # This checks for None, empty string, or any falsy value
            bs_id = "1"
        print(f"[UAV-->Controller] Send data from BS{bs_id}")
        client_socket.sendall(bs_id.encode("utf-8"))
        data = client_socket.recv(1024)
        decoded_data = data.decode("utf-8")  # Decode bytes to string
        print(f"{decoded_data}")

        # exactly 1 second pause
        # time_pause = time.time()
        # while (time_pause = time_pause - req_send_time) < 1:
        # while (time.time() - req_send_time) < 1:
        #    time_pause = time.time()
        #    pass  # This loop just waits

    except Exception:
        # print(f"Error communicating with {host}: {e}")  # Kept previous SNR
        pass  # don't print anything
    finally:
        client_socket.close()


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


def setBSForVehicleUse(bs):
    with open("tn.txt", "w") as f:
        f.write(bs)


def setSignalStrengths(signalStrengths):
    with open("ss.txt", "w") as f:
        f.write(signalStrengths)


def setDataVolume(dataVolume):
    with open("dv.txt", "w") as f:
        f.write(dataVolume)


def setDownloadedData(downloadedData):
    with open("dd.txt", "w") as f:
        f.write(downloadedData)


def getBSFromExperimenter():
    try:
        with open("bc.txt") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: 'bc.txt' was not found.")
        return None  # Return None if the file does not exist
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None  # Handle any other exceptions


def reset_files():
    file_content_map = {
        "bc.txt": "",
        #'download_indicator.txt': '0',
        "tn.txt": "0",
        "dd.txt": "1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0",
        "dv.txt": "1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0",
        "ss.txt": "1: -99, 2: -99, 3: -99, 4: -99",
    }
    # Iterate over each file and write its corresponding content
    for file_name, content in file_content_map.items():
        with open(file_name, "w") as f:
            f.write(content)


if __name__ == "__main__":
    # interface = "eth-XM-EVM"
    # ip_address = get_ip_address(interface)
    # lw1_ip = modify_ip(ip_address, increment_value=1)
    # print(lw1_ip)

    node_to_ip = map_nodes_to_ips()
    # print(node_to_ip)

    # print("Node-to-IP Mapping (XM) in Target Order:")
    for node, ip in node_to_ip.items():
        if node == "LW1":
            lw1_ip = ip
            # print(f"{node}: {ip}")

    # print(lw1_ip)

    reset_files()

    while True:
        try:
            print("....................................................")
            start_time = time.time()
            communicate_controller(lw1_ip)
            elapsed_time = time.time() - start_time

            if elapsed_time < 1:
                time.sleep(1 - elapsed_time - 0.0001)

        except Exception as e:
            print(f"An error occurred while getting connected to controller: {e}")
            continue  # Skip to the next iteration if there's an error
