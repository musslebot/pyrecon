'''gitmerge.py handles input given by gitmerge.sh, which is called by the git merge function. This program assumes that the series/section files are stored in a folder with the same name as the series (e.g. BBCHZ.ser and its sections are in a folder called BBCHZ).'''
import sys, os
from pyrecon.tools import handleXML as xml
from pyrecon.tools import mergeTool

# Assign arguments to variables
args = sys.argv
aFile = os.path.abspath(args[1]) # File in current branch / MERGE OVERWRITES THIS
bFile = os.path.abspath(args[2]) # File in other branch

directory = os.path.dirname(aFile) # Directory of current branch

# Name of files is name of folder + either .ser or .<section.index>
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
	# Append index to name
	aObject.name += ('.'+str(aObject.index))
	bObject.name += ('.'+str(bObject.index))
	# Handle merge
	mergedFile = mergeTool.sectionMerge.main(aObject, bObject, graphical=True)
	# Overwrite aFile with new section
	xml.writeSection(mergedFile, directory, outpath=aFile, overwrite=True)

elif aObject.__class__.__name__ == 'Series':
	# Handle merge
	mergedFile = mergeTool.seriesMerge.main(aObject, bObject, graphical=True)
	# Overwrite aFile with new series
	xml.writeSeries(mergedFile, directory, outpath=aFile, overwrite=True)





