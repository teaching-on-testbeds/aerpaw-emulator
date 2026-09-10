#!/bin/bash
GAIN_RX=30
SERIAL_NUM="${1:-}"
FREQUENCY="${2:-3.32G}"
CHANNEL="${3:-0}"

if [ $LAUNCH_MODE == "TESTBED" ]
then
#To select a specific device
#ARGS="serial=31E74A9"
ARGS="serial=$SERIAL_NUM"
elif [ $LAUNCH_MODE == "EMULATION" ]
then
ARGS=NULL
else
  echo "Specify correct mode"
fi

cd $PROFILE_DIR"/SDR_control/Channel_Sounderv4"
python3 CSRX_noGUI.py --freq $FREQUENCY --gainrx $GAIN_RX --channel $CHANNEL --args $ARGS
