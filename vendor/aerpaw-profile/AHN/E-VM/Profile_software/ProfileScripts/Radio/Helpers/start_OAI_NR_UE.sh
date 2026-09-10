#!/bin/bash
#
# This script will start an OAI NR UE process

TA=-280

rm -rf /dev/net/
mkdir /dev/net
mknod /dev/net/tun c 10 200


if [[ $LAUNCH_MODE == "TESTBED" ]]; then
  bash -c "/opt/openairinterface-AERPAW/cmake_targets/ran_build/build/nr-uesoftmodem -r 51 --numerology 1 --band 78 -C 3404640000 --ssb 186 --ue-fo-compensation -E --uicc0.imsi 001010000000001 --uicc0.key fec86ba6eb707ed08905757b1bb44b8f --uicc0.opc C42449363BBAD02B66D16BC975D77CC1 --uicc0.dnn internet --uicc0.nssai_sst 1"
elif [[ $LAUNCH_MODE == "EMULATION" ]]; then
  bash -c "/opt/openairinterface-AERPAW/cmake_targets/ran_build/build/nr-uesoftmodem -r 51 --numerology 1 --band 78 -C 3404640000 --ssb 186 --ue-fo-compensation -E --uicc0.imsi 001010000000001 --uicc0.key fec86ba6eb707ed08905757b1bb44b8f --uicc0.opc C42449363BBAD02B66D16BC975D77CC1 --uicc0.dnn internet --uicc0.nssai_sst 1 --usrp-args vusrp_force_type=b200 -A $TA" 
fi
