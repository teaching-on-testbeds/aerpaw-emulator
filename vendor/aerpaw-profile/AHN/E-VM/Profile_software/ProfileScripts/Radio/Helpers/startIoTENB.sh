#!/bin/bash
#
# This script will start an srsLTE ENB process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

# For testbed:
tx_gain=70
freq=915e6

if [ $LAUNCH_MODE == "TESTBED" ]; then
    bash -c "printf 't\n' | /root/npdsch_enodeb -g $tx_gain -f $freq" 
elif [ $LAUNCH_MODE == "EMULATION" ]; then
    bash -c "printf 't\n' | /root/npdsch_enodeb -g $tx_gain -f $freq"
fi
