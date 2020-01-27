#!/usr/bin/env python3

import util

import time

class DeviceInfo:
	'''
	Class representing the contents of the IDXH section
	'''
	def __init__(self, data, sectionName):
		self.data = data
		self.dataSize = len(data)
		self.sectionName = sectionName

		# 1st 32-bit (LE) int
		self.device = None
		# 2nd 32-bit (LE) int
		self.deviceVersion = None
		# 5th 32-bit (LE) int
		self.backupDate = None
		self.backupDateStr = None
		
		self.analyze()

	def analyze(self):
		self.device = util.getInt(self.data, 0)
		self.deviceVersion = util.getInt(self.data, 1 * util.intSize)
		self.backupDate = util.getInt(self.data, 4 * util.intSize)
		self.backupDateStr = time.asctime(time.localtime(self.backupDate))

	def printInfo(self):
		print("Device: {}".format(self.device))
		print("Device Version: {}".format(self.deviceVersion))
		print("Backup Date: {}".format(self.backupDateStr))
