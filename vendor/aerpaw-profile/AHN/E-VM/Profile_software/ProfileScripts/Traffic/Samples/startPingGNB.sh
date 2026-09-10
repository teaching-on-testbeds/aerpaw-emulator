#!/bin/bash

ip route del 172.16.0.1 dev ogstun

ip route add 172.16.0.1 via 172.16.0.2 dev ogstun

ipv4_address=$(ifconfig ogstun | awk '/inet /{print $2}')

ping -i 0.2 -c 2000 "$ipv4_address" | ts '[%Y-%m-%d %H:%M:%.S]' | tee pingResultsUE.txt
