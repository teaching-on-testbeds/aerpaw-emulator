#!/bin/bash
CONFIG_DIR=/opt/open5gs/build/configs
CONFIG_FILE=$CONFIG_DIR/ho_core.yaml
HELPER_CONFIG=$PROFILE_DIR/ProfileScripts/Radio/Helpers/ho_core.yaml

cd $CONFIG_DIR

interface_name="eth-XM-EVM" 
ip_address=$(ifconfig "$interface_name" | grep -oE 'inet ([0-9]*\.){3}[0-9]*' | awk '{print $2}')

cp "$HELPER_CONFIG" "$CONFIG_FILE"

yq eval ".mme.s1ap[0].addr = \"$ip_address\"" -i "$CONFIG_FILE"
yq eval ".sgwu.gtpu[0].addr = \"$ip_address\"" -i "$CONFIG_FILE"

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

# for the core network
screen -S open5gsCore -dm \
       bash -c "stdbuf -oL -eL ./startOpen5GS.sh $CONFIG_FILE \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_radio_core_log_err.txt) \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_core_log.txt"
