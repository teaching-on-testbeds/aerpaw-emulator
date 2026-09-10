#!/bin/bash
CONFIG_DIR=/opt/open5gs/build/configs

cd $CONFIG_DIR

interface_name="eth-XM-EVM"
ip_address=$(ifconfig "$interface_name" | grep -oE 'inet ([0-9]*\.){3}[0-9]*' | awk '{print $2}')

yq eval ".upf.gtpu[0].addr = \"$ip_address\"" -i open5gs_nr_core_oai.yaml
yq eval ".amf.ngap[0].addr = \"$ip_address\"" -i open5gs_nr_core_oai.yaml

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

# for the core network
screen -S open5gsCore -dm \
	bash -c "stdbuf -oL -eL ./startOpen5GS.sh $CONFIG_DIR/open5gs_nr_core_oai.yaml \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_radio_core_log_err.txt) \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_radio_core_log.txt"

# Wait for the core network to start
sleep 2

# Update FlexRIC configuration file with the correct IP address
cat > /usr/local/etc/flexric/flexric.conf << EOF
[NEAR-RIC]
NEAR_RIC_IP = $ip_address
NEAR_RIC_PORT = 36421

[IAPP]
IAPP_IP = $ip_address
IAPP_PORT = 36422

[XAPP]
DB_DIR = /tmp/
EOF


# Start the flexRIC
screen -S flexRIC -dm \
    bash -c "stdbuf -oL -eL ./startFlexRIC.sh \
       2> >(ts $TS_FORMAT >> $RESULTS_DIR/${LOG_PREFIX}_flexric_log_err.txt) \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_flexric_log.txt"

