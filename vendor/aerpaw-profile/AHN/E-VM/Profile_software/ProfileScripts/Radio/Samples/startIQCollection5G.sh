#!/bin/bash

IQ_CONFIG=/root/Profiles/SDR_control/aerpaw-iq-collection/oai_5g_3309MHz_51PRB.toml

screen -S IQ -dm \
  bash -c "stdbuf -oL -eL /root/Profiles/SDR_control/aerpaw-iq-collection/build/iq-agent/iq-agent \
        $IQ_CONFIG \
        2>&1 | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_IQ_log.txt"
