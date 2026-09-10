#!/bin/bash
#
# This script will start an srsLTE UE process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
tx_gain=70
rx_gain=40
#earfcn=6700
dl_freq=3410e6
ul_freq=3320e6
imsi=00$((1010123456700 + $node_num))

rm -rf /dev/net/
mkdir /dev/net
mknod /dev/net/tun c 10 200
ip tuntap add mode tun tun_srsue
ip link set dev tun_srsue mtu 1500

if [ $LAUNCH_MODE == "TESTBED" ]; then
	bash -c "printf 't\n' | srsue --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain \
   --rat.eutra.dl_freq=$dl_freq --rat.eutra.ul_freq=$ul_freq --usim.imsi=$imsi \
    --usim.algo=mil --usim.opc=63bfa50ee6523365ff14c1f45f88737d"
elif [ $LAUNCH_MODE == "EMULATION" ]; then
	bash -c "printf 't\n' | srsue --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain \
   --rat.eutra.dl_freq=$dl_freq --rat.eutra.ul_freq=$ul_freq --usim.imsi=$imsi \
   --usim.algo=mil --usim.opc=63bfa50ee6523365ff14c1f45f88737d --rf.srate=11.52e6"
fi
