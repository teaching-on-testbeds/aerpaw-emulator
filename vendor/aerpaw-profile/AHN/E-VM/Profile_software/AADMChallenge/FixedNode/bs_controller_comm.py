import math
import socket

import numpy as np
import psutil
from IP_trace import map_nodes_to_ips
from read_measurement import read_snr_measurement

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


previous_dr = 0.0


def handle_client(client_socket):
    global previous_dr
    token = client_socket.recv(1024).decode("utf-8")
    # if token == "00":
    # print(f"LW1 received token: {token}")
    # #print ("S   N   R: ", epy_block_1.blk.getSNR())
    # float_snr = epy_block_1.blk.getSNR()
    # # data_to_send = "00: LW1\n" #transform into string
    # data_to_send = str(float_snr) #transform into string
    # print('SNR sent to UAV: ',data_to_send)

    snr_float = read_snr_measurement()  # read SNR from FIFO
    print("SNR sent to Controller: ", snr_float)

    dr_float = calculate_shannon_capacity(snr_float)
    snr_str = str(snr_float)  # transform into string
    previous_dr_str = str(previous_dr)
    data_to_send = "00" + "," + snr_str + "," + previous_dr_str
    previous_dr = dr_float
    client_socket.sendall(data_to_send.encode("utf-8"))
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


def start_base_station():

    node_to_ip = map_nodes_to_ips()
    for node, ip in node_to_ip.items():
        # print(node, ':', ip)
        # port = 80
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

    interface = "eth-XM-EVM"
    ip_address = get_ip_address(interface)
    # print('IP:', ip_address, 'type:',type(ip_address), 'LW: ', type(lw1_ip))

    if ip_address == lw1_ip:
        port = 8001
    elif ip_address == lw2_ip:
        port = 8002
    elif ip_address == lw3_ip:
        port = 8003
    elif ip_address == lw4_ip:
        port = 8004

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse the port immediately after it has been released:
    server_socket.bind(("", port))
    server_socket.listen(5)
    # server_socket.settimeout(1)  # Set the timeout to 1 second
    print(f"Listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        # print(f"LW1 connected to {addr}")
        handle_client(client_socket)
        # threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    start_base_station()
