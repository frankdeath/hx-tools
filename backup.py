#!/usr/bin/env python3

import util
import section

class Backup:
	'''
	Class the contents of an .hxb file
	'''
	def __init__(self, filename):
		# Only set the filename at init
		self.filename=filename
		self.filesize=None
		#
		self.footerOffset = None
		self.footerSize = None
		self.fixedLabels = [b'IDXH', b'CSED', b'MNLS', b'BOLG']
		
		#
		self.data = None
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
			if s.json != None:
				pass
				#s.jsonPrint()
			else:
				pass
				#print("{} {}".format(s.name, s.data))
