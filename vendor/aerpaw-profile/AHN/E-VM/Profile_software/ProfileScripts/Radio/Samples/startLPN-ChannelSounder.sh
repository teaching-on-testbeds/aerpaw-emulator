#!/bin/bash
mkfifo /root/Power1
mkfifo /root/Quality1
mkfifo /root/Power2
mkfifo /root/Quality2
mkfifo /root/Power3
mkfifo /root/Quality3
mkfifo /root/Power4
mkfifo /root/Quality4
mkfifo /root/Power5
mkfifo /root/Quality5
mkfifo /root/Power6
mkfifo /root/Quality6
mkfifo /root/Power7
mkfifo /root/Quality7
mkfifo /root/Power8
mkfifo /root/Quality8
mkfifo /root/Power9
mkfifo /root/Quality9
mkfifo /root/Power10
mkfifo /root/Quality10




cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

screen -S LPNCSGRC -dm \
       bash -c "stdbuf -oL -eL ./startLPNsounderGRC.sh \
       2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_LPN_channelsoundergrc_log.txt"



screen -S powerLPN1 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power1\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN1_log.txt"

screen -S qualityLPN1 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality1\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN1_log.txt"

screen -S powerLPN2 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power2\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN2_log.txt"

screen -S qualityLPN2 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality2\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN2_log.txt"

screen -S powerLPN3 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power3\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN3_log.txt"

screen -S qualityLPN3 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality3\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN3_log.txt"

screen -S powerLPN4 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power4\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN4_log.txt"

screen -S qualityLPN4 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality4\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN4_log.txt"

screen -S powerLPN5 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power5\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN5_log.txt"

screen -S qualityLPN5 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality5\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN5_log.txt"

screen -S powerLPN6 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power6\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN6_log.txt"

screen -S qualityLPN6 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality6\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN6_log.txt"

screen -S powerLPN7 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power7\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN7_log.txt"

screen -S qualityLPN7 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality7\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN7_log.txt"

screen -S powerLPN8 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power8\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN8_log.txt"

screen -S qualityLPN8 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality8\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN8_log.txt"

screen -S powerLPN9 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power9\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN9_log.txt"

screen -S qualityLPN9 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality9\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN9_log.txt"

screen -S powerLPN10 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Power10\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_powerLPN10_log.txt"

screen -S qualityLPN10 -dm        bash -c "stdbuf -oL -eL od -f -w4 /root/Quality10\
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_qualityLPN10_log.txt"





