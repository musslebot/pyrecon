'''Driver for merging two series objects (as per .ser XML file). Does not take into account differences in the sections associated with this series -- refer to sectionMerge.py for merging sections.'''
from pyrecon.classes import *
import conflictResolution as handlers
import conflictResolutionGUI as handlersGUI

# MAIN FUNCTIONS
def main(series1, series2, graphical=False):
	# Check for argument issues
	if series1.__class__.__name__ != 'Series' or series2.__class__.__name__ != 'Series':
		print('Incorrect data types for series1 and/or series2:\n\tMust both be a pyrecon.classes.Section object.')
		return
	elif series1.name != series2.name:
		choice = 0
		while str(choice).lower()[0] not in ['y','n']: 
			choice = raw_input('The names of the series differ:%s vs. %s. are you sure you want to continue merging? Y or N: ') %(series1.name, series2.name)
			if str(choice).lower() == 'y':
				print('Continuing merge of differently named series.')
			elif str(choice).lower() == 'n':
				print('Aborting merge.')
				return
	# GUI or not GUI?
	if graphical == True: # GUI
		mergedSeries = graphicalMerge(series1, series2)
	else: # Terminal
		mergedSeries = nonGraphicalMerge(series1, series2)	
	return mergedSeries
def nonGraphicalMerge(series1, series2): #=== 
	mergedContours = mergeContours(series1, section2)
	# mergedZContours = mergeZContours(series1, series2)
	# mergedAttributes = mergeAttributes(series1, series2)
	return Series(mergedContours, mergedZContours, mergedAttributes)
def graphicalMerge(series1, series2): #=== HIGH PRIORITY
	from PySide.QtGui import QApplication
	# Merge 
	app = QApplication.instance()
	if app is None: # Create QApplication if doesn't exist
		app = QApplication([])
	newAttributes = mergeAttributes(series1, series2,
		handler=handlersGUI.sectionAttributes)
	newContours = mergeContours(series1, series2,
		handler=handlersGUI.sectionImages)
	newZContours = mergeZContours(series1, series2,
		handler=handlersGUI.sectionContours)
	app.exec_() # Open QWidgets and pause interpreter until closed
	# Gather data from handlers
	try: # GUI resolution used
		mergedAttributes = newAttributes.output
	except: # No conflict, no GUI
		mergedAttributes = newAttributes
	try: # "
		mergedContours = newContours.output
	except: # "
		mergedContours = newContours
	try: # "
		mergedZContours = newZContours.output
	except: # "
		mergedZContours = newZContours
	# Combine merged properties into a series object
	return Series(mergedContours, mergedZContours, mergedAttributes)
# MERGE FUNCTIONS
# - Contours
def mergeContours(series1, series2, handler=handlers.seriesContours): #===
	#=== Series contours reflect RECONSTRUCT palette options, return A for now
	return series1.contours
# - ZContours
def mergeZContours(series1, series2, handler=handlers.seriesZContours): #=== HIGH PRIORITY
	return
# - Attributes
def mergeAttributes(series1, series2, handler=handlers.seriesAttributes): #===
	return series1 #===