#!/usr/bin/env python3

import util

class Preset:
	'''
	Class representing the contents of one preset from the ##LS section
	'''
	def __init__(self, data, index, sectionName):
		self.data = data
		self.index = index
		self.sectionName = sectionName

		self.indexStr = self.indexToStr()

		if self.data != {}:
			self.name = self.data['meta']['name']
		else:
			self.name = None

	def indexToStr(self):
		return "{}{}".format(int(self.index/3)+1, "ABC"[self.index%3])

	def printInfo(self):
		print(" {:3s} {}".format(self.indexStr, self.name))
