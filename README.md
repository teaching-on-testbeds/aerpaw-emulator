# Standalone AERPAW Vehicle Digital Twin

This project runs AERPAW-style virtual vehicles with Docker Compose. Each node has a C-VM container running ArduPilot SITL and MAVLink Router, plus an E-VM container for `aerpawlib` experiments. The Docker bridge acts as an always-connected channel.

Three topologies ship with the project. Every one of them has a matching Compose file:

| Topology file | Experiment | Nodes | Demos |
|---|---|---|---|
| `topology.uav.yaml` | 841 | one UAV | `demo_square` (no ZMQ) |
| `topology.uav-ugv.yaml` | 839 | UAV + UGV | `demo_square` per vehicle; coordinated-square ZMQ demo |
| `topology.two-uav.yaml` | 840 | two UAVs | AERPAW tracer/orbiter/ground example, vendored unchanged |

Only run one stack at a time: every gateway publishes `127.0.0.1:5760`.

## Start

The first build downloads public source for ArduPilot, MAVLink Router, and DroneKit. It does not need a token.

```bash
docker compose -f docker-compose.uav.yml up --build -d
docker compose -f docker-compose.uav.yml ps
```

Wait until the C-VM services report `healthy`. The `-f` flag appears in every Compose command below; all commands assume the single-UAV stack unless shown otherwise.

The central gateway (`docker/gateway/mavlink_hub.py`) aggregates all vehicle system IDs onto one TCP port, published on the host as `127.0.0.1:5760`. It keeps AERPAW's link isolation between vehicles: each vehicle's stream is shared only with ground clients, never into another vehicle's link. To connect QGroundControl from your workstation through SSH, run:

```bash
ssh -N \
  -L 5760:127.0.0.1:5760 \
  user@remote-host
```

## QGroundControl

Add one TCP link to `localhost:5760` in QGroundControl.

The gateway exposes every vehicle of the running stack on that one TCP link, so QGroundControl shows them as separate entries in the vehicle list (the vehicle icon/drop-down in the toolbar). A vehicle's MAVLink system ID equals its node ID in the topology file:

| Topology | System IDs |
|---|---|
| `uav` | 1 (ArduCopter) |
| `uav-ugv` | 1 (ArduCopter), 2 (ArduRover) |
| `two-uav` | 1, 2 (both ArduCopter) |

Select an entry to switch telemetry. Only the active vehicle is drawn on the map and HUD, and QGC remembers which vehicle is active between connects.

### UAV vs UGV capabilities

- **UAV (ArduCopter quad):** flight-capable. Supports Guided, Auto, Loiter,
  RTL, takeoff, and landing, and reports altitude. It starts disarmed on the
  ground at its home; the experiment wrapper arms it and takes off before a run.
- **UGV (ArduRover):** ground vehicle. Supports Auto, Manual/Steering, and
  Hold, but has no Guided mode and no altitude/attitude control. The HUD and
  instrument panel reflect that: no flight instruments, ground speed only.

Notes:
- If QGC shows a "Frame Class: Rover" setup warning or reports "Guided mode not
  supported by Vehicle", the active vehicle is the UGV. Switch to the UAV entry
  for flight tests.
- Setup warnings for the UGV are expected to disappear now that its parameter
  defaults match the regular AERPAW rover SITL configuration (accelerometer
  calibration, RC ranges, battery monitor).
- Vehicle names in QGC are the SITL autopilot defaults; change them in the
  vehicle settings if you want per-node labels.

## Run Experiments

Run the no-ZMQ demo on the UAV:

```bash
docker compose -f docker-compose.uav.yml exec node1-uav-evm run-aerpawlib demo_square
```

Run it on both vehicles of the `uav-ugv` stack:

```bash
docker compose -f docker-compose.uav-ugv.yml exec -d node1-uav-evm sh -c \
  'run-aerpawlib demo_square > /results/demo.log 2>&1'
docker compose -f docker-compose.uav-ugv.yml exec -d node2-ugv-evm sh -c \
  'run-aerpawlib demo_square > /results/demo.log 2>&1'
```

Results are available on the host under `results/<experiment>/node-<id>`, e.g. `results/841/node-1`.

Place additional Python experiment modules in `experiments/`. Run a module named `experiments/my_experiment.py` with:

```bash
docker compose -f docker-compose.uav.yml exec node1-uav-evm run-aerpawlib my_experiment
```

Arguments after the module name pass through to the experiment:

```bash
docker compose -f docker-compose.uav.yml exec node1-uav-evm \
  run-aerpawlib my_experiment --output /results/run.csv
```

Open a container shell with:

```bash
docker compose -f docker-compose.uav.yml exec node1-uav-evm bash
docker compose -f docker-compose.uav.yml exec node1-uav-cvm bash
```

The experiment wrapper arms the simulated vehicle before a run and disarms it afterward. Set `AUTO_ARM: "0"` for a node in the compose file if an experiment handles arming itself.

The E-VM image also provides the AERPAW profile filesystem. `/root/Profiles` points to the vendored `Profile_software` tree, and `/root/startexperiment.sh`, `/root/stopexperiment.sh`, and `/root/reset.sh` point to the matching profile scripts. The image sets `AERPAW_REPO`, `PROFILE_DIR`, and the AERPAW E-VM `bin` directory in the environment and adds that bin directory to `/root/.bashrc`.

The profile scripts are present for path compatibility. Radio, CHEM, and other hardware-dependent programs remain unavailable in this vehicle-only deployment.

## Multi-vehicle coordination (ZMQ)

`aerpawlib`'s `ZmqStateMachine` runner lets several experiment processes coordinate: they exchange state transitions and field queries through a ZeroMQ proxy. This mirrors how AERPAW's *VCS3: Multiple Vehicle Coordination* works on the real testbed: the broker is a process the experimenter starts on any E-VM, and vehicles plus coordinators are separate processes that point at it.

Start the broker on one of the E-VMs (`screen` keeps it alive after the exec session exits):

```bash
docker compose -f docker-compose.uav-ugv.yml exec node1-uav-evm \
  screen -dmS zmq python3 -m aerpawlib --run-proxy
```

Agents reach the broker by container service name (`ZMQ_PROXY_SERVER=node1-uav-evm`). Start the coordinator before the vehicles: plain ZeroMQ pub/sub does not replay messages, and AERPAW's own examples announce readiness once.

### Coordinated-square demo (uav-ugv)

Three processes: one vehicle script serving both the UAV and the UGV, plus a coordinator that runs with `VEHICLE_TYPE=none` (the wrapper then skips arming). This pair keeps announcing readiness until the coordinator answers, so start order does not matter for it:

```bash
topo=docker-compose.uav-ugv.yml
docker compose -f $topo exec -d \
  -e ZMQ_IDENTIFIER=uav -e ZMQ_PROXY_SERVER=node1-uav-evm node1-uav-evm sh -c \
  'run-aerpawlib demo_coord_vehicle > /results/vehicle.log 2>&1'
docker compose -f $topo exec -d \
  -e ZMQ_IDENTIFIER=ugv -e ZMQ_PROXY_SERVER=node1-uav-evm node2-ugv-evm sh -c \
  'run-aerpawlib demo_coord_vehicle > /results/vehicle.log 2>&1'
docker compose -f $topo exec -d \
  -e VEHICLE_TYPE=none -e ZMQ_IDENTIFIER=coordinator \
  -e ZMQ_PROXY_SERVER=node1-uav-evm node1-uav-evm sh -c \
  'run-aerpawlib demo_coordinator > /results/coordinator.log 2>&1'
```

The coordinator dispatches each vehicle through a 10 m square (the UAV takes off and lands, the UGV drives), and prints `coordinated squares complete` when both report done.

### Tracer/orbiter demo (two-uav, AERPAW example verbatim)

`experiments/drone_tracer.py`, `drone_orbiter.py`, `ground_coordinator.py`, `consts.py`, and `orbit.plan` are AERPAW's `zmq_preplanned_orbit` example copied without changes; identifiers come from `consts.py`. The example needs two drones, so it runs on the `two-uav` stack:

```bash
topo=docker-compose.two-uav.yml
docker compose -f $topo exec node1-uav-evm \
  screen -dmS zmq python3 -m aerpawlib --run-proxy
docker compose -f $topo exec -d \
  -e VEHICLE_TYPE=none -e ZMQ_IDENTIFIER=ground \
  -e ZMQ_PROXY_SERVER=node1-uav-evm node1-uav-evm sh -c \
  'run-aerpawlib ground_coordinator --file /opt/standalone/experiments/orbit.plan > /results/ground.log 2>&1'
docker compose -f $topo exec -d \
  -e ZMQ_IDENTIFIER=tracer -e ZMQ_PROXY_SERVER=node1-uav-evm node1-uav-evm sh -c \
  'run-aerpawlib drone_tracer > /results/tracer.log 2>&1'
docker compose -f $topo exec -d \
  -e ZMQ_IDENTIFIER=orbiter -e ZMQ_PROXY_SERVER=node1-uav-evm node2-uav-evm sh -c \
  'run-aerpawlib drone_orbiter > /results/orbiter.log 2>&1'
```

The ground coordinator reads `orbit.plan`, sends both drones through parallel waypoint legs, has the orbiter circle the tracer at each waypoint, and lands both at the end.

## Add Nodes

Copy one of the `topology.*.yaml` files and edit it. Node IDs must be unique integers from 1 through 255; the ID doubles as the MAVLink system ID:

```yaml
version: 1
experiment: 842
nodes:
  - id: 1
    vehicle: uav
    home: {lat: 35.7274824, lon: -78.6962748, heading: 0}
  - id: 2
    vehicle: ugv
    home: {lat: 35.7273924, lon: -78.6962748, heading: 0}
  - id: 3
    vehicle: uav
    home: {lat: 35.7273024, lon: -78.6962748, heading: 0}
```

Render a matching Compose file and apply it:

```bash
python3 tools/render_topology.py topology.my-nodes.yaml --output docker-compose.my-nodes.yml
docker compose -f docker-compose.my-nodes.yml up --build -d --remove-orphans
```

The renderer creates an explicit C-VM/E-VM pair and result directory for every node. This avoids replica pairing and duplicate system IDs.

## Stop

```bash
docker compose -f docker-compose.uav.yml down
```

Compose preserves files under `results/`.

## Limits

This deployment provides vehicle emulation, `aerpawlib`, a single QGroundControl gateway link, and cross-node `ZmqStateMachine` coordination between processes of the running stack. It does not provide radio applications, channel effects, or shared platform checkpoints. The vendored platform adapter keeps the `aerpawlib` logging and checkpoint method names; checkpoints live only inside one experiment process.

## Checks

```bash
python3 -m pip install --user pytest
python3 -m pytest -q tests
python3 tools/render_topology.py topology.uav.yaml --output /tmp/docker-compose.yml
```
