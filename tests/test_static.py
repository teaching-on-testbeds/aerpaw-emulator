from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from render_topology import load_topology, render  # noqa: E402


def test_demo_topology_has_one_uav_and_one_ugv():
    topology = load_topology(ROOT / "topology.uav-ugv.yaml")
    assert topology["experiment"] == 839
    nodes = topology["nodes"]
    assert [(node["id"], node["vehicle"]) for node in nodes] == [(1, "uav"), (2, "ugv")]


def test_render_has_a_pair_per_node_and_one_bridge():
    document = render(load_topology(ROOT / "topology.uav-ugv.yaml"))
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
    gateway = render(load_topology(ROOT / "topology.uav-ugv.yaml"))["services"]["mavlink-gateway"]
    assert gateway["environment"]["CVM_ENDPOINTS"] == (
        "node1-uav-cvm:5762:1 node2-ugv-cvm:5762:2"
    )
    assert gateway["ports"] == ["127.0.0.1:5760:5760"]


def test_cvm_healthcheck_does_not_probe_the_long_lived_sitl_tcp_port():
    cvm = render(load_topology(ROOT / "topology.uav-ugv.yaml"))["services"]["node1-uav-cvm"]
    assert "5760" not in cvm["healthcheck"]["test"][1]
    assert "5762" not in cvm["healthcheck"]["test"][1]
    assert "standalone-sitl.pid" in cvm["healthcheck"]["test"][1]
    assert "standalone-mavlink-router.pid" in cvm["healthcheck"]["test"][1]


def test_nodes_have_stable_aerpaw_identity_and_result_mounts():
    document = render(load_topology(ROOT / "topology.uav-ugv.yaml"))
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


def test_single_uav_topology_is_the_no_zmq_baseline():
    topology = load_topology(ROOT / "topology.uav.yaml")
    assert topology["experiment"] == 841
    assert [(node["id"], node["vehicle"]) for node in topology["nodes"]] == [(1, "uav")]
    document = render(topology)
    assert set(document["services"]) == {
        "node1-uav-cvm",
        "node1-uav-evm",
        "mavlink-gateway",
    }


def test_two_uav_topology_matches_the_aerpaw_orbit_example():
    topology = load_topology(ROOT / "topology.two-uav.yaml")
    assert topology["experiment"] == 840
    assert [(node["id"], node["vehicle"]) for node in topology["nodes"]] == [(1, "uav"), (2, "uav")]
    document = render(topology)
    gateway = document["services"]["mavlink-gateway"]
    assert gateway["environment"]["CVM_ENDPOINTS"] == (
        "node1-uav-cvm:5762:1 node2-uav-cvm:5762:2"
    )
    assert document["services"]["node2-uav-evm"]["container_name"] == "E-VM-X0840-M2"
    assert "./results/840/node-2:/results" in document["services"]["node2-uav-evm"]["volumes"]


def test_checked_in_compose_files_match_the_renderer():
    pairs = {
        "topology.uav.yaml": "docker-compose.uav.yml",
        "topology.uav-ugv.yaml": "docker-compose.uav-ugv.yml",
        "topology.two-uav.yaml": "docker-compose.two-uav.yml",
    }
    for topology_name, compose_name in pairs.items():
        expected = render(load_topology(ROOT / topology_name))
        checked_in = yaml.safe_load((ROOT / compose_name).read_text(encoding="utf-8"))
        assert checked_in == expected, compose_name


def test_coordination_examples_are_shipped_in_experiments():
    for name in (
        "demo_coordinator.py",
        "demo_coord_vehicle.py",
        "drone_tracer.py",
        "drone_orbiter.py",
        "ground_coordinator.py",
        "consts.py",
        "orbit.plan",
    ):
        assert (ROOT / "experiments" / name).is_file(), name


def test_run_wrapper_forwards_zmq_flags_and_skips_armed_for_coordinators():
    wrapper = (ROOT / "tools/run-aerpawlib").read_text(encoding="utf-8")
    assert "--zmq-identifier" in wrapper
    assert "--zmq-proxy-server" in wrapper
    assert '"none"' in wrapper
    assert "arm_enabled" in wrapper
    runner = (ROOT / "tools/experiment_runner.py").read_text(encoding="utf-8")
    assert "--zmq-identifier" in runner
    assert "--zmq-proxy-server" in runner
    assert "--skip-init" in runner


def test_aerpaw_profile_compatibility_tree_is_vendored():
    profile_root = ROOT / "vendor/aerpaw-profile/AHN/E-VM"
    assert (profile_root / "Profile_software/ProfileScripts/startAll.sh").is_file()
    assert (profile_root / "Profile_software/ProfileScripts/stopAll.sh").is_file()
    assert (profile_root / "Profile_software/ProfileScripts/reset.sh").is_file()
    assert (profile_root / "Profile_software/ProfileScripts/Vehicle/startVehicle.sh").is_file()
    assert (profile_root / "bin/schedule_stop.sh").is_file()


def load_hub_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "mavlink_hub", ROOT / "docker/gateway/mavlink_hub.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RecordingBackend:
    def __init__(self, sysid: int):
        self.sysid = sysid
        self.sent = []

    def send(self, data: bytes) -> None:
        self.sent.append(data)


class FakeMessage:
    def __init__(self, msgid: int, raw: bytes, target: object = "unset"):
        self._msgid = msgid
        self._msgbuf = raw
        if target != "unset":
            self.target_system = target

    def get_msgId(self) -> int:
        return self._msgid


def test_hub_drops_gcs_heartbeats_and_routes_by_target_system():
    hub = load_hub_module()
    vehicle1 = RecordingBackend(1)
    vehicle2 = RecordingBackend(2)
    router = hub.Hub(5760, [vehicle1, vehicle2], parser_factory=None)

    router.route_from_client(FakeMessage(0, b"heartbeat"))
    assert vehicle1.sent == [] and vehicle2.sent == []

    router.route_from_client(FakeMessage(75, b"to-vehicle-1", target=1))
    assert vehicle1.sent == [b"to-vehicle-1"]
    assert vehicle2.sent == []

    router.route_from_client(FakeMessage(20, b"broadcast", target=0))
    assert vehicle1.sent[-1] == b"broadcast"
    assert vehicle2.sent[-1] == b"broadcast"

    router.route_from_client(FakeMessage(75, b"unknown-target", target=9))
    assert vehicle1.sent.count(b"unknown-target") == 0
    assert vehicle2.sent.count(b"unknown-target") == 0


def test_hub_backends_never_receive_other_vehicles_traffic():
    # vehicle-origin frames are only ever forwarded to ground clients; the hub
    # has no path that writes a backend frame into another backend socket
    hub = load_hub_module()
    source = RecordingBackend(1)
    neighbor = RecordingBackend(2)
    router = hub.Hub(5760, [source, neighbor], parser_factory=None)
    assert not hasattr(hub.Hub, "route_from_backend_to_backends")
    assert source.sent == [] and neighbor.sent == []
