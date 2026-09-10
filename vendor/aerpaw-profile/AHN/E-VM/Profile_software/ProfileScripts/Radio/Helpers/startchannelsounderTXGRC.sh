#!/bin/bash
GAIN_TX=76
OFFSET=250e3
SAMP_RATE=2e6
SPS=16

if [ $LAUNCH_MODE == "TESTBED" ]
then
#To select a specific device
#ARGS="serial=31E74A9"
ARGS=NULL
elif [ $LAUNCH_MODE == "EMULATION" ]
then
ARGS=NULL
else
  echo "Specify correct mode"
fi

cd $PROFILE_DIR"/SDR_control/Channel_Sounderv3"
python3 CSwSNRTX.py --freq $TX_FREQ --gaintx $GAIN_TX --args $ARGS --offset $OFFSET --samp-rate $SAMP_RATE --sps $SPS
