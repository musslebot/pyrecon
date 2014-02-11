'''Driver for merging two series objects (as per .ser XML file). Does not take into account differences in the sections associated with this series -- refer to sectionMerge.py for merging sections.'''

def main(series1, series2, graphical=False):
	# Check for type issues
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
		print('seriesMerge: Graphical handlers will be used.')
		# mergedContours = mergeContours(series1, series2, handler=handlersGUI.sectionImages)
		# mergedZContours = mergeZContours(series1, series2, handler=handlersGUI.sectionContours)
		# mergedAttributes = mergeAttributes(section1, section2, handler=handlersGUI.sectionAttributes)
	else: # Terminal
		print('seriesMerge: No graphical handlers.')
		# mergedContours = mergeContours(section1, section2)
		# mergedZContours = mergeZContours(section1, section2)
		# mergedAttributes = mergeAttributes(section1, section2)

def mergeContours(): #===
	return

def mergeZContours(): #===
	return

def mergeAttributes(): #===
	return