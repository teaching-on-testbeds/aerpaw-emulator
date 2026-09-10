#!/bin/bash

# This script checks if a mission plan file violates the rules for .plan files
# It checks for waypoints staying in the geofence, outside of no-go-zones
# as well as for altitude of the waypoints


AERPAW_REPO=${AERPAW_REPO:-/root/AERPAW-Dev}
VALIDATE_MISSION_DIR=$AERPAW_REPO"/OEO/vehicle_oeo"
VALIDATE_MISSION_SCRIPT=$VALIDATE_MISSION_DIR"/validate_mission.py"

SAFETY_CHECKER_DIR=$AERPAW_REPO"/AHN/E-VM/Profile_software/vehicle_control/aerpawlib/aerpawlib"
SAFETY_CHECKER_SCRIPT=$SAFETY_CHECKER_DIR"/safetyChecker.py"

SAFETY_CHECKER_IP="192.168.32.25"
SAFETY_CHECKER_PORT=14580

# uncomment to run a local safety checker instance
# SAFETY_CHECKER_IP="127.0.0.1"
# SAFETY_CHECKER_PORT=15480

GEOFENCE=$AERPAW_REPO"/AHN/C-VM/MAVLink_Filter/Geofences/copter_geofence.kml"
DEFAULT_MISSION=$AERPAW_REPO"/AHN/E-VM/Profile_software/vehicle_control/PreplannedTrajectory/Missions/default.plan"
MISSION_PLAN=${1:-$DEFAULT_MISSION}

DEFAULT_VEHICLE_CONFIG=$AERPAW_REPO"/AHN/C-VM/MAVLink_Filter/Geofences/safety_checker_config_copter.yaml"
VEHICLE_CONFIG=${2:-$DEFAULT_VEHICLE_CONFIG}

# uncomment to run a local safety checker instance
# cd $SAFETY_CHECKER_DIR
# bash -c "python3 $SAFETY_CHECKER_SCRIPT --port $SAFETY_CHECKER_PORT --vehicle_config $VEHICLE_CONFIG" &

cd $VALIDATE_MISSION_DIR
bash -c "python3 $VALIDATE_MISSION_SCRIPT $MISSION_PLAN $SAFETY_CHECKER_IP $SAFETY_CHECKER_PORT"

# kill safety checker server running in background
kill %%
