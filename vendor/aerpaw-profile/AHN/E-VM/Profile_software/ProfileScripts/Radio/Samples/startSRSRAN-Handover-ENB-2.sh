#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

# for the ENB
screen -S radioENB2 -dm \
       bash -c "stdbuf -oL -eL ./startHO2ENB.sh \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_radio_enb2_log_err.txt) \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_enb2_log.txt"
