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
		self.name = None
		self.schema = None
		self.version = None
		self.presets = []
		self.numNewPreset = 0
		self.numEmpty = 0

		self.analyze()

		#!print(util.dumpJson(self.jsonData))

	def analyze(self):
		#
		self.jsonData = json.loads(self.rawData.decode('utf-8'))
		#!print(self.jsonData)
		
		# .hls files contain encoded data
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

		self.name = self.meta['name']

		self.dataMeta = self.data['meta']
		self.dataPresets = self.data['presets']
		
		for i in range(len(self.dataPresets)):
			p = preset.Preset(self.dataPresets[i], i, self.sectionName)
			self.presets.append(p)
			if p.name == None:
				self.numEmpty += 1
			if p.name == "New Preset":
				self.numNewPreset += 1

	def printStats(self):
		print("  Used:      {:3d}/{}".format(len(self.presets)-self.numEmpty, len(self.presets)))
		print("  Available: {:3d}/{}".format(self.numEmpty, len(self.presets)))

	def printPreset(self, index):
		# index starts at 0
		self.presets[index].printInfo()

	def printInfo(self):
		#print("")
		for p in self.presets:
			p.printInfo()

	def createFilename(self):
		return util.replaceChars("{}.hls".format(self.name))

	def exportHLS(self, exportDir):
		### Export the set list as a .hls file

		# start with all the data from the set list section of the .hxb file
		hlsData = self.jsonData
		
		# Calculate values for 'compression' dictionary
		data = util.dumpJson(hlsData['data']).encode('utf-8')
		# sorting the keys has no effect on the output
		#!data = util.dumpJsonSorted(hlsData['data']).encode('utf-8')
		size = len(data)
		crc32 = zlib.crc32(data)
		# Add the 'compression' dictionary
		hlsData["compression"] = {"crc32":crc32, "decompressed_size":size, "type":"zlib"}
		
		# Compress the data
		c_data = zlib.compress(data)
		# Encode the data
		e_data = base64.b64encode(c_data)
		# Add the encoded data
		hlsData["encoded_data"] = e_data.decode('utf-8')
		hlsData["encoding"] = "Base64"
		
		# Remove the unencoded data from the dictionary
		del hlsData['data']
		
		filename = "{}/{}".format(exportDir, self.createFilename())

		print("Exporting {}".format(filename))
		f = open(filename, "w")
		f.write(util.dumpJsonSorted(hlsData))
		f.close()

	def exportPreset(self, index, exportDir):
		# index starts at 0
		self.presets[index].export(exportDir)

	def exportAllPresets(self, exportDir):
		# Export each preset individually
		for p in self.presets:
			p.export(exportDir)
