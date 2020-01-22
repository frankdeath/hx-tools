#!/usr/bin/env python3

import util
import zlib

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

	def decompress(self):
		if self.footerSection.compressed == False:
			# No decompression needed
			self.data = self.rawData
			self.dataSize = self.rawDataSize
		else:
			# Decompress the data
			self.data = zlib.decompress(self.rawData)
			self.dataSize = len(self.data)

	def analyze(self):
		#
		pass
