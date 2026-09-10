#!/bin/bash

cd "/root/Profiles/AADMChallenge/Coordinator"

VOLUME_FILE="uniform.txt"  # Path to your file

PYTHONUNBUFFERED=1 python3 Controller.py --file $VOLUME_FILE
# PYTHONUNBUFFERED=1 python3 Controller.py --volumes 100 200 300 234 


