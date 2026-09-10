#!/bin/bash
GAIN_TX=76
GAIN_RX=30
FREQUENCY=3.32G
TXFREQ=187.5e3
#ARGS="serial=31E74A9"
ARGS=NULL

cd $PROFILE_DIR"/SDR_control/Channel_Sounderv3"
python3 LPN_CS.py --freq=$FREQUENCY --gaintx=$GAIN_TX --gainrx=$GAIN_RX  --args=$ARGS --txfreq=$TXFREQ \
--rxfreq1=812.5e3 \
--rxfreq2=-312.5e3 \
--rxfreq3=687.5e3 \
--rxfreq4=-437.5e3 \
--rxfreq5=562.5e3 \
--rxfreq6=-562.5e3 \
--rxfreq7=437.5e3 \
--rxfreq8=-687.5e3 \
--rxfreq9=312.5e3 \
--rxfreq10=-812.5e3
