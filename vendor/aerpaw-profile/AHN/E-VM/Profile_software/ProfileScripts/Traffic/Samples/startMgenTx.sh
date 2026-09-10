#!/bin/bash

# script to start MGEN sender

MGN_FILE=$PROFILE_DIR/ProfileScripts/Traffic/Helpers/TX.mgn

screen -S mgensender -dm \
	bash -c "stdbuf -oL -eL mgen input $MGN_FILE \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_mgensender_log.txt"
