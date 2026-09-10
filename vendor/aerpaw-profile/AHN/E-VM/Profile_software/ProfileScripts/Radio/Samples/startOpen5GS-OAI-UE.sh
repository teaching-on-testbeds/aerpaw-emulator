#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"
screen -S radioNRUE -dm \
	bash -c "stdbuf -oL -eL ./start_OAI_NR_UE.sh \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_radio_err.txt) \
        | ts $TS_FORMAT \
        | tee $RESULTS_DIR/$LOG_PREFIX\_radio_log.txt"
