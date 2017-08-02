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
knownIDs = [b'E20040057307015424301ED2',
	b'E20040057307015824301ED4',
	b'E20040057307016224301EE2',
	b'E20040057307016624301EE4',
	b'E20040057307017024301EF2',
	b'E20040057307025124301F8B',
	b'E20040057307024724301F89',
	b'E20040057307024324301F7B',
	b'E20040057307023924301F79',
	b'E20040057307023524301F6B',
	b'E20040057307016624101EE8',
	b'E20040057307016224101EE6',
	b'E20040057307015824101ED8',
	b'E20040057307015424101ED6',
	b'E20040057307014924101EC0',
	b'E20040057307010124701AFA',
	b'E20040057307010524701AFC',
	b'E20040057307010924701B0A',
	b'E20040057307011424701B14',
	b'E20040057307011824701B22',
	b'E2005186010701930700CC1A',
	b'E2005186010701930690CC19',
	b'E2005186010701930670D113']

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
