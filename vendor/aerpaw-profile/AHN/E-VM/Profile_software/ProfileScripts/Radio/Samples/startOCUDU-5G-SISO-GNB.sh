#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

interface_name="eth-XM-EVM"
ip_address=$(ifconfig "$interface_name" | grep -oE 'inet ([0-9]*\.){3}[0-9]*' | awk '{print $2}')

sed -i "s/^amf_bind_addr=.*/amf_bind_addr=$ip_address/" startOCUDU-5G-SISO-GNB.sh

# for the gNB
screen -S radioGNB -dm \
    bash -c "stdbuf -oL -eL startOCUDU-5G-SISO-GNB.sh \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_radio_gnb_log_err.txt) \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_gnb_log.txt"
