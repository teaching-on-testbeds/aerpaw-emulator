#!/bin/bash

cd $PROFILE_DIR"/ProfileScripts/Radio/Samples/LoRaWAN/TerminalLostik/"

# Name of the screen session
SESSION_NAME="terminal_lostik_loRaWAN"

# Path to your Python script
SCRIPT_PATH="terminalLostik.py"

# Create a new screen session and run the Python script
screen -dmS $SESSION_NAME bash -c "python3 $SCRIPT_PATH; exec bash"

# Check if the screen session was created successfully
if screen -list | grep -q "$SESSION_NAME"; then
  echo "Screen session '$SESSION_NAME' started successfully."
  echo "Use 'screen -r $SESSION_NAME' to reattach to the session."
else
  echo "Failed to start screen session '$SESSION_NAME'."
fi
