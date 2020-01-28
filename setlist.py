#!/usr/bin/env python3

import util
import preset

import json
import pprint

class SetList:
	'''
	Class representing the contents of the ##LS section
	'''
	def __init__(self, data, sectionName):
		# rawData is the raw bytes of the section
		self.rawData = data
		self.rawDataSize = len(data)
		self.sectionName = sectionName
		#
		self.jsonData = None
		self.data = None
		self.dataMeta = None
		self.dataPresets = None
		self.meta = None
		self.schema = None
		self.version = None
		self.presets = []

		self.analyze()

		#!pprint.pprint(self.jsonData)

	def analyze(self):
		#
		self.jsonData = json.loads(self.rawData.decode('utf-8'))
		
		#
		self.data = self.jsonData['data']
		self.meta = self.jsonData['meta']
		self.schema = self.jsonData['schema']
		self.version = self.jsonData['version']

		self.dataMeta = self.data['meta']
		self.dataPresets = self.data['presets']
		
		for i in range(len(self.dataPresets)):
			self.presets.append(preset.Preset(self.dataPresets[i], i, self.sectionName))

	def printInfo(self):
		#print("")
		for p in self.presets:
			p.printInfo()
