#!/bin/bash

MGN_FILE=$PROFILE_DIR/ProfileScripts/Traffic/Helpers/RX.mgn

screen -S mgenreceiver -dm \
	bash -c "stdbuf -oL -eL mgen input $MGN_FILE \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_mgenreceiver_log.txt"
