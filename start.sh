#!/bin/sh

/usr/bin/pd -nogui /home/pi/afbook/afbook.pd 2>&1 &
sleep 1
/usr/bin/python3 /home/pi/afbook/findIDs.py > /home/pi/afbook/python.log 2>&1
