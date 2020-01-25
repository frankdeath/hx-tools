#!/usr/bin/env python3

# Helper functions that don't need to be methods of a class
	
def getBytes(data, offset, size):
	return data[offset:offset+size]

def getInt(data, offset):
	# Return a 32-bit int
	return int.from_bytes(data[offset:offset+4], byteorder='little', signed=False)
