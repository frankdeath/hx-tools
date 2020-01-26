#!/usr/bin/env python3

import zlib
import json
import pprint
import util
import ir

class Section:
	'''
	Class the contents of one section of the footer
	'''
	def __init__(self, data, footerSection):
		# data from the footer
		self.footerSection = footerSection
		self.name = self.footerSection.label
		self.rawData = data
		self.rawDataSize = len(data)
		self.data = None
		self.dataSize = None
		self.ir = None
		self.json = None
		
		self.decompress()
		
		self.analyze()

	def decompress(self):
		if self.footerSection.compressed == False:
			# No decompression needed
			self.data = self.rawData
			self.dataSize = self.rawDataSize
		else:
			# Decompress the data
			self.data = zlib.decompress(self.rawData)
			self.dataSize = len(self.data)
		
		# Error check
		if self.footerSection.compressedSize != self.rawDataSize:
			print("Error: Section {}: compressed size discrepancy: {}!={}".format(self.footerSection.label, self.footerSection.compressedSize, self.rawDataSize))
		if self.footerSection.deflatedSize != self.dataSize:
			print("Error: Section {}: decompressed size discrepancy: {}!={}".format(self.footerSection.label, self.footerSection.deflatedSize, self.dataSize))

	def analyze(self):
		# If Section is an IR section
		if self.name[2:] == b'0I':
			self.ir = ir.ImpulseResponse(self.data, self.name)
		if self.name == b'BOLG':
			self.json = json.loads(self.data.decode('utf-8'))
		else:
			pass
			#print("{} {}".format(self.name, self.data))

	def jsonPrint(self):
		pprint.pprint(self.json)
