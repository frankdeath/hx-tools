#!/usr/bin/env python3

import util
import section
import setlist

import os
import pprint

class Backup:
	'''
	Class the contents of an .hxb file
	'''
	def __init__(self, filename):
		# Only set the filename at init
		self.filename=filename
		self.extension=filename[-4:]
		self.filesize=None
		#
		self.footerOffset = None
		self.footerSize = None
		
		# Data useful to the Backup class
		self.data = None
		self.sections = []

		# Data useful to hx-tool.py
		self.IRs = []
		self.globalSettings = None
		self.setListNames = []
		self.setLists = []
		self.deviceInfo = None
		self.description = None
		
		self.exportDir = None

	def read(self, debug=False):
		# Read the file whole file, then close it
		with open(self.filename, "rb") as binary_file:
			self.data = binary_file.read()
			binary_file.close()
		self.filesize = len(self.data)
		
		if debug:
			print("filename = {}".format(self.filename))
			print("filesize = {}".format(self.filesize))

		if self.extension == '.hxb':
			self.analyzeHXB(debug)
		elif self.extension == '.hls':
			self.analyzeHLS(debug)
		else:
			print("Error: unknown file extension")
			
	def analyzeHLS(self, debug):
		# The data for the .hls was read as binary data so it can be parsed like the data from the .hxb file
		self.setLists.append(setlist.SetList(self.data))

	def analyzeHXB(self, debug):
		# Diagnostic (IR lables only exist if loaded, SL00 always exists, rest depend on use)
		# IR section labeling from b'000I' to b'F70I'

		# 
		self.footerOffset = util.getInt(self.data, util.footerOffsetLocation)
		self.footerSize = self.filesize - self.footerOffset
		if debug:
			print("footerOffset = {}".format(self.footerOffset))
			print("footerSize = {}".format(self.footerSize))
			#
			#!print((self.filesize - self.footerOffset)/util.footerSectionSize)
		
		#
		for footerSectionOffset in range(self.footerOffset, self.filesize, util.footerSectionSize):
			# Get the section
			s = section.Section(self.data, footerSectionOffset, util.footerSectionSize) 
			self.sections.append(s)

			#
			if debug:
				print("{} {}".format(s.name, s.footerValues))

			# If Section has an IR, append it to a list to simply code in hx-tool.py
			if s.ir != None:
				self.IRs.append(s.ir)
			elif s.setListName != None:
				self.setListNames.append(s.setListName)
			elif s.setList != None:
				self.setLists.append(s.setList)
			elif s.jsonGlobal != None:
				self.globalSettings = s.jsonGlobal
			elif s.deviceInfo != None:
				self.deviceInfo = s.deviceInfo
			elif s.description != None:
				self.description = s.description
			else:
				pass
				#print("{} {}".format(s.name, s.data))

	def makeExportDir(self):
		if self.extension == '.hxb' or self.extension == '.hls':
			self.exportDir = "{}-export".format(self.filename[:-4])
			if not os.path.isdir(self.exportDir):
				os.mkdir(self.exportDir)
			return True
		else:
			return False


	def printSummary(self):
		#
		self.deviceInfo.printInfo()
		print("Description: {}".format(self.description))
		for i in range(len(self.setLists)):
			print("Set List #{}: {}".format(i+1, self.setListNames[i]))
			self.setLists[i].printStats()
		print("IRs: {}".format(len(self.IRs)))

	def printGlobalSettings(self):
		# It isn't obvious if this info is useful or not
		pprint.pprint(self.globalSettings)
