#!/usr/bin/env python3

import util
import info
import ir
import setlist

import zlib
import json
import pprint

class Section:
	'''
	Class the contents of one section of the footer
	'''
	def __init__(self, data, footerSectionOffset, footerSectionSize):
		## raw data from the footer
		self.footer = util.getBytes(data, footerSectionOffset, footerSectionSize)
		self.footerSize = len(self.footer)
		self.footerOffset = footerSectionOffset
		## parsed data from the footer
		self.name = None
		self.footerValues = []
		# 1st 32-bit (LE) int
		self.sectionOffset = None
		# 3rd 32-bit (LE) int
		self.compressedSize = None
		# 5th 32-bit (LE) int
		self.compressed = None
		# 6th 32-bit (LE) int
		self.uncompressedSize = None
		
		self.analyzeFooter()

		## raw data from the section
		self.rawData = util.getBytes(data, self.sectionOffset, self.compressedSize)
		self.rawDataSize = len(self.rawData)
		## parsed data from the section
		self.data = None
		self.dataSize = None
		#
		self.ir = None
		self.jsonGlobal = None
		self.deviceInfo = None
		self.description = None
		self.setList = None
		self.setListName = None
		
		self.decompress()
		
		self.analyze()


	def analyzeFooter(self):
		#
		self.name = util.getBytes(self.footer, 0, util.sectionNameSize)
		
		#
		for i in range(util.sectionNameSize, self.footerSize, util.intSize):
			self.footerValues.append(util.getInt(self.footer, i))

		#
		self.sectionOffset = self.footerValues[0]
		self.compressedSize = self.footerValues[2]
		self.compressed = (self.footerValues[4] > 0)
		self.uncompressedSize = self.footerValues[5]


	def decompress(self):
		if self.compressed == False:
			# No decompression needed
			self.data = self.rawData
			self.dataSize = self.rawDataSize
		else:
			# Decompress the data
			self.data = zlib.decompress(self.rawData)
			self.dataSize = len(self.data)
		
		# Error check
		if self.compressedSize != self.rawDataSize:
			print("Error: Section {}: compressed size discrepancy: {}!={}".format(self.footerSection.label, self.footerSection.compressedSize, self.rawDataSize))
		if self.uncompressedSize != self.dataSize:
			print("Error: Section {}: decompressed size discrepancy: {}!={}".format(self.footerSection.label, self.footerSection.deflatedSize, self.dataSize))


	def analyze(self):
		if self.name[2:] == b'0I':
			# IR section
			self.ir = ir.ImpulseResponse(self.data, self.name)
		elif self.name == b'BOLG':
			# Global section
			self.jsonGlobal = json.loads(self.data.decode('utf-8'))
		elif self.name[1:] == b'0LS':
			# Set List section
			self.setList = setlist.SetList(self.data, self.name)
		elif self.name == b'IDXH':
			self.deviceInfo = info.DeviceInfo(self.data, self.name)
		elif self.name == b'CSED':
			# Backup file description
			self.description = self.data.decode('utf-8')
		elif self.name == b'MNLS':
			# Set List names
			# Note: this is probably more interesting on the Helix devices than on the HX Stomp
			self.setListName = self.data.decode('utf-8')
		else:
			pass
			#print("{} {}".format(self.name, self.data))
			#print(len(self.data))
			#for i in range(0, len(self.data), util.intSize):
			#	print(i, util.getInt(self.data, i))

	def jsonPrint(self, data):
		pprint.pprint(data)
