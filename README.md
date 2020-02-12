# hx-tools
Command-line tool(s) to examine and export data from Line 6 Helix backup files (*.hxb) and Helix set-list files (*.hls)

## Motivation

I want to be able to examine Helix files on Linux, an OS that Line 6 has completely ignored, without having to do the following:

1. Launch a Windows virtual machine
2. Connect my HX Stomp to my computer

## Getting started

### Limitations

The amount of testing that has been done is *minimal*.  This software has only been tested with HX Stomp backups from v2.81 and v2.82.

The files that are exported by hx-tool should *NOT* be loaded onto Helix or HX devices.  I cannot guarantee that they won't damage the device.

The few IRs that I've exported with hx-tool seem to be identical to those exported from HX Edit, however, the .hls and .hlx files differ from those written by HX Edit in subtle ways.

### Prequisites

* Linux
* python3

Note: the scripts are certain to break on Windows due to file path separator issues, which are easy to fix in the future if there is demand for it.

### Installation

1. Clone this repo
```
$ git clone https://github.com/frankdeath/hx-tools.git
```

2. Add the hx-tools directory to the PATH
```
$ export PATH=${PATH}:${PWD}/hx-tools
```

### Usage
```
$ ./hx-tool.py -h
usage: hx-tool.py [-h] [--debug] [--global-settings] [--set-list] [-s S]
                  [--ir] [-i I] [--preset] [-p P] [-x]
                  filename

positional arguments:
  filename           HX Stmop backup file name

optional arguments:
  -h, --help         show this help message and exit
  --debug            Show debug info
  --global-settings  Show global settings
  --set-list         Show set list info
  -s S               Set-list index
  --ir               Show IR names
  -i I               IR index
  --preset           Show Preset details
  -p P               Preset index
  -x                 Export data files
```

### Examples
```
$ ./hx-tool.py --ir backup.hxb
```
Print all the IR names.

```
$ ./hx-tool.py --ir -i 1-10,21 backup.hxb
```
Print a subset of the IR names.

```
$ ./hx-tool.py --preset
```
Print all the preset names.

```
$ ./hx-tool.py --preset -p 42,100-109 setlist.hls
```
Print a subset of the preset names.

```
$ ./hx-tool.py --ir -x backup.hxb
```
Export all IRs as .wav files.

```
$ ./hx-tool.py --set-list -x backup.hxb
```
Export all set lists as .hls files.

```
$ ./hx-tool.py --preset -x setlist.hls
```
Export all presets as .hlx files.

## Acknowledgements

Thanks to @AntonyCorbett.  This project would not have been possible without the documentation in [HelixBackupFiles](https://github.com/AntonyCorbett/HelixBackupFiles.git)
