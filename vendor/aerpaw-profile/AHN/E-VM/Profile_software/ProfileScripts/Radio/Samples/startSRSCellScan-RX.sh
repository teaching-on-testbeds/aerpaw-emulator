#!/bin/bash

CELL_SEARCH_DIR="/opt/srsRAN/build/lib/examples/"

RX_GAIN=40
BAND=22
EARFCN_START=6700
EARFCN_END=6702
FREQ_OFFSET=100000000

cd $CELL_SEARCH_DIR

if [ "$LAUNCH_MODE" == "TESTBED" ]; then
    while true; do
        screen -dmS cellSearch bash -c "printf 't\n' | stdbuf -oL -eL ./cell_search -s $EARFCN_START -e $EARFCN_END -b $BAND -g $RX_GAIN | ts $TS_FORMAT | tee -a $RESULTS_DIR/$LOG_PREFIX\_cellsearch.txt" 
    done
elif [ "$LAUNCH_MODE" == "EMULATION" ]; then
    screen -dmS cellSearch bash -c "while true; do 
            printf 't\n' | stdbuf -oL -eL ./cell_search -s $EARFCN_START -e $EARFCN_END -b $BAND -g $RX_GAIN -o $FREQ_OFFSET | ts $TS_FORMAT | tee -a $RESULTS_DIR/$LOG_PREFIX\_cellsearch.txt;
        sleep 1;
    done" 
fi
