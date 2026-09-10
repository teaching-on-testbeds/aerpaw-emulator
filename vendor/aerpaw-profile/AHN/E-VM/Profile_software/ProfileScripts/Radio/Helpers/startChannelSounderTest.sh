#!/bin/bash
##### THIS HAS BEEN DEPRECATED #####
cd $PROFILE_DIR"/ProfileScripts/Radio"

NODE_ID=$AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM
#C_VM_IP_VAR="AP_EXPENV_CVM_${NODE_ID}_XE"
# Get C_VM ip for accessing checkpoint server
C_VM_HOST=${!C_VM_IP_VAR}
echo $C_VM_HOST
# Checkpoint server port
C_VM_PORT=12435

# Set variables needed for script
nodes=($AP_EXPENV_SET_NODES)
num_nodes=${#nodes[@]}
index=$((NODE_ID - 1))
# Get name of this AFRN
AFRN_ID="${nodes[index]}"
echo $AFRN_ID

function log_to_oeo () {
    msg="${AFRN_ID}:$1"
    echo $msg
    curl --silent --output /dev/null -X POST http://$C_VM_HOST:$C_VM_PORT/oeo_msg/INFO/$(echo -n $msg | base64 -w 0)
}

post="curl -X POST http://$C_VM_HOST:$C_VM_PORT/checkpoint/$1"

while ((1)); do
    # Check what state this node should be in
    response=$(curl --silent -X GET http://$C_VM_HOST:$C_VM_PORT/checkpoint/string/$AFRN_ID | python3 -c "import sys, urllib.parse;  print(urllib.parse.unquote(sys.stdin.read()))")
    verb=$(echo "$response" | cut -d',' -f1)
    if [ -z $verb ]; then
        sleep 1
        continue
    elif [ $verb == "transmit" ]; then
	IFS=',' read -r verb serial_num channel frequency <<< "$response"
        # Start transmitting
        log_to_oeo "Transmitting with Serial $serial_num,Channel $channel,Frequency $frequency"
        # Make sure log is marked with transmitter
	# Resets log timestamp (because $LOG_PREFIX is only set when startexperiment.sh is run and this experiment generates multiple log files at different times)
	export LOG_PREFIX="$AFRN_ID:$serial_num:$frequency:$channel:$(date +%Y-%m-%d_%H_%M_%S)"
        ./Samples/startGNURadio-ChannelSounder-TX_v2.sh $serial_num $frequency $channel

	# Wait for transmitter screen to start
	while ! ( screen -ls | grep -q txGRC ); do
	    sleep 0.2
	done

	while [ $(echo "$response" | cut -d',' -f1) == "transmit" ]; do
	    sleep 1
	    response=$(curl --silent -X GET http://$C_VM_HOST:$C_VM_PORT/checkpoint/string/$AFRN_ID | python3 -c "import sys, urllib.parse;  print(urllib.parse.unquote(sys.stdin.read()))")
	done

        log_to_oeo "Stopping transmitting"
        screen -S txGRC -X quit
	# Notify control script that this transmitter is done
        curl --silent -X POST http://$C_VM_HOST:$C_VM_PORT/checkpoint/bool/transmitter_finished

        sleep 1
    elif [ $verb == "receive" ]; then
	IFS=',' read -r verb serial_num channel frequency transmitter <<< "$response"
        # Reset checkpoint variable
        curl --silent -X POST http://$C_VM_HOST:$C_VM_PORT/checkpoint/string/$AFRN_ID?val=
        # Start receiving
        log_to_oeo "Receiving from $transmitter with Serial $serial_num,Channel $channel,Frequency $frequency"

        # Make sure log is marked with transmitter
	# Resets log timestamp (because $LOG_PREFIX is only set when startexperiment.sh is run and this experiment generates multiple log files at different times)
	export LOG_PREFIX="$transmitter:$AFRN_ID:$serial_num:$frequency:$channel:$(date +%Y-%m-%d_%H_%M_%S)"

        # NOTE: this script sometimes takes ~5 seconds to finish
        ./Samples/startGNURadio-ChannelSounder-RX_v2.sh $serial_num $frequency $channel
	# Wait for receiver screens to start
	while ! ( screen -ls | grep -q rxGRC && screen -ls | grep -q power && screen -ls | grep -q quality ); do
	    sleep 0.2
	done

        # Sleep for 20 seconds to receive data
        sleep 20
        log_to_oeo "Stopping receiving"
        screen -S rxGRC -X quit
        screen -S power -X quit
        screen -S quality -X quit
        rm -f /root/Power /root/Quality
        pkill open5g*

	# Notify control script that this receiver is done
	curl --silent -X POST http://$C_VM_HOST:$C_VM_PORT/checkpoint/int/receivers_finished

    fi

done
