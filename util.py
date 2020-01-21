#!/usr/bin/env python3

# Helper functions that don't need to be methods of a class

def littleEndianList(size, width):
	l = []
	for i in range(size):
		if width == 2:
			l.append("{:02d}".format(i)[::-1])
		if width == 3:
			l.append("{:03d}".format(i)[::-1])
	return(l[:])
	
def getBytes(byte_array, offset, size):
	return byte_array[offset:offset+size]

def getInt(byte_array, offset):
	# Return a 32-bit int
	return int.from_bytes(byte_array[offset:offset+4], byteorder='little', signed=False)
