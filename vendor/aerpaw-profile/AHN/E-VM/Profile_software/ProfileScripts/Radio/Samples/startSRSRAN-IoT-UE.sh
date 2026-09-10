#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"
screen -S radioUE -dm \
       bash -c "stdbuf -oL -eL ./startIoTUE.sh \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_radio_ue_log_err.txt) \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_ue_log.txt"
