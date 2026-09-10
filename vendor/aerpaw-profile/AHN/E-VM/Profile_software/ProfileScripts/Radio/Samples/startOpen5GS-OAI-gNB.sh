#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"
# start Open5GS
screen -S open5gsCore -dm \
       bash -c "stdbuf -oL -eL ./startOpen5GS.sh /root/Profiles/ProfileScripts/Radio/Helpers/open5gs_nr_core_oai.yaml \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_radio_core_log_err.txt) \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_open5gs_log.txt"

sleep 2

# start the gNB
screen -S radioGNB -dm \
       bash -c "stdbuf -oL -eL ./start_OAI_gNB.sh \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_radio_gnb_log_err.txt) \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_gnb_log.txt"
