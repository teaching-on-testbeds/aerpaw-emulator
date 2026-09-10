#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

# start the gNB
screen -S radioGNB -dm \
       bash -c "stdbuf -oL -eL ./start-OAI-gNB-nocore.sh $1 \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_radio_gnb_log_err.txt) \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_gnb_log.txt"

