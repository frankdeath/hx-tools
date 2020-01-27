#!/usr/bin/env python3

'''
A command-line tool to examine .hxb files
'''

import backup

# Temporarily call pprint directly, until more classes exist
import pprint

def main(args):
	filename = args.filename
	
	b = backup.Backup(filename)
	b.read(debug=args.debug)

	# Print basic details by default
	b.deviceInfo.printInfo()
	print("Description: {}".format(b.description))
	print("IRs: {}".format(len(b.IRs)))

	if args.global_settings:
		pprint.pprint(b.globalSettings)

	if args.ir:
		for i in b.IRs:
			i.info()

	if args.set_list:
		for sl in b.setLists:
			sl.printInfo()


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

	args = parser.parse_args(sys.argv[1:])
	
	#!print(args)

	if (os.path.isfile(args.filename)):
		main(args)
	else:
		print("Error: {} does not exist".format(args.filename))
