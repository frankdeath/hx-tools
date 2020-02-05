#!/usr/bin/env python3

import json

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
	return filename

def dumpJson(data):
	return json.dumps(data, indent=1, separators=(',', ' : '))

def dumpJsonSorted(data):
	return json.dumps(data, indent=1, separators=(',', ' : '), sort_keys=True)

def indicesToList(argString, func=int):
	# function to convert index arguments like '1-5,7,21,42-54' into a list of indices
	# func = function to convert from string to int
	result = []
	if (',' in argString) or ('-' in argString):
		for x in argString.split(','):
			if '-' in x:
				a, b = x.split('-')
				for y in range(func(a), func(b)+1):
					result.append(y)
			else:
				result.append(func(x))
	else:
		# There is only one element, return a list with one element
		result.append([func(x),])
	return result[:]

