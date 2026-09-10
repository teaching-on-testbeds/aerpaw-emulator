#!/bin/bash
GAIN_RX=30
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
python3 CSwSNRRX.py --freq $RX_FREQ --gainrx $GAIN_RX --noise 0 --args $ARGS --offset $OFFSET --samp-rate $SAMP_RATE --sps $SPS
