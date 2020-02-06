#!/usr/bin/env python3

'''
A command-line tool to examine .hxb files
'''

import backup
import util

def main(args):
	filename = args.filename
	
	# check for .hls or .hxb file
	
	b = backup.Backup(filename)
	b.read(debug=args.debug)

	doExport = False

	if args.x:
		# True = Success, False = Fail
		doExport = b.makeExportDir()
		#!print(doExport)

	if b.isFullBackup():
		# Print basic details by default
		b.printSummary()

		if args.global_settings:
			b.printGlobalSettings()

		if args.ir:
			if doExport:
				if args.i == 'all':
					b.exportAllIRs()
				elif util.argIsList(args.i):
					b.exportIRs(util.indexStringToList(args.i))
				else:
					b.exportIR(int(args.i))
			else:
				if args.i == 'all':
					b.printAllIRs()
				elif util.argIsList(args.i):
					b.printIRs(util.indexStringToList(args.i))
				else:
					b.printIR(int(args.i))

		if args.set_list:
			if doExport:
				if args.s == 'all':
					b.exportAllSetLists()
				elif util.argIsList(args.s):
					b.exportSetLists(util.indexStringToList(args.s))
				else:
					b.exportSetList(int(args.s))
			else:
				if args.s == 'all':
					b.printAllSetLists()
				elif util.argIsList(args.s):
					b.printSetLists(util.indexStringToList(args.s))
				else:
					b.printSetList(int(args.s))
	else:
		# A .hls file only has one set list?
		if args.set_list:
			if doExport:
				b.exportAllSetLists()
			else:
				b.printAllSetLists()
	
	if args.preset:
		if doExport:
			if args.p == 'all':
				b.exportAllPresets()
			elif util.argIsList(args.p):
				b.exportPresets(int(args.s), util.indexStringToList(args.p))
			else:
				if b.isFullBackup():
					b.exportPreset(int(args.s), int(args.p))
				else:
					b.exportPreset(1, int(args.p))
		else:
			if args.p == 'all':
				# should there be a printAllPresets function for consistency?
				b.printSetList(int(args.s))
			elif util.argIsList(args.p):
				b.printPresets(int(args.s), util.indexStringToList(args.p))
			else:
				if b.isFullBackup():
					b.printPreset(int(args.s), int(args.p))
				else:
					b.printPreset(1, int(args.p))

if __name__ == '__main__':
	import argparse as ap
	import sys
	import os.path
	
	parser = ap.ArgumentParser("hx-tool.py")
	
	parser.add_argument("filename", action="store", default=None, help="HX Stmop backup file name")
	parser.add_argument("--debug", action="store_true", help="Show debug info")
	parser.add_argument("--global-settings", action="store_true", help="Show global settings")
	parser.add_argument("--set-list", action="store_true", help="Show set list info")
	parser.add_argument("-s", action="store", default='0', help="Set-list index")
	parser.add_argument("--ir", action="store_true", help="Show IR names")
	parser.add_argument("-i", action="store", default='all', help="IR index")
	parser.add_argument("--preset", action="store_true", help="Show Preset details")
	parser.add_argument("-p", action="store", default='all', help="Preset index")
	parser.add_argument("-x", action="store_true", help="Export data files")

	args = parser.parse_args(sys.argv[1:])
	
	#!print(args)

	if (os.path.isfile(args.filename)):
		main(args)
	else:
		print("Error: {} does not exist".format(args.filename))
