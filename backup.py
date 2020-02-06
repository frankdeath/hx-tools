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

	def isFullBackup(self):
		return (self.extension == '.hxb')

	def makeExportDir(self):
		if self.extension == '.hxb' or self.extension == '.hls':
			self.exportDir = "{}-export".format(self.filename[:-4])
			if not os.path.isdir(self.exportDir):
				os.mkdir(self.exportDir)
			return True
		else:
			return False

	def getExportPath(self, subDir):
		dirName = "{}/{}".format(self.exportDir, subDir)
		if not os.path.isdir(dirName):
			os.mkdir(dirName)
		return dirName

	def exportIR(self, index, subDir="IRs"):
		# index is a int numbered from 1
		dirName = self.getExportPath(subDir)
		self.IRs[index-1].export(dirName)

	def exportIRs(self, iList, subDir="IRs"):
		# iList is a list of indices numbered from 1
		dirName = self.getExportPath(subDir)
		for i in iList:
			self.IRs[i-1].export(dirName)

	def exportAllIRs(self, subDir="IRs"):
		dirName = self.getExportPath(subDir)
		for i in self.IRs:
			# i is an ImpulseResponse object
			i.export(dirName)

	def exportSetList(self, index):
		self.setLists[index-1].exportHLS(self.exportDir)

	def exportSetLists(self, iList):
		for i in iList:
			self.setLists[i-1].exportHLS(self.exportDir)

	def exportAllSetLists(self):
		for sl in self.setLists:
			sl.exportHLS(self.exportDir)

	def exportPreset(self, slIndex, pIndex, subDirPrefix="SetList"):
		dirName = self.getExportPath("{}{}".format(subDirPrefix, slIndex))
		self.setLists[slIndex-1].exportPreset(pIndex-1, dirName)

	def exportPresets(self, slIndex, pList, subDirPrefix="SetList"):
		dirName = self.getExportPath("{}{}".format(subDirPrefix, slIndex))
		for i in pList:
			self.setLists[slIndex-1].exportPreset(i-1, dirName)

	def exportAllPresets(self, subDirPrefix="SetList"):
		# should this export all set lists or just one set list?
		for i in range(len(self.setLists)):
			# i is numbered from 0
			dirName = self.getExportPath("{}{}".format(subDirPrefix, i))
			self.setLists[i].exportAllPresets(dirName)

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

	def printIR(self, index):
		# index is an int numbered from 1
		self.IRs[index-1].info()

	def printIRs(self, iList, subDir="IRs"):
		# iList is a list of indices numbered from 1
		for i in iList:
			self.IRs[i-1].info()

	def printAllIRs(self):
		for i in self.IRs:
			i.info()

	def printSetList(self, index):
		self.setLists[index-1].printInfo()

	def printSetLists(self, iList):
		for i in iList:
			self.setLists[i-1].printInfo()

	def printAllSetLists(self):
		for sl in self.setLists:
			sl.printInfo()

	def printPreset(self, slIndex, pIndex):
		self.setLists[slIndex].printPreset(pIndex-1)

	def printPresets(self, slIndex, pList):
		for i in pList:
			self.setLists[slIndex-1].printPreset(i-1)

	def printAllPresets(self):
		self.printAllSetLists()
