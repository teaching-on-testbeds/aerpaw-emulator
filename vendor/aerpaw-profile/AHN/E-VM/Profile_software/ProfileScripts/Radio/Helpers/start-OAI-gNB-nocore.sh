#!/bin/bash

CHEM_IP_ADDR=$AP_EXPENV_CHEMVM_XE
node_num=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM

#!bin/sh

ETH_XM_VM_IP=$(ip -4 addr show eth-XM-EVM | grep -oP '(?<=inet\s)\d+(\.\d+){3}')


if [[ "$LAUNCH_MODE" == "TESTBED" ]]; then
	echo "starting testbed"
	if [ -n "$1" ]; then
		sed -i "s/amf_ip_address[[:space:]]*=[[:space:]]*([[:space:]]*{[[:space:]]*ipv4[[:space:]]*=[[:space:]]*\"[^\"]*\"/amf_ip_address      = ( { ipv4       = \"$1\"/" /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf
		sed -i "s/near_ric_ip_addr[[:space:]]*=[[:space:]]*\"[^\"]*\"/near_ric_ip_addr  = \"$1\"/" /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf
		sed -i "s|GNB_IPV4_ADDRESS_FOR_NG_AMF[[:space:]]*=[[:space:]]*\"[^\"]*\"|GNB_IPV4_ADDRESS_FOR_NG_AMF = \"${ETH_XM_VM_IP}/24\"|" /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf
		sed -i "s|GNB_IPV4_ADDRESS_FOR_NGU[[:space:]]*=[[:space:]]*\"[^\"]*\"|GNB_IPV4_ADDRESS_FOR_NGU = \"${ETH_XM_VM_IP}/24\"|" /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf

	fi
	bash -c "/opt/openairinterface-AERPAW/cmake_targets/ran_build_e2/build/nr-softmodem -O /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf --gNBs.[0].min_rxtxtime 6 -E --continuous-tx"
elif [[ "$LAUNCH_MODE" == "EMULATION" ]]; then
	if [ -n "$1" ]; then
		sed -i "s/amf_ip_address[[:space:]]*=[[:space:]]*([[:space:]]*{[[:space:]]*ipv4[[:space:]]*=[[:space:]]*\"[^\"]*\"/amf_ip_address      = ( { ipv4       = \"$1\"/" /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf
		sed -i "s/near_ric_ip_addr[[:space:]]*=[[:space:]]*\"[^\"]*\"/near_ric_ip_addr  = \"$1\"/" /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf
		sed -i "s|GNB_IPV4_ADDRESS_FOR_NG_AMF[[:space:]]*=[[:space:]]*\"[^\"]*\"|GNB_IPV4_ADDRESS_FOR_NG_AMF = \"${ETH_XM_VM_IP}/24\"|" /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf
		sed -i "s|GNB_IPV4_ADDRESS_FOR_NGU[[:space:]]*=[[:space:]]*\"[^\"]*\"|GNB_IPV4_ADDRESS_FOR_NGU = \"${ETH_XM_VM_IP}/24\"|" /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf

	fi
	bash -c "/opt/openairinterface-AERPAW/cmake_targets/ran_build_e2/build/nr-softmodem -O /root/Profiles/ProfileScripts/Radio/Helpers/gnb.sa.band78.fr1.51PRB.usrpb210.conf --gNBs.[0].min_rxtxtime 6 -E --continuous-tx --RUs.[0].sdr_addrs vusrp_force_type=b200"
fi

