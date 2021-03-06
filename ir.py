#!/usr/bin/env python3

import util

class ImpulseResponse:
	'''
	Class representing the contents of one IR section
	'''
	def __init__(self, data, sectionName):
		self.data = data
		self.dataSize = len(data)
		self.sectionName = sectionName
		self.irSlot = self.sectionNameToIRSlot(sectionName)
		self.name = None
		self.nameStr = None
		
		self.analyze()

	def sectionNameToIRSlot(self, sectionName):
		hexStr = sectionName[:2][::-1].decode('utf-8')
		return int(hexStr, 16)+1

	def analyze(self):
		# "RIFF"
		#!self.riffTag = util.getBytes(self.data, 0, 4)
		# riffSize = dataSize - 8
		#!self.riffSize = util.getInt(self.data, 4)
		# "WAVE"
		#!self.waveTag = util.getBytes(self.data, 8, 4)
		# "fmt "
		#!self.fmtChunk = util.getBytes(self.data, 12, 4)
		# size of the format section
		self.fmtChunkSize = util.getInt(self.data, 16)
		# "data"
		#!self.dataChunk = util.getBytes(self.data, 20+self.fmtChunkSize, 4)
		# size of the data section
		self.dataChunkSize = util.getInt(self.data, 24+self.fmtChunkSize)
		# "LIST"
		#!self.listTag = util.getBytes(self.data, 28+self.fmtChunkSize+self.dataChunkSize, 4)
		# size of list section (includes iname)
		#!self.listSize = util.getInt(self.data, 32+self.fmtChunkSize+self.dataChunkSize) 
		# "INFO"
		#!self.infoTag = util.getBytes(self.data, 36+self.fmtChunkSize+self.dataChunkSize, 4)
		# "INAM"
		#!self.inamTag = util.getBytes(self.data, 40+self.fmtChunkSize+self.dataChunkSize, 4)
		# size of iname section
		self.inamSize = util.getInt(self.data, 44+self.fmtChunkSize+self.dataChunkSize)
		# Name of impulse response
		self.name = util.getBytes(self.data, 48+self.fmtChunkSize+self.dataChunkSize, self.inamSize)
		# Remove the trailing null byte when converting to a string
		self.nameStr = self.name.decode('utf-8')[:-1]

		#!self.info()

	def info(self):
		#!print(self.dataSize)
		#!print(self.riffTag)
		#!print(self.riffSize)
		#!print(self.waveTag)
		#!print(self.fmtChunk)
		#!print(self.fmtChunkSize)
		#!print(self.dataChunk)
		#!print(self.dataChunkSize)
		#1print(self.listTag)
		#!print(self.listSize)
		#1print(self.infoTag)
		#!print(self.inamTag)
		#!print(self.inamSize)
		#!print("\t", self.name)
		#!print()
		#!print("{:3d} {} {}".format(self.irSlot, self.sectionName, self.name))
		print(" {:3d} = {}".format(self.irSlot, self.nameStr))

	def createFileName(self):
		return util.replaceChars("{:03d}-{}.wav".format(self.irSlot, self.nameStr))

	def export(self, exportDir):
		filename = "{}/{}".format(exportDir, self.createFileName())
		print("Exporting {}".format(filename))
		f = open(filename, "wb")
		# NOTE: the data that is exported is identical to data that is exported from HX Edit
		f.write(self.data)
		f.close()
