#!/usr/bin/env python3

# RFID reading code based on Python Wrapper for the Thingmagic Mercury API: https://github.com/gotthardp/python-mercuryapi
# This reads tags, if they're known, adds them to a list of current IDs. If it is new in there, it also send it to Pd over OSC.
# If tag hasn't been seen for X seconds, removes it from the list and lets Pd know it's gone(!)

# Mark IJzerman 2017
# Created during Residency at NABI Art Center, Seoul
# Supported by v2_ and Stimuleringsfonds

# ---------------------------------------------------------

# importing libraries
import time 
import mercury
import collections

# setting the connected reader
reader = mercury.Reader("tmr:///dev/ttyS0", baudrate=115200)
print(reader.get_model()) # print the model to see if it's working
reader.set_region("EU3") # set a region to work with
reader.set_read_plan([1], "GEN2", read_power=1900)


# this reads all of them in one go within the given time limit, and puts them in the CurID list
CurIDs = reader.read()

CurrrIDs = list(CurIDs)

set = set(CurIDs)
CurIDs_noduplicates = list(set)
print (CurIDs_noduplicates)


def makeUnique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]



# Below should be the IDs of the RFID tags!
knownIDs = [b'E2000015860E01451120AB56',
        b'48656C6C6F2101591120AB75',
        b'E2000015860E01601120AB6E',
        b'E2000015860E01611120AB76']


def checkIfIDexists():
	# this looks at if the given ID is in the list IDs!
	index = dict((y,x) for x,y in enumerate(knownIDs))
	try:
	# it should enter the page ID into index from the RFID reader!
   		IDfound_index = index[ID]
	except KeyError:
   		print ("ID is not found in knownIDs")
	else:
	    print ("ID is found in knownIDs")
	    print ("The ID that is found is", IDfound_index)
	    
	    # Put it in the CurIDs list if it isn't there yet
	    if not IDfound_index in CurIDs:
	      CurIDs.append(IDfound_index)
	      print("Current IDs is added to CurIDs. Now consists of:", CurIDs)
	    else:
	      print("Current ID is already in CurIDs")