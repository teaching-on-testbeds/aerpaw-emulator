#!/bin/bash
#
# This script will start an srsLTE ENB process
#
# needs to be called with MODE=IQ_EMULATION or MODE=TESTBED

CONFIG_PATH=/root/Profiles/ProfileScripts/Radio/Helpers/5G/rr5G.conf

# For testbed:
tx_gain=70
rx_gain=40
mme_addr=192.168.103.1
gtp_s1c_bind_addr=192.168.103.2
pdsch_mcs=10
pusch_mcs=10

if [ $LAUNCH_MODE == "TESTBED" ]; then
    bash -c "printf 't\n' | srsenb --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain --enb.mme_addr=$mme_addr --enb.n_prb=50 --enb_files.rr_config=$CONFIG_PATH --scheduler.nr_pdsch_mcs=$pdsch_mcs --scheduler.nr_pusch_mcs=$pusch_mcs --enb.gtp_bind_addr=$gtp_s1c_bind_addr --enb.s1c_bind_addr=$gtp_s1c_bind_addr"
elif [ $LAUNCH_MODE == "EMULATION" ]; then
    bash -c "printf 't\n' | srsenb --rf.tx_gain=$tx_gain --rf.rx_gain=$rx_gain --enb.mme_addr=$mme_addr --enb.n_prb=50 --enb_files.rr_config=$CONFIG_PATH --scheduler.nr_pdsch_mcs=$pdsch_mcs --scheduler.nr_pusch_mcs=$pusch_mcs --enb.gtp_bind_addr=$gtp_s1c_bind_addr --enb.s1c_bind_addr=$gtp_s1c_bind_addr"
fi
