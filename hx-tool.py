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

	if args.export or args.export_hls:
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
				b.exportAllIRs()
			else:
				b.printAllIRs()

		if args.export_hls:
			b.exportAllSetLists()

	if args.set_list:
		if doExport:
			b.exportAllPresets()
		else:
			b.printAllSetLists()

if __name__ == '__main__':
	import argparse as ap
	import sys
	import os.path
	
	parser = ap.ArgumentParser("hx-tool.py")
	
	parser.add_argument("filename", action="store", default=None, help="HX Stmop backup file name")
	parser.add_argument("--ir", action="store_true", help="Show IR names")
	parser.add_argument("--debug", action="store_true", help="Show debug info")
	parser.add_argument("--global-settings", action="store_true", help="Show global settings")
	parser.add_argument("--set-list", action="store_true", help="Show set list info")
	parser.add_argument("--export", action="store_true", help="Export data files")
	parser.add_argument("--export-hls", action="store_true", help="Export set list files")

	args = parser.parse_args(sys.argv[1:])
	
	#!print(args)

	if (os.path.isfile(args.filename)):
		main(args)
	else:
		print("Error: {} does not exist".format(args.filename))
