#!/bin/bash
#
# This script will start an iperf server
#

# add -u to use UDP instead of the default TCP
if [ -z "$(ifconfig oaitun_ue1 2>/dev/null | awk '/inet /{print $2}')" ]; then
	echo "tuntap device does not exist or has no IP address"
	exit 1
fi

#iperf3 -s
screen -S iperfserver -dm \
	bash -c "stdbuf -oL -eL iperf3 -s -u \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_iperfserver_log.txt"
