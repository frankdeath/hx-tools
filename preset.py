#!/usr/bin/env python3

import util

import json

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

	def createFileName(self):
		return util.replaceChars("{}-{}.hlx".format(self.indexStr, self.name))

	def export(self, exportDir):
		filename = "{}/{}".format(exportDir, self.createFileName())
		if self.name != None:
			print("Exporting {}".format(filename))
			f = open(filename, "w")
			# NOTE: self.data is a subset of the data that is exported from HX Edit
			f.write(util.dumpJson({"data": self.data, "meta" : {"original":0, "pbn":0, "premium":0}, "schema":"L6Preset", "version":6}))
			f.close()
