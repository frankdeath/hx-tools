#!/usr/bin/env python3

import util
import preset

import json
import base64
import zlib
import pprint

class SetList:
	'''
	Class representing the contents of the ##LS section
	'''
	def __init__(self, data, sectionName=None):
		# rawData is the raw bytes of the section
		self.rawData = data
		self.rawDataSize = len(data)
		self.sectionName = sectionName
		#
		self.jsonData = None
		self.compressedData = None
		self.decompressedData = None
		self.data = None
		self.dataMeta = None
		self.dataPresets = None
		self.meta = None
		self.schema = None
		self.version = None
		self.presets = []

		self.analyze()

		#!print(util.dumpJson(self.jsonData))

	def analyze(self):
		#
		self.jsonData = json.loads(self.rawData.decode('utf-8'))
		#!print(self.jsonData)
		if 'encoded_data' in self.jsonData:
			if self.jsonData['encoding'] == "Base64":
				self.compressedData = base64.b64decode(self.jsonData['encoded_data'])
			if 'compression' in self.jsonData:
				self.decompressedData = zlib.decompress(self.compressedData)
				#!print(self.decompressedData)
			if zlib.crc32(self.decompressedData) == self.jsonData['compression']['crc32']:
				print("Checksum is OK")
				if len(self.decompressedData) == self.jsonData['compression']['decompressed_size']:
					print("Filesize is OK")
					#!print(type(self.decompressedData))
					self.jsonData['data'] = json.loads(self.decompressedData.decode('utf-8'))
		
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

	def export(self, exportDir):
		# Export each preset individually
		for p in self.presets:
			p.export(exportDir)
