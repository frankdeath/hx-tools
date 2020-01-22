#!/usr/bin/env python3

import util

class ImpulseResponse:
	'''
	Class representing the contents of one IR section
	'''
	def __init__(self, data):
		self.data = data
		self.dataSize = len(data)
		self.name = None

	def analyze(self):
		# 
		self.riff = util.getBytes(self.data, 0, 4)
		self.riffSize = util.getInt(self.data, 4)
		self.wave = util.getBytes(self.data, 8, 4)
		self.fmtChunk = util.getBytes(self.data, 12, 4)
		self.fmtChunkSize = util.getInt(self.data, 16)
		self.dataChunk = util.getBytes(self.data, 20+self.fmtChunkSize, 4)
		self.dataChunkSize = util.getInt(self.data, 20+self.fmtChunkSize+4)
		self.headerSize = 20+self.fmtChunkSize+4+4
		self.extraOffset = self.headerSize + self.dataChunkSize
		self.extraSize = self.dataSize - self.extraOffset
		self.list = util.getBytes(self.data, self.extraOffset, 4)
		self.listSize = util.getInt(self.data, self.extraOffset+4) 
		self.info = util.getBytes(self.data, self.extraOffset+8, 4)
		self.inam = util.getBytes(self.data, self.extraOffset+12, 4)
		self.inamSize = util.getInt(self.data, self.extraOffset+16)
		self.name = util.getBytes(self.data, self.extraOffset+20, self.inamSize)

		#!print(self.riff)
		#!print(self.riffSize)
		#!print(self.wave)
		#!print(self.fmtChunk)
		#!print(self.fmtChunkSize)
		#!print(self.dataChunk)
		#!print(self.dataChunkSize)
		#!print(self.headerSize)
		#!print(self.extraOffset)
		#!print(self.extraSize)
		#!print(self.list)
		#!print(self.listSize)
		#!print(self.info)
		#!print(self.inam)
		#!print(self.inamSize)
		print("\t", self.name)
		#!print()
