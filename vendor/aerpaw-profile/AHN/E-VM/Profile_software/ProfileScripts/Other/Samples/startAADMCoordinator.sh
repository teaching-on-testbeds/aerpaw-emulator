#!/bin/bash

cd "/root/Profiles/ProfileScripts/Other/Helpers"
   
screen -S controller -dm \
       bash -c "stdbuf -oL -eL ./controllerHelper.sh \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_controller_log.txt"	
