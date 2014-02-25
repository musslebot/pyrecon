'''gitmerge.py handles input given by gitmerge.sh, which is called by the git merge function. This program assumes that the series/section files are stored in a folder with the same name as the series (e.g. BBCHZ.ser and its sections are in a folder called BBCHZ).'''
import sys, os
from pyrecon import handleXML as xml
from pyrecon import mergeTool

# Assign arguments to variables
args = sys.argv
aFile = args[1] # File in current branch
bFile = args[2] # File in other branch
directory = args[3] # Directory of current branch

# Name of series is name of folder
serName = os.path.abspath(directory).split('/')[-1]

# Load objects from files
aObject = xml.process( aFile, obj=True ) # Series or Section object of file
aObject.name = serName
bObject = xml.process( bFile, obj=True ) # "
bObject.name = serName

# Directory needs '/' at the end
if directory[-1] != '/':
	directory += '/'

# Run appropriate mergeTool functions and write merged file
if aObject.__class__.__name__ == 'Section':
	aObject.name += ('.'+str(aObject.index)) # append index to name if section
	bObject.name += ('.'+str(bObject.index)) # "
	mergedFile = mergeTool.sectionMerge.main(aObject, bObject, graphical=True)
	os.remove(str(directory+aObject.name))
	xml.writeSection(mergedFile, directory)

elif aObject.__class__.__name__ == 'Series':
	mergedFile = mergeTool.seriesMerge.main(aObject, bObject, graphical=True)
	os.remove(str(directory+aObject.name+'.ser'))
	xml.writeSeries(mergedFile, directory)
	




