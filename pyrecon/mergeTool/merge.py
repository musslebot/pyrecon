'''Main driver for mergeTool module.'''
#!/usr/bin/python
from pyrecon.main import openSeries
from pyrecon.classes import Section, Series
from pyrecon.mergeTool import sectionMerge, seriesMerge
import pyrecon.handleXML as xml
import argparse

def main(series1, series2, directory, *args, **kwargs): #===
	#=== Are path1/2 series or sections?
	#=== series+sections or just series?
	# GUI handlers?
	gui = False
	if 'graphical' in args or kwargs['graphical'] == True:
		gui = True
	# Merge series
	mergedSer = seriesMerge.main(series1, series2, graphical=gui)
	mergedSer.sections = [] # Change None to [] for adding sections
	# Merge sections
	allSections = zip(series1.sections, series2.sections)
	for secPair in allSections:
		mergedSec = sectionMerge.main(*secPair, graphical=gui)
		mergedSer.sections.append(mergedSec)
	# Write <series> & <sections> to XML files in directory
	xml.writeSeries(mergeSer, directory, sections=True)

def mergeSeries(): #=== 
	return
def mergeSections(): #===
	return

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Merge two series together.')
	parser.add_argument('input1', nargs=1, type=str, help='Path to the first series (or directory) or section file')
	parser.add_argument('input2', nargs=1, type=str, help='Path to the second series (or directory) or section file')
	parser.add_argument('outpath', nargs=1, type=str, help='Path to the directory for writing the merged object\'s XML files')
	parser.add_argument('graphical', nargs=1, type=bool, help='True/False for graphical version', default=False)
	try:
		args = vars(parser.parse_args())
		# Assign argparse things to their variables
		input1 = openSeries( str(args['input1'][0]) )
		input2 = openSeries( str(args['input2'][0]) )
		directory = str(args['outpath'][0])
		graphical = args['graphical'][0]
		main(input1, input2, directory, graphical=graphical) #===
	except:
		print('error loading. launching gui load tool')