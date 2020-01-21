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
		# Constants
		self.footerOffsetLocation = 0x8
		self.footerOffset = None
		self.fixedLabels = [b'IDXH', b'CSED', b'MNLS', b'BOLG']
		self.irLabels = [bytes(x+'I', encoding='ascii') for x in util.littleEndianList(128, 3)]
		self.slLabels = [bytes(x+'LS', encoding='ascii') for x in util.littleEndianList(8, 2)]
		#!print(self.irLabels)
		#!print(self.slLabels)
		self.sectionLabels = self.fixedLabels + self.irLabels + self.slLabels
		self.sectionSize = 36
		
		#
		self.raw_data=None
		self.byte_array=None
		self.sections=[]
		
	def read(self):
		# Read the file whole file, then close it
		with open(self.filename, "rb") as binary_file:
			self.data = binary_file.read()
			binary_file.close()
		self.filesize = len(self.data)
		
		print("filename = {}".format(self.filename))
		print("filesize = {}".format(self.filesize))
		
		# Convert the data to a byte array
		self.byte_array = bytearray(self.data) 

		# Diagnostic (IR lables only exist if loaded, SL00 always exists, rest depend on use)
		for label in self.sectionLabels:
			if label in self.byte_array:
				print("{} = {}".format(label, label in self.byte_array))

		# 
		self.footerOffset = util.getInt(self.byte_array, self.footerOffsetLocation)
		print("footerOffset = {}".format(self.footerOffset))

		#
		#!print((self.filesize - self.footerOffset)/self.sectionSize)
		
		#
		for i in range(int((self.filesize - self.footerOffset)/self.sectionSize)):
			self.sections.append(section.Section(util.getBytes(self.byte_array, (self.footerOffset + i * self.sectionSize), self.sectionSize)))
			
		for s in self.sections:
			#!print(s.data)
			s.analyze()
			print("{} {}".format(s.label, s.values))
