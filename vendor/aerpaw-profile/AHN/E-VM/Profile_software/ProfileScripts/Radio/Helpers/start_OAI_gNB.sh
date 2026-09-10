#!/bin/bash

CHEM_IP_ADDR=$AP_EXPENV_CHEMVM_XE
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM

#!bin/sh

if [[ "$LAUNCH_MODE" == "TESTBED" ]]; then
	echo "starting testbed"
	bash -c "/opt/open5gs/build/misc/db/open5gs-dbctl add 001010000000001 fec86ba6eb707ed08905757b1bb44b8f C42449363BBAD02B66D16BC975D77CC1"
	bash -c "/opt/openairinterface-AERPAW/cmake_targets/ran_build/build/nr-softmodem -O /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf --gNBs.[0].min_rxtxtime 6 -E --continuous-tx"
elif [[ "$LAUNCH_MODE" == "EMULATION" ]]; then
	bash -c "/opt/open5gs/build/misc/db/open5gs-dbctl add 001010000000001 fec86ba6eb707ed08905757b1bb44b8f C42449363BBAD02B66D16BC975D77CC1"
	bash -c "/opt/openairinterface-AERPAW/cmake_targets/ran_build/build/nr-softmodem -O /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf --gNBs.[0].min_rxtxtime 6 -E --continuous-tx --RUs.[0].sdr_addrs vusrp_force_type=b200"
fi
