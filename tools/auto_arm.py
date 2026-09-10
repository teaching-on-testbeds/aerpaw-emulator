#!/usr/bin/env python3
"""Arm or disarm one ArduPilot SITL vehicle over MAVLink."""

from __future__ import annotations

import argparse
import time

from pymavlink import mavutil


def set_mode(master, mode: str, deadline: float) -> None:
    mode_id = (master.mode_mapping() or {}).get(mode.upper())
    if mode_id is None:
        raise ValueError(f"flight mode {mode!r} is not available")

    while time.monotonic() < deadline:
        master.set_mode(mode_id)
        heartbeat = master.recv_match(type="HEARTBEAT", blocking=True, timeout=2)
        if heartbeat and heartbeat.custom_mode == mode_id:
            return
    raise TimeoutError(f"vehicle did not enter {mode} mode")


def set_armed(connection: str, timeout: float, armed: bool, mode: str | None = None) -> None:
    master = mavutil.mavlink_connection(connection)
    master.wait_heartbeat(timeout=timeout)
    deadline = time.monotonic() + timeout
    if mode:
        set_mode(master, mode, deadline)

    while time.monotonic() < deadline:
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1 if armed else 0,
            0,
            0,
            0,
            0,
            0,
            0,
        )
        try:
            ack = master.recv_match(type="COMMAND_ACK", blocking=True, timeout=2)
        except Exception:
            ack = None
        if ack and ack.command == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM:
            if ack.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
                state = "armed" if armed else "disarmed"
                print(f"vehicle {state}", flush=True)
                return
            if ack.result not in (
                mavutil.mavlink.MAV_RESULT_TEMPORARILY_REJECTED,
                mavutil.mavlink.MAV_RESULT_DENIED,
                mavutil.mavlink.MAV_RESULT_FAILED,
            ):
                raise RuntimeError(f"arm command failed with result {ack.result}")
        time.sleep(1)
    action = "arm" if armed else "disarm"
    raise TimeoutError(f"vehicle did not {action} within {timeout:g}s")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connect", required=True)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--action", choices=("arm", "disarm"), default="arm")
    parser.add_argument("--mode", help="flight mode to set before changing arm state")
    args = parser.parse_args()
    set_armed(args.connect, args.timeout, args.action == "arm", args.mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
