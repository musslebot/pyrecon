#!/bin/bash

# This file will take input from git's merge function and load the appropriate pyrecon mergeTool GUI handler.
# Installation instructs:
#     In order to replace Git's merge driver with pyrecon's mergeTool:
#	  1) Add the following lines to your repository's .git/config file
#         [merge "pymerge"]
#             name = pyrecon mergetool driver
#             driver = <PATH TO gitmerge.py> %O %A %B
#             recursive = binary
#     2) Add the following line to your repository's .git/info/attributes file
#         * merge=pymerge

# This passes paths to the series to merge ($1 and $2) and the directory in which they are located
# Make sure the following path to gitmerge is correct:
python ~/Documents/pyrecon/pyrecon/mergeTool/gitmerge.py $1 $2 $PWD
exit 0 # This tells Git that the merge was a success and preps the commit
# exit 1 # This tells Git that the merge was unsuccessful