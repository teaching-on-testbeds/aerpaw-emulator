#!/bin/bash
CONFIG_DIR="/opt/open5gs/build/configs/"
PROFILE_DIR="/root/Profiles"

cd $PROFILE_DIR"/ProfileScripts/Radio/Helpers"

#for the core network
screen -S open5gsCore -dm \
	bash -c "stdbuf -oL -eL ./startOpen5GS.sh $CONFIG_DIR/open5gs_nr_core_oai.yaml \
       | ts $TS_FORMAT \
       | tee /root/logs/open5gs.log"
