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
from more_itertools import unique_everseen
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
reader = mercury.Reader("tmr:///dev/serial0", baudrate=115200)
print(reader.get_model()) # print the model to see if it's working
reader.set_region("EU3") # set a region to work with
reader.set_read_plan([1], "GEN2", read_power=1400)

# Below should be the IDs of the RFID tags! Their location is the page numbers
knownIDs = [b'E20040057307022824101F67',
	b'E20040057307021024301F42',
	b'E20040057307022024101F57',
	b'E20040057307020224301F32',
	b'E20040057307021124101F3F',
	b'E20040057307019824301F24',
	b'E20040057307024924101F8E',
	b'E20040057307019424301F22',
	b'E2004005730701842530152F',
	b'E2004005730701882530153D',
	b'E2004005730701922530153F',
	b'E2004005730700762530145D',
	b'E2004005730700802530145F',
	b'E2004005730700842530146D',
	b'E2004005730700882530146F',
	b'E2004005730700922530147D',
	b'E20040057307021825301570',
	b'E2004005730702222530157E',
	b'E20040057307022625301580',
	b'E20040057307023425301590',
	b'E2004005730702302530158E',
	b'E20040057307024524101F80',
	b'E20040057307023724101F70',
	b'E20040057307024124101F7E'
	]

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
		pagePresent = knownIDs.index(curIDs[x]) + 1
		curPages.append(pagePresent)
		curPages.sort(key=int)
	
	# Take out the duplicates using unique_everseen, and print it.
	curPages = list(unique_everseen(curPages))
	print (curPages)
	client.send_message("/pages", curPages)

readTags()
