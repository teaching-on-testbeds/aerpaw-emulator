#!/bin/bash
mkfifo /root/Power
mkfifo /root/Quality

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

screen -S rxGRC -dm \
       bash -c "stdbuf -oL -eL ./startchannelsounderRXGRC_v2.sh $1 $2 $3 \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\:radio_channelsounderrxgrc_log.txt"

screen -S power -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\:power_log.txt"

screen -S quality -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\:quality_log.txt"
