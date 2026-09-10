# Standalone AERPAW Vehicle Digital Twin

This project runs AERPAW-style virtual vehicles with Docker Compose. Each node has a C-VM container running ArduPilot SITL and MAVLink Router, plus an E-VM container for `aerpawlib` experiments. The Docker bridge acts as an always-connected channel.

The included topology creates a UAV as node 1 and a UGV as node 2. You can add any mix of UAV and UGV nodes in `topology.yaml`.

## Install

Run on an Ubuntu 22.04 or 24.04 `amd64` host:

```bash
sudo apt-get update
sudo apt-get install -y curl git ca-certificates python3 python3-yaml

curl -sSL https://get.docker.com/ | sudo sh
sudo groupadd -f docker; sudo usermod -aG docker $USER
```

Log out and back in so the group change takes effect, then check Docker:

```bash
docker run --rm hello-world
docker compose version
```

## Start

The first build downloads public source for ArduPilot, MAVLink Router, and DroneKit. It does not need a token.

```bash
docker compose up --build -d
docker compose ps
```

Wait until both C-VM services report `healthy`.

The central MAVLink Router gateway aggregates all vehicle system IDs and is
published on the remote host as `127.0.0.1:5760`. To connect QGroundControl
from your workstation through SSH, run:

```bash
ssh -N \
  -L 5760:127.0.0.1:5760 \
  user@remote-host
```

## QGroundControl

Add one TCP link to `localhost:5760` in QGroundControl.

The gateway exposes every vehicle on that one TCP link, so QGroundControl shows
them as separate entries in the vehicle list (the vehicle icon/drop-down in the
toolbar). Each entry corresponds to a system ID in `topology.yaml`:

| Vehicle | System ID | Firmware | Home |
|---|---|---|---|
| UAV | 1 | ArduCopter | 35.7274824, -78.6962748, heading 0 |
| UGV | 2 | ArduRover | 35.7273924, -78.6962748, heading 0 |

Select an entry to switch telemetry. Only the active vehicle is drawn on the
map and HUD, and QGC remembers which vehicle is active between connects.

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
  vehicle settings if you want UAV/UGV labels per node.

## Run Experiments

Run the demo on the UAV:

```bash
docker compose exec node1-uav-evm run-aerpawlib demo_square
```

Run it on the UGV:

```bash
docker compose exec node2-ugv-evm run-aerpawlib demo_square
```

To run both at once:

```bash
docker compose exec -d node1-uav-evm sh -c \
  'run-aerpawlib demo_square > /results/demo.log 2>&1'
docker compose exec -d node2-ugv-evm sh -c \
  'run-aerpawlib demo_square > /results/demo.log 2>&1'
```

Results are available on the host under `results/839/node-1` and `results/839/node-2`.

Place additional Python experiment modules in `experiments/`. Run a module named `experiments/my_experiment.py` with:

```bash
docker compose exec node1-uav-evm run-aerpawlib my_experiment
```

Arguments after the module name pass through to the experiment:

```bash
docker compose exec node1-uav-evm \
  run-aerpawlib my_experiment --output /results/run.csv
```

Open a container shell with:

```bash
docker compose exec node1-uav-evm bash
docker compose exec node1-uav-cvm bash
```

The experiment wrapper arms the simulated vehicle before a run and disarms it afterward. Set `AUTO_ARM: "0"` for a node in `docker-compose.yml` if an experiment handles arming itself.

The E-VM image also provides the AERPAW profile filesystem. `/root/Profiles` points to the vendored `Profile_software` tree, and `/root/startexperiment.sh`, `/root/stopexperiment.sh`, and `/root/reset.sh` point to the matching profile scripts. The image sets `AERPAW_REPO`, `PROFILE_DIR`, and the AERPAW E-VM `bin` directory in the environment and adds that bin directory to `/root/.bashrc`.

The profile scripts are present for path compatibility. Radio, CHEM, and other hardware-dependent programs remain unavailable in this vehicle-only deployment.

## Add Nodes

Edit `topology.yaml`. Node IDs must be unique integers from 1 through 255:

```yaml
version: 1
experiment: 839
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

Regenerate the Compose file and apply the topology:

```bash
python3 tools/render_topology.py topology.yaml
docker compose up --build -d --remove-orphans
```

The renderer creates an explicit C-VM/E-VM pair and result directory for every node. This avoids replica pairing and duplicate system IDs.

## Stop

```bash
docker compose down
```

Compose preserves files under `results/`.

## Limits

This deployment provides vehicle emulation and `aerpawlib`. It does not provide radio applications, channel effects, shared platform checkpoints, or cross-node `ZmqStateMachine` coordination. The vendored platform adapter keeps the `aerpawlib` logging and checkpoint method names; checkpoints live only inside one experiment process.

## Checks

```bash
python3 -m pip install --user pytest
python3 -m pytest -q tests
python3 tools/render_topology.py topology.yaml --output /tmp/docker-compose.yml
docker compose config
```
