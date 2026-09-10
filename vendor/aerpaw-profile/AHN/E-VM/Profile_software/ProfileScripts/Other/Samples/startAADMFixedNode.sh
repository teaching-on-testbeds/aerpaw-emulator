#!/bin/bash

cd "/root/Profiles/ProfileScripts/Other/Helpers"
   
screen -S responder -dm \
       bash -c "stdbuf -oL -eL ./responderHelper.sh \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_responder_log.txt"	
