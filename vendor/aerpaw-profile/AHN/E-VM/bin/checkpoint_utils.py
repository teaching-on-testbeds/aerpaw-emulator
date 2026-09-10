import os
import time

import requests

DEFAULT_QUERY_DELAY = 1
DEFAULT_PORT = 12435
DEFAULT_HOST = os.getenv("AP_EXPENV_OEOCVM_XM", "192.168.32.25")  # connect to OEO-CONSOLE, or default to C-VM (will only work on portable nodes)


def _build_request(var_type: str, var_name: str, port: int, host: str) -> str:
    if var_type not in ["string", "bool", "int"]:
        return None
    return f"http://{host}:{port}/checkpoint/{var_type}/{var_name}"


def reset_checkpoint_server(port: int = DEFAULT_PORT, host: str = DEFAULT_HOST):
    response = requests.post(f"http://{host}:{port}/checkpoint/reset")
    if response.status_code != 200:
        raise Exception("error when resetting checkpoint server")


def set_checkpoint(checkpoint_name: str, port: int = DEFAULT_PORT, host: str = DEFAULT_HOST):
    response = requests.post(_build_request("bool", checkpoint_name, port, host))
    if response.status_code != 200:
        raise Exception("error when posting to checkpoint server")


def check_checkpoint(checkpoint_name: str, port: int = DEFAULT_PORT, host: str = DEFAULT_HOST) -> bool:
    response = requests.get(_build_request("bool", checkpoint_name, port, host))
    if response.status_code != 200:
        raise Exception("error when getting from checkpoint server")
    response_content = response.content.decode()
    if response_content == "True":
        return True
    elif response_content == "False":
        return False
    raise Exception(f"malformed content in response from server: {response_content}")


def wait_for_checkpoint(checkpoint_name: str, query_delay: int = DEFAULT_QUERY_DELAY, port: int = DEFAULT_PORT, host: str = DEFAULT_HOST):
    # blocks until checkpoint is set
    while not check_checkpoint(checkpoint_name, port, host):
        time.sleep(query_delay)


def increment_counter(counter_name: str, port: int = DEFAULT_PORT, host: str = DEFAULT_HOST):
    response = requests.post(_build_request("int", counter_name, port, host))
    if response.status_code != 200:
        raise Exception("error when posting to checkpoint server")


def check_counter(counter_name: str, port: int = DEFAULT_PORT, host: str = DEFAULT_HOST) -> int:
    response = requests.get(_build_request("int", counter_name, port, host))
    if response.status_code != 200:
        raise Exception("error when getting from checkpoint server")
    response_content = response.content.decode()
    try:
        return int(response_content)
    except TypeError:
        raise Exception(f"malformed content in response from server: {response_content}")


def set_string(string_name: str, value: str, port: int = DEFAULT_PORT, host: str = DEFAULT_HOST):
    response = requests.post(_build_request("string", string_name, port, host) + f"?val={value}")
    if response.status_code != 200:
        raise Exception("error when posting to checkpoint server")


def check_string(string_name: str, port: int = DEFAULT_PORT, host: str = DEFAULT_HOST) -> str:
    response = requests.get(_build_request("string", string_name, port, host))
    if response.status_code != 200:
        raise Exception("error when getting from checkpoint server")
    response_content = response.content.decode()
    return response_content
