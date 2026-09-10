#!/bin/bash
mkfifo /root/Power1
mkfifo /root/Quality1

mkfifo /root/Power2
mkfifo /root/Quality2


cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

screen -S LWCSGRC -dm \
       bash -c "stdbuf -oL -eL ./startLWsounderGRC.sh \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_LW_channelsoundergrc_log.txt"



screen -S power1 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power1\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_power1_log.txt"

screen -S quality1 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality1\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_quality1_log.txt"



screen -S power2 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power2\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_power2_log.txt"

screen -S quality2 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality2\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_quality2_log.txt"

