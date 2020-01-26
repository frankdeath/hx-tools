#!/usr/bin/env python3

import util
import footerSection
import section

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
			self.footerSections.append(f)

			# Get the section
			s = section.Section(util.getBytes(self.data, f.sectionOffset, f.compressedSize), f)
			self.sections.append(s)

			#
			if debug:
				print("{} {}".format(s.name, s.footerSection.footerValues))

			# If Section has an IR, append it to a list to simply code in hx-tool.py
			if s.ir != None:
				self.IRs.append(s.ir)
			if s.json != None:
				#pass
				s.jsonPrint()
			else:
				pass
				#print("{} {}".format(s.name, s.data))
