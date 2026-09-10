#!/bin/bash

cd "/root/Profiles/ProfileScripts/Other/Helpers"

screen -S report -dm \
       bash -c "stdbuf -oL -eL ./UAVrequestHelper.sh \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_report_log.txt"

