#!/usr/bin/env python3

'''
A command-line tool to examine .hxb files
'''

import backup

def main(args):
	filename = args.filename
	
	b = backup.Backup(filename)
	b.read(debug=args.debug)

	if args.ir:
		for i in b.IRs:
			i.info()
 

if __name__ == '__main__':
	import argparse as ap
	import sys
	import os.path
	
	parser = ap.ArgumentParser("hx-tool.py")
	
	parser.add_argument("filename", action="store", default=None, help="HX Stmop backup file name")
	parser.add_argument("--ir", action="store_true", help="Show IR names")
	parser.add_argument("--debug", action="store_true", help="Show debug info")

	args = parser.parse_args(sys.argv[1:])
	
	#!print(args)
	#!print(args.filename)
	#!print(args.ir)

	if (os.path.isfile(args.filename)):
		main(args)
	else:
		print("Error: {} does not exist".format(args.filename))
