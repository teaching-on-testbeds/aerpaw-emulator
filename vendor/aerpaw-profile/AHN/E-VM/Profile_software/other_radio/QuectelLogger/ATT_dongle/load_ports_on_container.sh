#!/bin/bash
Ports=$(ls /dev/ttyUSB* | pcregrep -o1 -i 'USB(\d+)')
Ports2=( "${Ports[@]/0}" )
echo $Ports2
for i in $Ports2
	do sudo docker exec E-VM-X0104-M1 mknod /dev/ttyUSB$i c 188 $i
done
