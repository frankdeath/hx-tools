#!/usr/bin/env python3

import util

class Section:
	'''
	Class the contents of one section of the footer
	'''
	def __init__(self, data):
		self.data = data
		self.size = len(data)
		#
		self.label = None
		self.labelSize = 4
		self.values = []
		self.intSize = 4
		# 1st 32-bit (LE) int
		self.offset = None
		# 2nd 32-bit (LE) int
		self.two = None
		# 3rd 32-bit (LE) int
		self.compressedSize = None
		# 4th 32-bit (LE) int
		self.four = None
		# 5th 32-bit (LE) int
		self.deflated = None
		# 6th 32-bit (LE) int
		self.deflatedSize = None
		# 7th 32-bit (LE) int
		self.seven = None
		# 8th 32-bit (LE) int
		self.eight = None
		
	def analyze(self):
		#
		self.label = util.getBytes(self.data, 0, self.labelSize)
		
		#
		for i in range(int((self.size - self.labelSize)/self.intSize)):
			self.values.append(util.getInt(self.data, self.labelSize + i * self.intSize))

		#!print(self.values)
