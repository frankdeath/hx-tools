#!/usr/bin/env python3

# Constants

footerOffsetLocation = 0x8
footerSectionSize = 36
sectionNameSize = 4
intSize = 4

# Helper functions that don't need to be methods of a class

def getBytes(data, offset, size):
	return data[offset:offset+size]

def getInt(data, offset, size=intSize):
	# Return a 32-bit int
	return int.from_bytes(data[offset:offset+size], byteorder='little', signed=False)

def replaceChars(filename):
	#
	filename = filename.replace(':', '-')
	filename = filename.replace(' ', '_')
	filename = filename.replace('/', '_')
	filename = filename.replace('\'', '')
	filename = filename.replace('+', '-')
	filename = filename.replace('?', '')
	filename = filename.replace('$', 'Money')
	print([ord(x) for x in ('/', ':', "'", '\'', ' ')])
	return filename
