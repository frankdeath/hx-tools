#!/usr/bin/env python3

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
		
	def read(self):
		# Read the file whole file, then close it
		with open(self.filename, "rb") as binary_file:
			self.data = binary_file.read()
			binary_file.close()
		self.filesize = len(self.data)
		
		print("filename = {}".format(self.filename))
		print("filesize = {}".format(self.filesize))
		
		# Diagnostic (IR lables only exist if loaded, SL00 always exists, rest depend on use)
		# IR section labeling from b'000I' to b'F70I'

		# 
		self.footerOffset = util.getInt(self.data, self.footerOffsetLocation)
		self.footerSize = self.filesize - self.footerOffset
		print("footerOffset = {}".format(self.footerOffset))
		print("footerSize = {}".format(self.footerSize))

		#
		#!print((self.filesize - self.footerOffset)/self.footerSectionSize)
		
		#
		for i in range(int((self.filesize - self.footerOffset)/self.footerSectionSize)):
			self.footerSections.append(footerSection.FooterSection(util.getBytes(self.data, (self.footerOffset + i * self.footerSectionSize), self.footerSectionSize)))
			
		for s in self.footerSections:
			#!print(s.data)
			s.analyzeFooter()
			#!print("{} {}".format(s.label, s.footerValues))

			#
			self.sections.append(section.Section(util.getBytes(self.data, s.sectionOffset, s.compressedSize), s))
		for s in self.sections:
			s.decompress()
			if s.footerSection.compressedSize != s.rawDataSize:
				print("{}  {}!={}".format(s.footerSection.label, s.footerSection.compressedSize, s.rawDataSize))
			if s.footerSection.deflatedSize != s.dataSize:
				print("{}  {}!={}".format(s.footerSection.label, s.footerSection.deflatedSize, s.dataSize))

			print("{} {}".format(s.name, s.footerSection.footerValues))
			# If Section is an IR section
			if s.name[2:] == b'0I':
				i = ir.ImpulseResponse(s.data)
				i.analyze()
			#print(s.name)
