#!/bin/bash

# --------------------------------------------
# stopexperiment.sh
# --------------------------------------------

# Get the list of valid screen sessions quietly
sessions=$(screen -ls 2>/dev/null | \
    grep -wv -e 'There' -e 'No' -e 'remoteConsole' -e 'remoteServer' \
              -e 'OEOConsole' -e 'OEOServer' -e 'Socket' -e 'Sockets' | \
    awk '{print $1}' | sed '/^[[:space:]]*$/d')

# Quit only if there are any
if [ -n "$sessions" ]; then
    for scr in $sessions; do
        echo "Quitting from $scr"
        screen -S "$scr" -X quit >/dev/null 2>&1
    done
fi

# Delete network interfaces quietly
ip link delete ogstun 2>/dev/null
ip link delete tun_srsue 2>/dev/null
ip link delete srs_spgw_sgi 2>/dev/null

# For channel sounder experiment
rm -f /root/Power /root/Quality /root/SNR
pkill open5g* >/dev/null 2>&1

# Stop zombie processes
kill -9 $(ps aux | awk '/srsenb/ && !/awk/ || /srsue/ && !/awk/{print $2}') >/dev/null 2>&1

# Wipe dead screen sessions quietly
screen -wipe >/dev/null 2>&1
