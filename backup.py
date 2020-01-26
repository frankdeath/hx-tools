#!/usr/bin/env python3

import json
import pprint
import util
import footerSection
import section
import ir

class Backup:
	'''
	Class the contents of an .hxb file
	'''
	def __init__(self, filename):
		# Only set the filename at init
		self.filename=filename
		self.filesize=None
		# Constants
		self.footerOffsetLocation = 0x8
		self.footerOffset = None
		self.footerSize = None
		self.fixedLabels = [b'IDXH', b'CSED', b'MNLS', b'BOLG']
		self.footerSectionSize = 36
		
		#
		self.data = None
		self.footerSections = []
		self.sections = []
		self.IRs = []
		
	def read(self, debug=False):
		# Read the file whole file, then close it
		with open(self.filename, "rb") as binary_file:
			self.data = binary_file.read()
			binary_file.close()
		self.filesize = len(self.data)
		
		if debug:
			print("filename = {}".format(self.filename))
			print("filesize = {}".format(self.filesize))
		
		# Diagnostic (IR lables only exist if loaded, SL00 always exists, rest depend on use)
		# IR section labeling from b'000I' to b'F70I'

		# 
		self.footerOffset = util.getInt(self.data, self.footerOffsetLocation)
		self.footerSize = self.filesize - self.footerOffset
		if debug:
			print("footerOffset = {}".format(self.footerOffset))
			print("footerSize = {}".format(self.footerSize))
			#
			#!print((self.filesize - self.footerOffset)/self.footerSectionSize)
		
		#
		for i in range(int((self.filesize - self.footerOffset)/self.footerSectionSize)):
			# Get the footer section
			f = footerSection.FooterSection(util.getBytes(self.data, (self.footerOffset + i * self.footerSectionSize), self.footerSectionSize))
			f.analyzeFooter()
			self.footerSections.append(f)

			# Get the section
			s = section.Section(util.getBytes(self.data, f.sectionOffset, f.compressedSize), f)

			#
			s.decompress()
			if s.footerSection.compressedSize != s.rawDataSize:
				print("Error: Section {}: compressed size discrepancy: {}!={}".format(s.footerSection.label, s.footerSection.compressedSize, s.rawDataSize))
			if s.footerSection.deflatedSize != s.dataSize:
				print("Error: Section {}: decompressed size discrepancy: {}!={}".format(s.footerSection.label, s.footerSection.deflatedSize, s.dataSize))

			self.sections.append(s)

			#
			if debug:
				print("{} {}".format(s.name, s.footerSection.footerValues))

			# If Section is an IR section
			if s.name[2:] == b'0I':
				i = ir.ImpulseResponse(s.data, s.name)
				i.analyze()
				self.IRs.append(i)
			if s.name == b'BOLG':
				sdata = s.data.decode('utf-8')
				jdata = json.loads(sdata)
				pprint.pprint(jdata)
			else:
				pass
				#print("{} {}".format(s.name, s.data))
