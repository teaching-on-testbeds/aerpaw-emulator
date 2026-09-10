"""
Functionality exclusive to the AERPAW platform

The AERPAW_Platform singleton will automatically detect if a script is being
run in an AERPAW experiment, in which case it enables additional AERPAW
functionality.
"""

import base64
import os

import requests

# connect to OEO-CONSOLE, or default to C-VM (will only work on portable nodes)
_DEFAULT_FORWARD_SERVER_IP = os.getenv("AP_EXPENV_OEOCVM_XM", "192.168.32.25")
_DEFAULT_FORWARD_SERVER_PORT = 12435

_DEFAULT_HUMAN_READABLE_AGENT_ID = os.getenv("AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM")

OEO_MSG_SEV_INFO = "INFO"
OEO_MSG_SEV_WARN = "WARNING"
OEO_MSG_SEV_ERR = "ERROR"
OEO_MSG_SEV_CRIT = "CRITICAL"
_OEO_MSG_SEVS = [OEO_MSG_SEV_INFO, OEO_MSG_SEV_WARN, OEO_MSG_SEV_ERR, OEO_MSG_SEV_CRIT]


class AERPAW:
    _forw_addr: str
    _connected: bool

    _connection_warning_displayed = False

    def __init__(self, forw_addr=_DEFAULT_FORWARD_SERVER_IP, forw_port=_DEFAULT_FORWARD_SERVER_PORT):
        self._forw_addr = forw_addr
        self._forw_port = forw_port
        self._connected = self.attach_to_aerpaw_platform()
        self._no_stdout = False

    def attach_to_aerpaw_platform(self) -> bool:
        """
        Attempts to attach this `AERPAW` object to the AERPAW platform/C-VM
        hosting this experiment. Returns bool depending on success.
        """
        try:
            requests.post(f"http://{self._forw_addr}:{self._forw_port}/ping", timeout=1)
        except requests.exceptions.RequestException:
            return False
        return True

    def _display_connection_warning(self):
        if self._connection_warning_displayed:
            return
        if not self._no_stdout:
            print("[aerpawlib] INFO: the user script has attempted to use AERPAW platform functionality without being in the AERPAW environment")
        self._connection_warning_displayed = True

    def log_to_oeo(self, msg: str, severity: str = OEO_MSG_SEV_INFO, agent_id: str = _DEFAULT_HUMAN_READABLE_AGENT_ID):
        """
        Send `msg` to the OEO console, if connected. Prints message regardless
        of connection status.

        Use `agent_id` to provide an identifier for the message being sent. By
        default, it uses the current node's number.
        """
        if not self._no_stdout:
            print(msg)
        if not self._connected:
            self._display_connection_warning()
            return

        if severity not in _OEO_MSG_SEVS:
            raise Exception("severity provided for log_to_oeo not supported")
        encoded = base64.urlsafe_b64encode(msg.encode("utf-8"))
        try:
            if agent_id:
                requests.post(f"http://{self._forw_addr}:{self._forw_port}/oeo_msg/{severity}/{encoded.decode('utf-8')}/{agent_id}", timeout=3)
            else:
                requests.post(f"http://{self._forw_addr}:{self._forw_port}/oeo_msg/{severity}/{encoded.decode('utf-8')}", timeout=3)
        except requests.exceptions.RequestException:
            if not self._no_stdout:
                print("unable to send previous message to OEO.")

    def _checkpoint_build_request(self, var_type, var_name):
        return f"http://{self._forw_addr}:{self._forw_port}/checkpoint/{var_type}/{var_name}"

    # NOTE: unlike the above functionality, all checkpoint functions will cause an
    # exception if they are run while not in the AERPAW platform, as there isn't a way
    # to "recover" while maintaining the function's API contract

    def checkpoint_reset_server(self):
        """
        Reset the AERPAW checkpoint server.

        This function should be called at the start of an experiment by an E-VM script
        to ensure that no stored state remains between experiment runs.
        """
        if not self._connected:
            self._display_connection_warning()
            raise Exception("AERPAW checkpoint functionality only works in AERPAW environment")
        response = requests.post(f"http://{self._forw_addr}:{self._forw_port}/checkpoint/reset")
        if response.status_code != 200:
            raise Exception("error when resetting checkpoint server")

    def checkpoint_set(self, checkpoint_name: str):
        """
        Set a checkpoint in the AERPAW checkpoint system with name `checkpoint_name`
        """
        if not self._connected:
            self._display_connection_warning()
            raise Exception("AERPAW checkpoint functionality only works in AERPAW environment")
        response = requests.post(self._checkpoint_build_request("bool", checkpoint_name))
        if response.status_code != 200:
            raise Exception("error when posting to checkpoint server")

    def checkpoint_check(self, checkpoint_name: str) -> bool:
        """
        See if a checkpoint has been set in the AERPAW checkpoint system with name
        `checkpoint_name`.

        Returns `True` if it has been set, `False` otherwise
        """
        if not self._connected:
            self._display_connection_warning()
            raise Exception("AERPAW checkpoint functionality only works in AERPAW environment")
        response = requests.get(self._checkpoint_build_request("bool", checkpoint_name))
        if response.status_code != 200:
            raise Exception("error when getting from checkpoint server")
        response_content = response.content.decode()
        if response_content == "True":
            return True
        elif response_content == "False":
            return False
        raise Exception(f"malformed content in response from server: {response_content}")

    def checkpoint_increment_counter(self, counter_name: str):
        """
        Increment a counter in the AERPAW checkpoint system with name `counter_name`.
        """
        if not self._connected:
            self._display_connection_warning()
            raise Exception("AERPAW checkpoint functionality only works in AERPAW environment")
        response = requests.post(self._checkpoint_build_request("int", counter_name))
        if response.status_code != 200:
            raise Exception("error when posting to checkpoint server")

    def checkpoint_check_counter(self, counter_name: str) -> int:
        """
        Get the current state of a counter in the AERPAW checkpoint system with name
        `counter_name`

        An un-incremented counter will always start at 0, regardless of if it has been
        interacted with.
        """
        if not self._connected:
            self._display_connection_warning()
            raise Exception("AERPAW checkpoint functionality only works in AERPAW environment")
        response = requests.get(self._checkpoint_build_request("int", counter_name))
        if response.status_code != 200:
            raise Exception("error when getting from checkpoint server")
        response_content = response.content.decode()
        try:
            return int(response_content)
        except TypeError:
            raise Exception(f"malformed content in response from server: {response_content}")

    def checkpoint_set_string(self, string_name: str, value: str):
        """
        Set the value of a string in the AERPAW checkpoint system's key:value store with
        name `string_name` and value `value`
        """
        if not self._connected:
            self._display_connection_warning()
            raise Exception("AERPAW checkpoint functionality only works in AERPAW environment")
        response = requests.post(self._checkpoint_build_request("string", string_name) + f"?val={value}")
        if response.status_code != 200:
            raise Exception("error when posting to checkpoint server")

    def checkpoint_check_string(self, string_name: str) -> str:
        """
        Get the value of a key:value pair in AERPAW's key:value store with key
        `string_name`
        """
        if not self._connected:
            self._display_connection_warning()
            raise Exception("AERPAW checkpoint functionality only works in AERPAW environment")
        response = requests.get(self._checkpoint_build_request("string", string_name))
        if response.status_code != 200:
            raise Exception("error when getting from checkpoint server")
        response_content = response.content.decode()
        return response_content

    def publish_user_oeo_topic(self, value: str, topic: str, agent_id: str = _DEFAULT_HUMAN_READABLE_AGENT_ID) -> bool:
        """
        Publish `value` to a user topic in the OEO system (can be added/is
        visible on the OEO-console).

        Use `agent_id` to provide an identifier for the message being sent. By
        default, it uses the current node's number.

        `topic` is used to structure the topic as received in the OEO system.
        The message will be received internally "oeo/user/`topic`" and can be
        viewed in the OEO-CONSOLE by adding `topic`. `topic` can include "/"s
        to indicate a hierachy within the message (e.g. "radio_script/snr" and
        "radio_script/throughput" could both be seen on the console by "add"ing
        "radio_script").

        returns bool based on success
        """

        # note for devs, the messages can be sent to http://oeo_console:port/oeo_pub/encoded_topic/encoded_value/(optional)encoded_agent

        if not self._connected:
            self._display_connection_warning()
            return False

        value_b64 = base64.urlsafe_b64encode(str(value).encode("utf-8")).decode("utf-8")
        topic_b64 = base64.urlsafe_b64encode(str(topic).encode("utf-8")).decode("utf-8")
        agent_b64 = None

        if agent_id is not None:
            agent_b64 = base64.urlsafe_b64encode(str(agent_id).encode("utf-8")).decode("utf-8")

        try:
            if not agent_id:
                requests.post(f"http://{self._forw_addr}:{self._forw_port}/oeo_pub/{topic_b64}/{value_b64}", timeout=3)
            else:
                requests.post(f"http://{self._forw_addr}:{self._forw_port}/oeo_pub/{topic_b64}/{value_b64}/{agent_b64}", timeout=3)
        except requests.exceptions.RequestException as e:
            print("unable to publish value to OEO system. exception:")
            print(e.strerror)
            return False
        return True


AERPAW_Platform = AERPAW()
