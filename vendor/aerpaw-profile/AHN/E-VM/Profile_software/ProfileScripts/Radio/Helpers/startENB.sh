#!/bin/bash
#
# This script will start an srsLTE ENB process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

# For testbed:
tx_gain=70
rx_gain=40
#dl_earfcn=6700
dl_freq=3410e6
ul_freq=3320e6
n_prb=50

if [ $LAUNCH_MODE == "TESTBED" ]; then
	bash -c "printf 't\n' | srsenb --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain --rf.dl_freq=$dl_freq --rf.ul_freq=$ul_freq --enb.n_prb=$n_prb"
elif [ $LAUNCH_MODE == "EMULATION" ]; then
	bash -c "printf 't\n' | srsenb --rf.srate=11.52e6 --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain --rf.dl_freq=$dl_freq --rf.ul_freq=$ul_freq --enb.n_prb=$n_prb"
fi
