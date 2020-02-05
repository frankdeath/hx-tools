#!/usr/bin/env python3

'''
A command-line tool to examine .hxb files
'''

import backup

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

	if b.extension == '.hxb':
		# Print basic details by default
		b.printSummary()

		if args.global_settings:
			b.printGlobalSettings()

		if args.ir:
			if doExport:
				if args.i == 'all':
					b.exportAllIRs()
				else:
					b.exportIR(args.i)
			else:
				if args.i == 'all':
					b.printAllIRs()
				else:
					b.printIR(args.i)

	if args.set_list:
		if doExport:
			# Note: args.s has no effect if the data file is a .hls
			if args.s == 'all':
				b.exportAllSetLists()
			else:
				b.exportSetList(args.s)
		else:
			if args.s == 'all':
				b.printAllSetLists()
			else:
				b.printSetList(args.s)
	
	if args.preset:
		if doExport:
			if args.p == 'all':
				b.exportAllPresets()
			else:
				b.exportPreset(args.s, args.p)
		else:
			if args.p == 'all':
				b.printSetList(args.s)
			else:
				b.printPreset(args.s, args.p)


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
