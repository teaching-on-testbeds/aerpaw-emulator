from pathlib import Path
import socket
import subprocess
import sys
import time

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from render_topology import load_topology, render  # noqa: E402


def test_demo_topology_has_one_uav_and_one_ugv():
    topology = load_topology(ROOT / "topology.yaml")
    assert topology["experiment"] == 839
    nodes = topology["nodes"]
    assert [(node["id"], node["vehicle"]) for node in nodes] == [(1, "uav"), (2, "ugv")]


def test_render_has_a_pair_per_node_and_one_bridge():
    document = render(load_topology(ROOT / "topology.yaml"))
    assert set(document["services"]) == {
        "node1-uav-cvm",
        "node1-uav-evm",
        "node2-ugv-cvm",
        "node2-ugv-evm",
        "mavlink-gateway",
    }
    assert document["networks"] == {"vehicle-net": {"driver": "bridge"}}
    for name, service in document["services"].items():
        assert service["networks"] == ["vehicle-net"]
        if name.endswith("-evm"):
            assert service["depends_on"]


def test_mavlink_gateway_aggregates_cvm_routers_on_one_host_port():
    gateway = render(load_topology(ROOT / "topology.yaml"))["services"]["mavlink-gateway"]
    assert gateway["environment"]["CVM_ENDPOINTS"] == (
        "node1-uav-cvm:5762 node2-ugv-cvm:5762"
    )
    assert gateway["ports"] == ["127.0.0.1:5760:5760"]


def test_cvm_healthcheck_does_not_probe_the_long_lived_sitl_tcp_port():
    cvm = render(load_topology(ROOT / "topology.yaml"))["services"]["node1-uav-cvm"]
    assert "5760" not in cvm["healthcheck"]["test"][1]
    assert "5762" not in cvm["healthcheck"]["test"][1]
    assert "standalone-sitl.pid" in cvm["healthcheck"]["test"][1]
    assert "standalone-mavlink-router.pid" in cvm["healthcheck"]["test"][1]


def test_nodes_have_stable_aerpaw_identity_and_result_mounts():
    document = render(load_topology(ROOT / "topology.yaml"))
    evm = document["services"]["node1-uav-evm"]
    cvm = document["services"]["node1-uav-cvm"]
    assert evm["container_name"] == "E-VM-X0839-M1"
    assert cvm["container_name"] == "C-VM-X0839-M1"
    assert evm["environment"]["AP_EXPENV_THIS_CONTAINER_NODE_VEHICLE"] == "vehicle_uav"
    assert "./results/839/node-1:/results" in evm["volumes"]


def test_ugv_defaults_match_regular_aerpaw_sitl_setup_requirements():
    params = (ROOT / "docker/cvm/params/ugv.parm").read_text(encoding="utf-8")
    for setting in (
        "INS_ACCOFFS_X 0.001",
        "INS_ACCSCAL_X 1.001",
        "INS_ACC2OFFS_X 0.001",
        "INS_ACC2SCAL_X 1.001",
        "RC1_MIN 1000",
        "RC1_MAX 2000",
        "RC3_MIN 1000",
        "RC3_MAX 2000",
    ):
        assert setting in params


def test_checked_in_compose_matches_renderer():
    expected = render(load_topology(ROOT / "topology.yaml"))
    checked_in = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
    assert checked_in == expected


def test_aerpaw_profile_compatibility_tree_is_vendored():
    profile_root = ROOT / "vendor/aerpaw-profile/AHN/E-VM"
    assert (profile_root / "Profile_software/ProfileScripts/startAll.sh").is_file()
    assert (profile_root / "Profile_software/ProfileScripts/stopAll.sh").is_file()
    assert (profile_root / "Profile_software/ProfileScripts/reset.sh").is_file()
    assert (profile_root / "Profile_software/ProfileScripts/Vehicle/startVehicle.sh").is_file()
    assert (profile_root / "bin/schedule_stop.sh").is_file()


def test_tcp_udp_bridge_keeps_multiple_tcp_clients_connected():
    bridge = ROOT / "docker/gateway/tcp_udp_bridge.py"
    upstream = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    upstream.bind(("127.0.0.1", 0))
    tcp_probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_probe.bind(("127.0.0.1", 0))
    tcp_port = tcp_probe.getsockname()[1]
    tcp_probe.close()
    process = subprocess.Popen(
        [sys.executable, str(bridge), "--tcp-port", str(tcp_port), "--udp-port", str(upstream.getsockname()[1])],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    clients = []
    try:
        deadline = time.monotonic() + 3
        while True:
            try:
                clients.append(socket.create_connection(("127.0.0.1", tcp_port), timeout=1))
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise
        clients.append(socket.create_connection(("127.0.0.1", tcp_port), timeout=1))
        clients[0].sendall(b"qgc")
        upstream.settimeout(2)
        packet, address = upstream.recvfrom(1024)
        assert packet == b"qgc"
        upstream.sendto(b"mavlink", address)
        for client in clients:
            client.settimeout(2)
            assert client.recv(1024) == b"mavlink"
    finally:
        for client in clients:
            client.close()
        upstream.close()
        process.terminate()
        process.wait(timeout=3)
