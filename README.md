# Audiophotobook project
## Mark IJzerman, summer 2017
#### created during residency at Art center Nabi, Seoul: www.nabi.or.kr
#### as part of V2_'s Summer Sessions program: http://www.summersessions.net
#### Supported by V2_ and Stimuleringsfonds

### What is it?
This repository contains all the files I'm working for to create an audiophotobook. That means a photo book with RFID-tags embedded in the pages. These are read by a "Simultaneous RFID Tag Reader" (https://www.sparkfun.com/products/14066, quite expensive but useful for this application!) which is embedded in the book's lasercut cover. This information is then sent over a serial connection to a Raspberry Pi Zero, which is read in in a python script, using gotthardp's python-mercury Python wrapper for the ThingMagic Mercury API: https://github.com/gotthardp/python-mercuryapi
This information is in turn sent to PureData using an OSC connection. Pd generates sound which is output using Pimoroni's pHat DAC: https://shop.pimoroni.com/products/phat-dac

This keeps everything nice & small so it can easily be embedded in the book.

### Why?
This is a starting point to experiment with new ways of telling stories and an exploration into creating very small/thin embedded audio applications.

### Notes
- The mijstartup.service must go in the systemd directory and be initiated as follows: http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/ (from Step 3 on)
- In the "notes" folder there are logs I keep on setting up the Pi, what I run in to with the lasercutter, et cetera.
- The pHAT DAC can easily be swapped out for some speaker HATs, such as this nifty Speaker Bonnet: https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/overview
