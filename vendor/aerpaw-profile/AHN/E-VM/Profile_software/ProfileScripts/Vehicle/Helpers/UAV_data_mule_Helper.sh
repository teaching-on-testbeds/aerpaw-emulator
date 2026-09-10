#!/bin/bash
#
# This script is used for UAV data mule

#

C_VM_ADDR="192.168.32.25"
SAFETY_CHECKER_PORT=14580

cd $PROFILE_DIR"/AADMChallenge/PortableNode"
$AERPAW_PYTHON -u -m aerpawlib \
    --vehicle $VEHICLE_TYPE \
    --script uav_data_mule \
    --conn :14550 \
    --safety_checker_ip $C_VM_ADDR \
    --safety_checker_port $SAFETY_CHECKER_PORT
#    --output $RESULTS_DIR/$LOG_PREFIX\_vehicleOut.txt
