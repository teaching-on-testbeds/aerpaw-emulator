#!/bin/bash

export VEHICLE_TYPE="${VEHICLE_TYPE:-drone}" # out of rover, drone, generic

cd $PROFILE_DIR"/ProfileScripts/Vehicle/Helpers"
screen -S vehicle -dm \
       bash -c "
       cd ~/Tests &&
       $AERPAW_PYTHON -u -m aerpawlib \
              --vehicle $VEHICLE_TYPE \
              --script velocity_ok \
              --conn :14550 \
              --output $RESULTS_DIR/$LOG_PREFIX\_vehicleOut.txt \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_vehicle_log.txt"

