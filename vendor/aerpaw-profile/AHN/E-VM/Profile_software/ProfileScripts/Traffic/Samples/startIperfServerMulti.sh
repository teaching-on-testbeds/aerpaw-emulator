#!/bin/bash
#
# This script will start an iperf server 
#

# add -u to use UDP instead of the default TCP 

#iperf3 -s
screen -S iperfserver -dm \
       bash -c "stdbuf -oL -eL iperf3 -s -p 5001 \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_iperfserver1_log.txt"

screen -S iperfserver2 -dm \
       bash -c "stdbuf -oL -eL iperf3 -s -p 5003 \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_iperfserver2_log.txt"
