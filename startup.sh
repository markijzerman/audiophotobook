#!/bin/bash

# This startup script will launch the python script & Pd with the right parameters. It is called with systemd.
# More information here: http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/
# Mark IJzerman, 2017

pd -nogui home/pi/afbook/afbook.pd &
python3 home/pi/afbook/findIDs.py
