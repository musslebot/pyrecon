import sys, os
from pyrecon import handleXML as xml
from pyrecon import mergeTool

# Assign arguments to variables
args = sys.argv
aFile = args[1] # File in current branch
bFile = args[2] # File in other branch
directory = args[3] # Directory of current branch

# Load objects from files
aObject = xml.process( aFile, obj=True ) # Series or Section object of file
bObject = xml.process( bFile, obj=True ) # "

# Run appropriate mergeTool functions
if aObject.__class__.__name__ == 'Section':
	mergedFile = mergeTool.sectionMerge.main(aObject, bObject, graphical=True)
elif aObject.__class__.__name__ == 'Series':
	mergedFile = mergeTool.seriesMerge.main(aObject, bObject, graphical=True)

# Delete old file
# Write new file
