#!/bin/bash
# This file will take input from git's merge function and load the appropriate pyrecon mergeTool GUI handler.
# Installation instructs:
#     In order to replace Git's merge driver with pyrecon's mergeTool:
#	  1) Add the following to your repository's .git/config file
#         [merge "pymerge"]
#             name = pyrecon mergetool driver
#             driver = <PATH TO gitmerge.py> %O %A %B
#             recursive = binary
#     2) Add the following to your repository's .git/info/attributes file
#         * merge=pymerge

# Make sure the following path to gitmerge is correct:
path_to_gitmerge = ~/Documents/pyrecon/pyrecon/mergeTool/gitmerge.py

python path_to_gitmerge $1 $2 $PWD
