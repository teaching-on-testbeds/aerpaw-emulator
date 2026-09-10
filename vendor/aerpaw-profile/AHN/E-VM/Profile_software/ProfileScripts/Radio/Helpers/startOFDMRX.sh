#!/bin/bash

RATE=1000000
FREQUENCY=3.4G
#To select a specific device
#ARGS="serial=31E74A9"
ARGS=NULL
GAIN=30
#For MOD:
#2 -> BPSK
#4 -> QPSK
#16 -> 16QAM
MOD=4
#Duration is measured in seconds
duration=60

if [ $LAUNCH_MODE == "TESTBED" ]
then
   mode='uhd'
   cd $PROFILE_DIR"/SDR_control/OFDM/RX"
   if [ $MOD == 2 ] ; then
      python3 rx_ofdm_bpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   elif [ $MOD == 4 ] ; then
      python3 rx_ofdm_qpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   elif [ $MOD == 16 ] ; then
      python3 rx_ofdm_16qam.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   fi
elif [ $LAUNCH_MODE == "EMULATION" ]
then
   mode='uhd'
   cd $PROFILE_DIR"/SDR_control/OFDM/RX"
   if [ $MOD == 2 ] ; then
      python3 rx_ofdm_bpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   elif [ $MOD == 4 ] ; then
      python3 rx_ofdm_qpsk.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   elif [ $MOD == 16 ] ; then
      python3 rx_ofdm_16qam.py --source $mode --samp-rate $RATE --freq $FREQUENCY --args $ARGS --rx-gain $GAIN --duration $duration
   fi
else
  echo "Specify correct mode"
fi
