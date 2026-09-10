#!/bin/bash
sleep 3

# Run ifconfig and filter for the IPv4 address of oaitun_ue1
ipv4_address=$(ifconfig oaitun_ue1 | awk '/inet /{print $2}')

ping -i 0.2 -c 2000 "$ipv4_address" | ts '[%Y-%m-%d %H:%M:%.S]' | tee pingResultsUE.txt
