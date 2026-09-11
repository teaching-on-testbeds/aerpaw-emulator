#!/usr/bin/env python3
"""Render a topology definition into an explicit Docker Compose file."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by the CLI
    raise SystemExit("render_topology.py needs PyYAML; install requirements.txt") from exc


VEHICLE_TYPES = {
    "uav": {
        "evm_vehicle": "drone",
        "sitl_model": "copter",
        "sitl_binary": "arducopter",
        "params": "uav.parm",
    },
    "ugv": {
        "evm_vehicle": "rover",
        "sitl_model": "rover",
        "sitl_binary": "ardurover",
        "params": "ugv.parm",
    },
}


def _service_name(node_id: int, vehicle: str, role: str) -> str:
    return f"node{node_id}-{vehicle}-{role}"


def _number(value, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    return value


def load_topology(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        document = yaml.safe_load(stream)

    if not isinstance(document, dict) or document.get("version") != 1:
        raise ValueError("topology version must be 1")
    experiment = document.get("experiment")
    if isinstance(experiment, bool) or not isinstance(experiment, int) or not 1 <= experiment <= 9999:
        raise ValueError("experiment must be an integer from 1 to 9999")

    nodes = document.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("topology must contain a non-empty nodes list")

    result = []
    seen = set()
    for raw in nodes:
        if not isinstance(raw, dict):
            raise ValueError("each node must be a mapping")
        node_id = raw.get("id")
        if isinstance(node_id, bool) or not isinstance(node_id, int) or not 1 <= node_id <= 255:
            raise ValueError("node ids must be integers from 1 to 255")
        if node_id in seen:
            raise ValueError(f"duplicate node id: {node_id}")
        seen.add(node_id)

        vehicle = raw.get("vehicle")
        if vehicle not in VEHICLE_TYPES:
            raise ValueError("vehicle must be one of: uav, ugv")
        home = raw.get("home")
        if not isinstance(home, dict):
            raise ValueError(f"node {node_id} needs a home mapping")
        for key in ("lat", "lon", "heading"):
            _number(home.get(key), f"node {node_id} home.{key}")
        result.append({"id": node_id, "vehicle": vehicle, "home": home})

    return {"experiment": experiment, "nodes": result}


def render(topology: dict) -> dict:
    experiment = topology["experiment"]
    nodes = topology["nodes"]
    experiment_id = f"{experiment:04d}"
    node_set = " ".join("0" for _ in nodes)
    services = {}
    for node in nodes:
        node_id = node["id"]
        vehicle = node["vehicle"]
        kind = VEHICLE_TYPES[vehicle]
        cvm = _service_name(node_id, vehicle, "cvm")
        evm = _service_name(node_id, vehicle, "evm")
        home = node["home"]
        cvm_container = f"C-VM-X{experiment_id}-M{node_id}"
        evm_container = f"E-VM-X{experiment_id}-M{node_id}"
        common_environment = {
            "AP_EXPENV_EXP_NUM": str(experiment),
            "AP_EXPENV_NUM_NODES": str(len(nodes)),
            "AP_EXPENV_SESSION_ENV": "Virtual",
            "AP_EXPENV_SET_NODES": node_set,
            "AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM": str(node_id),
            "AP_EXPENV_THIS_CONTAINER_NODE_TYPE": "Portable",
            "AP_EXPENV_THIS_CONTAINER_NODE_VEHICLE": f"vehicle_{vehicle}",
        }

        services[cvm] = {
            "build": {"context": ".", "dockerfile": "docker/cvm/Dockerfile"},
            "image": "aerpaw-standalone-cvm:latest",
            "container_name": cvm_container,
            "hostname": cvm_container.lower(),
            "environment": {
                **common_environment,
                "AP_EXPENV_THIS_CONTAINER_NAME": cvm_container,
                "AP_EXPENV_THIS_CONTAINER_ROLE": "C-VM",
                "EVM_SERVICE": evm,
                "NODE_ID": str(node_id),
                "SITL_HOME": f"{home['lat']},{home['lon']},0,{home['heading']}",
                "SITL_SYSID": str(node_id),
                "VEHICLE_TYPE": vehicle,
            },
            "healthcheck": {
                "test": [
                    "CMD-SHELL",
                    "test -r /run/standalone-sitl.pid && kill -0 \"$(cat /run/standalone-sitl.pid)\" && test -r /run/standalone-mavlink-router.pid && kill -0 \"$(cat /run/standalone-mavlink-router.pid)\"",
                ],
                "interval": "2s",
                "timeout": "2s",
                "retries": 60,
                "start_period": "5s",
            },
            "init": True,
            "networks": ["vehicle-net"],
            "stop_grace_period": "10s",
        }
        services[evm] = {
            "build": {"context": ".", "dockerfile": "docker/evm/Dockerfile"},
            "image": "aerpaw-standalone-evm:latest",
            "container_name": evm_container,
            "hostname": evm_container.lower(),
            "depends_on": {cvm: {"condition": "service_started"}},
            "environment": {
                **common_environment,
                "AP_EXPENV_OEOCVM_XM": "127.0.0.1",
                "AP_EXPENV_THIS_CONTAINER_NAME": evm_container,
                "AP_EXPENV_THIS_CONTAINER_ROLE": "E-VM",
                "CVM_SERVICE": cvm,
                "AUTO_ARM": "1",
                "AUTO_ARM_CONNECTION": "udp:0.0.0.0:14551",
                "MAVLINK_CONNECTION": "udp:0.0.0.0:14550",
                "NODE_ID": str(node_id),
                "SQUARE_SIZE": "10",
                "VEHICLE_TYPE": kind["evm_vehicle"],
            },
            "init": True,
            "networks": ["vehicle-net"],
            "volumes": [
                "./experiments:/opt/standalone/experiments:ro",
                f"./results/{experiment}/node-{node_id}:/results",
            ],
        }

    cvm_endpoints = " ".join(
        f"{_service_name(node['id'], node['vehicle'], 'cvm')}:5762:{node['id']}"
        for node in nodes
    )
    services["mavlink-gateway"] = {
        "build": {"context": ".", "dockerfile": "docker/cvm/Dockerfile"},
        "image": "aerpaw-standalone-cvm:latest",
        "container_name": f"MAVLink-Gateway-X{experiment_id}",
        "hostname": f"mavlink-gateway-x{experiment_id}",
        "depends_on": {
            _service_name(node["id"], node["vehicle"], "cvm"): {"condition": "service_started"}
            for node in nodes
        },
        "environment": {"CVM_ENDPOINTS": cvm_endpoints},
        "entrypoint": ["/opt/standalone/docker/gateway/entrypoint.sh"],
        "healthcheck": {
            "test": ["CMD-SHELL", "nc -z 127.0.0.1 5760"],
            "interval": "2s",
            "timeout": "2s",
            "retries": 60,
            "start_period": "5s",
        },
        "init": True,
        "networks": ["vehicle-net"],
        "ports": ["127.0.0.1:5760:5760"],
    }

    return {
        "name": f"aerpaw-standalone-x{experiment_id}",
        "services": services,
        "networks": {"vehicle-net": {"driver": "bridge"}},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topology", type=Path)
    parser.add_argument("--output", type=Path, default=Path("docker-compose.yml"))
    args = parser.parse_args()

    try:
        document = render(load_topology(args.topology))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"topology render failed: {exc}", file=sys.stderr)
        return 2

    with args.output.open("w", encoding="utf-8") as stream:
        yaml.safe_dump(document, stream, sort_keys=False, default_flow_style=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
