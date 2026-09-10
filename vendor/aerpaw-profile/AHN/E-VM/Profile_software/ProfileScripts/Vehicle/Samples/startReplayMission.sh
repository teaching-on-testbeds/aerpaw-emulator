#!/bin/bash

export VEHICLE_TYPE="${VEHICLE_TYPE:-rover}" # out of rover, drone, generic

# Replay a recorded MAVLink mission into CHEM and OEO Console.

export REPLAY_MISSION="${REPLAY_MISSION:-$PROFILE_DIR/vehicle_control/PreplannedTrajectory/Missions/rover_sample_replay.tlog}"
NODE_NUM=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
export REPLAY_OEO_AGENT_ID="${NODE_NUM:-99}"
export REPLAY_VEHICLE_LOG_OUTPUT="${REPLAY_VEHICLE_LOG_OUTPUT:-$RESULTS_DIR/${LOG_PREFIX}_replay_vehicleOut.txt}"
export REPLAY_VEHICLE_STDOUT_LOG="${REPLAY_VEHICLE_STDOUT_LOG:-$RESULTS_DIR/${LOG_PREFIX}_vehicle_log.txt}"
export REPLAY_VEHICLE_STDERR_LOG="${REPLAY_VEHICLE_STDERR_LOG:-$RESULTS_DIR/${LOG_PREFIX}_vehicle_log_err.txt}"

if [ "$REPLAY_VEHICLE_LOG_OUTPUT" = "$REPLAY_VEHICLE_STDOUT_LOG" ] || \
   [ "$REPLAY_VEHICLE_LOG_OUTPUT" = "$REPLAY_VEHICLE_STDERR_LOG" ] || \
   [ "$REPLAY_VEHICLE_STDOUT_LOG" = "$REPLAY_VEHICLE_STDERR_LOG" ]; then
    echo "Replay mission generated output files must be unique:" >&2
    echo "  REPLAY_VEHICLE_LOG_OUTPUT=$REPLAY_VEHICLE_LOG_OUTPUT" >&2
    echo "  REPLAY_VEHICLE_STDOUT_LOG=$REPLAY_VEHICLE_STDOUT_LOG" >&2
    echo "  REPLAY_VEHICLE_STDERR_LOG=$REPLAY_VEHICLE_STDERR_LOG" >&2
    exit 1
fi


cd $PROFILE_DIR"/ProfileScripts/Vehicle/Helpers"
screen -S vehicle -dm \
       bash -c "stdbuf -oL -eL python3 ./replay_mission.py \"$REPLAY_MISSION\" \
       --oeo-agent-id \"$REPLAY_OEO_AGENT_ID\" \
       --vehicle-log-output \"$REPLAY_VEHICLE_LOG_OUTPUT\" \
       2> >(ts $TS_FORMAT >> \"$REPLAY_VEHICLE_STDERR_LOG\") \
       | ts $TS_FORMAT \
       | tee \"$REPLAY_VEHICLE_STDOUT_LOG\""
