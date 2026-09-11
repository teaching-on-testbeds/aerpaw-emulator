#!/usr/bin/env python3
"""Launch an aerpawlib runner with the standalone container settings."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script", default=os.environ.get("EXPERIMENT_SCRIPT", "demo_square"))
    parser.add_argument("--vehicle", default=os.environ.get("VEHICLE_TYPE", "drone"))
    parser.add_argument("--connection", default=os.environ.get("MAVLINK_CONNECTION"))
    parser.add_argument("--zmq-identifier", default=os.environ.get("ZMQ_IDENTIFIER"))
    parser.add_argument("--zmq-proxy-server", default=os.environ.get("ZMQ_PROXY_SERVER"))
    parser.add_argument("extra", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.connection and args.vehicle != "none":
        parser.error("--connection or MAVLINK_CONNECTION is required")

    command = [
        sys.executable,
        "-m",
        "aerpawlib",
        "--script",
        args.script,
        "--conn",
        args.connection or "none",
        "--vehicle",
        args.vehicle,
    ]
    if args.vehicle == "none":
        command.append("--skip-init")
    if args.zmq_identifier:
        command += ["--zmq-identifier", args.zmq_identifier]
    if args.zmq_proxy_server:
        command += ["--zmq-proxy-server", args.zmq_proxy_server]
    extra = list(args.extra)
    if extra[:1] == ["--"]:
        extra = extra[1:]
    command.extend(extra)
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
