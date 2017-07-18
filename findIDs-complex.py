#!/usr/bin/env python3

# RFID reading code based on Python Wrapper for the Thingmagic Mercury API: https://github.com/gotthardp/python-mercuryapi
# This reads tags, if they're known, adds them to a list of current IDs. If it is new in there, it also send it to Pd over OSC.
# If tag hasn't been seen for X seconds, removes it from the list and lets Pd know it's gone(!)

# Mark IJzerman 2017
# Created during Residency at NABI Art Center, Seoul
# Supported by v2_ and Stimuleringsfonds

# ---------------------------------------------------------

# importing libraries
import threading
import time 
import mercury
import collections
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

# set up OSC stuff
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5005,
      help="The port the OSC server is listening on")
  args = parser.parse_args()
  client = udp_client.SimpleUDPClient(args.ip, args.port)

# set-up for the connected reader
reader = mercury.Reader("tmr:///dev/ttyS0", baudrate=115200)
print(reader.get_model()) # print the model to see if it's working
reader.set_region("EU3") # set a region to work with
reader.set_read_plan([1], "GEN2", read_power=1900)

# Below should be the IDs of the RFID tags! Their location is the page numbers
knownIDs = [b'E2000015860E01451120AB56',
        b'48656C6C6F2101591120AB75',
        b'E2000015860E01601120AB6E',
        b'E2000015860E01611120AB76']

def readTags():
	threading.Timer(0.15, readTags).start()
	# this reads all of them in one go within the given time limit, and puts them in the CurIDs list
	incomingIDs = reader.read(timeout=100)
	# print ("length of list is", len(incomingIDs))
	
	# make list out of all the tags epc item. CurIDs is flat list
	curIDs = []
	curPages = []

	for x in range(0, len(incomingIDs)):
		curIDs.append(incomingIDs[x].epc)

	# comparing lists, output the location of the found IDs within knownIDs
	for x in range(0, len(curIDs)):
		pagePresent = knownIDs.index(curIDs[x])
		curPages.append(pagePresent)
		curPages.sort(key=int)
	
	print (curPages)
	client.send_message("/pages", curPages)

readTags()
