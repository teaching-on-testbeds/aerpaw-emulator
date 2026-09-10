import re


def map_nodes_to_ips():
    """
    This function reads a configuration file, extracts node names and their corresponding IP addresses
    from the script, and returns the node-to-IP mapping in the order defined by the nodes in
    AP_EXPENV_SET_NODES.

    :param file_path: Path to the configuration file containing the node and IP information.
    :return: A dictionary with node names as keys and IPs as values in the target order.
    """
    node_to_ip_temp = {}

    try:
        # Open and read the file
        file_path = "/root/.ap-set-experiment-env.sh"
        with open(file_path) as file:
            lines = file.readlines()

        # Extract the target order from AP_EXPENV_SET_NODES
        nodes_line = next(line for line in lines if "AP_EXPENV_SET_NODES=" in line)
        target_order = re.findall(r"[a-zA-Z0-9]+", nodes_line.split("=")[1])

        # Extract XM IP mappings and temporarily store by node number
        for line in lines:
            if "AP_EXPENV_EVM" in line and "_XM=" in line:
                match = re.match(r"export AP_EXPENV_EVM_(\d+)_XM=(.*)", line.strip())
                if match:
                    node_num, ip = match.groups()
                    node_to_ip_temp[node_num] = ip

        # Map nodes in the target order
        node_to_ip_final = {}
        for idx, node_name in enumerate(target_order):
            # Node index in `AP_EXPENV_SET_NODES` corresponds to the node number in the script
            node_num = str(idx + 1)  # Node numbers start at 1
            ip = node_to_ip_temp.get(node_num, "No XM IP found")
            node_to_ip_final[node_name] = ip

        return node_to_ip_final

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


# # Example usage
# if __name__ == "__main__":
# # Provide the path to your shell script here
# node_to_ip = map_nodes_to_ips(file_path)
# print(node_to_ip)

# # Display the results in the required format
# print("Node-to-IP Mapping (XM) in Target Order:")
# for node, ip in node_to_ip.items():
# print(f"{node}: {ip}")
