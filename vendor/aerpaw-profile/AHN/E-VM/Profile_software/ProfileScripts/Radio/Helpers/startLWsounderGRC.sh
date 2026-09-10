#!/bin/bash
GAIN_TX=76
GAIN_RX=30
FREQUENCY=3.32G
RXFREQ=187.5e3
#ARGS="serial=31E74A9"
ARGS=NULL

cd $PROFILE_DIR"/SDR_control/Channel_Sounderv3"
#LW1
python3 LW_CS.py --freq=$FREQUENCY --gaintx=$GAIN_TX --gainrx=$GAIN_RX  --args=$ARGS --txfreq1=812.5e3 --txfreq2=-312.5e3 --rxfreq=$RXFREQ
#LW2
#python3 LW_CS.py --freq=$FREQUENCY --gaintx=$GAIN_TX --gainrx=$GAIN_RX  --args=$ARGS --txfreq1=687.5e3 --txfreq2=-437.5e3 --rxfreq=$RXFREQ
#LW3
#python3 LW_CS.py --freq=$FREQUENCY --gaintx=$GAIN_TX --gainrx=$GAIN_RX  --args=$ARGS --txfreq1=562.5e3 --txfreq2=-562.5e3 --rxfreq=$RXFREQ
#LW4
#python3 LW_CS.py --freq=$FREQUENCY --gaintx=$GAIN_TX --gainrx=$GAIN_RX  --args=$ARGS --txfreq1=437.5e3 --txfreq2=-687.5e3 --rxfreq=$RXFREQ
#LW5
#python3 LW_CS.py --freq=$FREQUENCY --gaintx=$GAIN_TX --gainrx=$GAIN_RX  --args=$ARGS --txfreq1=312.5e3 --txfreq2=-812.5e3 --rxfreq=$RXFREQ
