#!/usr/bin/env python3

import util

class Section:
	'''
	Class the contents of one section of the footer
	'''
	def __init__(self, footerData):
		# Raw data from the footer
		self.footerData = footerData
		self.size = len(footerData)
		# Parsed data from the footer
		self.label = None
		self.labelSize = 4
		self.footerValues = []
		self.intSize = 4
		# 1st 32-bit (LE) int
		self.sectionOffset = None
		# 3rd 32-bit (LE) int
		self.compressedSize = None
		# 5th 32-bit (LE) int
		self.compressed = None
		# 6th 32-bit (LE) int
		self.deflatedSize = None
		#
		self.rawData = None
		self.data = None
		
	def analyzeFooter(self):
		#
		self.label = util.getBytes(self.footerData, 0, self.labelSize)
		
		#
		for i in range(int((self.size - self.labelSize)/self.intSize)):
			self.footerValues.append(util.getInt(self.footerData, self.labelSize + i * self.intSize))

		#
		self.sectionOffset = self.footerValues[0]
		self.compressedSize = self.footerValues[2]
		self.compressed = (self.footerValues[4] > 0)
		self.deflatedSize = self.footerValues[5]
