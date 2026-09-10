#!/bin/bash
#
# This script will start an OCUDU (srsRAN-based O-CU/O-DU) gNB process
#
# needs to be called with MODE=EMULATION or MODE=TESTBED

CONFIG_PATH=/root/Profiles/ProfileScripts/Radio/Helpers/5G/gnb.yaml

# For testbed:
tx_gain=70
rx_gain=40
amf_addr=192.168.103.1
amf_bind_addr=192.168.103.2
#pdsch_mcs=10
#pusch_mcs=10

if [ $LAUNCH_MODE == "TESTBED" ]; then
    bash -c "printf 't\n' | gnb -c $CONFIG_PATH --ru_sdr.tx_gain=$tx_gain --ru_sdr.rx_gain=$rx_gain --ru_sdr.clock=external --cu_cp.amf.addr=$amf_addr --cu_cp.amf.bind_addr=$amf_bind_addr"
elif [ $LAUNCH_MODE == "EMULATION" ]; then
    bash -c "printf 't\n' | gnb -c $CONFIG_PATH --ru_sdr.tx_gain=$tx_gain --ru_sdr.rx_gain=$rx_gain --cu_cp.amf.addr=$amf_addr --cu_cp.amf.bind_addr=$amf_bind_addr"
fi
