#!/bin/bash
#
# This script will start an srsLTE ENB process for MIMO
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

# For testbed:
tx_gain=70
rx_gain=40
#earfcn=6700
n_prb=25
dl_freq=3410e6
ul_freq=3320e6

#for MIMO configuration
tm=4 # closed loop spatial multiplexing
nof_ports=2



if [ $LAUNCH_MODE == "TESTBED" ]; then
    bash -c "printf 't\n' | srsenb --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain \
    --rf.dl_freq=$dl_freq --rf.ul_freq=$ul_freq --enb.n_prb=$n_prb \
    --enb.tm=$tm --enb.nof_ports=$nof_ports" 
elif [ $LAUNCH_MODE == "EMULATION" ]
then
    bash -c "printf 't\n' | srsenb --rf.device_args=\"num_channels=2\" --rf.srate=11.52e6 \
    --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain \
    --enb.nof_ports=$nof_ports --enb.n_prb=$n_prb --rf.dl_freq=$dl_freq --rf.ul_freq=$ul_freq --enb.tm=$tm "
fi
