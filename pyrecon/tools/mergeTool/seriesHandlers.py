'''Driver for merging two series objects (as per .ser XML file). Does not take into account differences in the sections associated with this series -- refer to sectionMerge.py for merging sections.'''
from pyrecon.classes import *

# SERIES MERGE FUNCTIONS
# - Contours
def seriesContours(contsA, contsB): #=== low priority, return A's contours
	return contsA
# - ZContours
def seriesZContours(ser1zconts, ser2zconts, ser3zconts): #=== HIGH PRIORITY
	# add leftover, unique zcontours to ser3zconts
	ser3zconts.extend(ser1zconts)
	ser3zconts.extend(ser2zconts)
	return ser3zconts
# - Attributes
def seriesAttributes(dictA, dictB): #=== low priority, return A's attributes
	mergedAttributes = {}
	for key in dictA:
		if key not in ['zcontours','contours', 'sections']: # ignore zcontours, contours, sections -- they have their own merge functions
			mergedAttributes[key] = dictA[key]
	return mergedAttributes
