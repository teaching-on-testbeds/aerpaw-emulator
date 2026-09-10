"""Local platform adapter used by the standalone vehicle digital twin.

The public aerpawlib API remains available to experiment scripts. Platform
messages print to the container log and checkpoint values live for the life of
the Python process.
"""

from __future__ import annotations

import base64


OEO_MSG_SEV_INFO = "INFO"
OEO_MSG_SEV_WARN = "WARNING"
OEO_MSG_SEV_ERR = "ERROR"
OEO_MSG_SEV_CRIT = "CRITICAL"
_OEO_MSG_SEVS = [OEO_MSG_SEV_INFO, OEO_MSG_SEV_WARN, OEO_MSG_SEV_ERR, OEO_MSG_SEV_CRIT]


class AERPAW:
    """Provide aerpawlib's platform methods without a remote platform service."""

    def __init__(self, *_args, **_kwargs):
        self._connected = True
        self._no_stdout = False
        self._checkpoints: dict[tuple[str, str], object] = {}

    def attach_to_aerpaw_platform(self) -> bool:
        return True

    def _display_connection_warning(self):
        return

    def log_to_oeo(self, msg: str, severity: str = OEO_MSG_SEV_INFO, agent_id: str = None):
        """Print a platform log message to the container log."""
        if severity not in _OEO_MSG_SEVS:
            raise Exception("unsupported platform log severity")
        if not self._no_stdout:
            prefix = f"[{severity}]"
            if agent_id:
                prefix += f" [{agent_id}]"
            print(f"{prefix} {msg}", flush=True)

    def _checkpoint_build_request(self, var_type, var_name):
        return var_type, var_name

    def checkpoint_reset_server(self):
        self._checkpoints.clear()

    def checkpoint_set(self, checkpoint_name: str):
        self._checkpoints[("bool", checkpoint_name)] = True

    def checkpoint_check(self, checkpoint_name: str) -> bool:
        return bool(self._checkpoints.get(("bool", checkpoint_name), False))

    def checkpoint_increment_counter(self, counter_name: str):
        key = ("int", counter_name)
        self._checkpoints[key] = int(self._checkpoints.get(key, 0)) + 1

    def checkpoint_check_counter(self, counter_name: str) -> int:
        return int(self._checkpoints.get(("int", counter_name), 0))

    def checkpoint_set_string(self, string_name: str, value: str):
        self._checkpoints[("string", string_name)] = value

    def checkpoint_check_string(self, string_name: str) -> str:
        return str(self._checkpoints.get(("string", string_name), ""))

    def publish_user_oeo_topic(self, value: str, topic: str, agent_id: str = None) -> bool:
        """Log a topic value locally and report success."""
        encoded_topic = base64.urlsafe_b64encode(str(topic).encode("utf-8")).decode("ascii")
        encoded_value = base64.urlsafe_b64encode(str(value).encode("utf-8")).decode("ascii")
        self.log_to_oeo(f"topic={encoded_topic} value={encoded_value}", agent_id=agent_id)
        return True


AERPAW_Platform = AERPAW()
