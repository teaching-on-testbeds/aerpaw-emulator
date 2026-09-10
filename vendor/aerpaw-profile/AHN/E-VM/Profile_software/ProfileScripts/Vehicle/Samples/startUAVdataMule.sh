#!/bin/bash

export VEHICLE_TYPE="${VEHICLE_TYPE:-drone}" 

# UAV Data Mule sample application

cd $PROFILE_DIR"/ProfileScripts/Vehicle/Helpers"
screen -S vehicle -dm \
       bash -c "stdbuf -oL -eL ./UAV_data_mule_Helper.sh \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_vehicle_log.txt"	    
