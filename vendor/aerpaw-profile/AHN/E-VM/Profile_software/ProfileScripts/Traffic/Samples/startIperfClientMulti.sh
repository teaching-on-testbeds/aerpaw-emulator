#!/bin/bash
#
# This script will start an iperf client to the specified destination
#

DESTINATION_IP=172.16.0.1
# Checking the connection via ping to server until it gets it
while ((1)); do
	echo "Looking for connection..."
	ping -c 1 -W 1 $DESTINATION_IP >&/dev/null
	rv=$?
	if (test $rv -eq 0); then
		echo "Got it"
		break
	fi
	sleep 1
done

# total transmit time (in seconds)
IPERF_DURATION=3000
# bandwidth (in MBits / sec)
IPERF_BANDWIDTH=100M
# set iperf index to 1 or 2 to allow for multiple iperf clients
IPERF_PORT=$((5000 + $iperf_index))

# add -u to use UDP instead of the default TCP
# add -R to use reverse direction (from server to client)

#iperf3 -c $DESTINATION_IP -t $IPERF_DURATION

screen -S iperfclient -dm \
	bash -c "stdbuf -oL -eL iperf3 -c $DESTINATION_IP -t $IPERF_DURATION -p $IPERF_PORT -b $IPERF_BANDWIDTH \
       | ts $TS_FORMAT \
       | tee $RESULTS_DIR/$LOG_PREFIX\_iperfclient_log.txt"
