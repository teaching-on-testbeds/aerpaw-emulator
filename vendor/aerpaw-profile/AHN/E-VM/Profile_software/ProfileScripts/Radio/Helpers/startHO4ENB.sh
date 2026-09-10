#!/bin/bash
#
# This script will start an srsLTE ENB process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

CONFIG_PATH=/root/Profiles/ProfileScripts/Radio/Helpers/Handover/rrHO4.conf

interface_name="eth-XM-EVM"
ip_address=$(ifconfig "$interface_name" | grep -oE 'inet ([0-9]*\.){3}[0-9]*' | awk '{print $2}')

# For testbed:
tx_gain=70
rx_gain=40
earfcn=6700
dl_freq=3410e6
ul_freq=3320e6
n_prb=50
mme_addr=192.168.103.1
gtp_s1c_bind_addr=$ip_address

if [ $LAUNCH_MODE == "TESTBED" ]; then
    bash -c "printf 't\n' | srsenb --rf.tx_gain=$tx_gain \
        --rf.rx_gain=$rx_gain \
        --rf.dl_earfcn=$earfcn \
        --enb.n_prb=$n_prb \
        --enb_files.rr_config=$CONFIG_PATH \
        --enb.mme_addr=$mme_addr \
        --enb.gtp_bind_addr=$gtp_s1c_bind_addr \
        --enb.s1c_bind_addr=$gtp_s1c_bind_addr \
        --enb.enb_id=0x19E"
elif [ $LAUNCH_MODE == "EMULATION" ]; then
    bash -c "printf 't\n' | srsenb --rf.srate=11.52e6 \
        --rf.tx_gain=$tx_gain \
        --rf.rx_gain=$rx_gain \
        --rf.dl_freq=$dl_freq \
        --rf.ul_freq=$ul_freq \
        --enb.n_prb=$n_prb \
        --enb_files.rr_config=$CONFIG_PATH \
        --enb.mme_addr=$mme_addr \
        --enb.gtp_bind_addr=$gtp_s1c_bind_addr \
        --enb.s1c_bind_addr=$gtp_s1c_bind_addr \
        --enb.enb_id=0x19E"
fi
