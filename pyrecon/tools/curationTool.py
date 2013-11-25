#!/usr/bin/python
from pyrecon.tools.classes import *
from pyrecon.tools.mergeTool import checkOverlappingContours, separateOverlappingContours

def locateDuplicates(series):
	'''Locates overlapping traces of the same name in a section. Returns a dictionary of section numbers with duplicates'''
	dictOfDuplicates = {}
	for section in series.sections:
		
		duplicates = []
		contourNames = [cont.name for cont in section.contours] # List of contour names
		# Go through each contour, see if name appears in contourName > 1 time
		for contour in section.contours:
			if contourNames.count(contour.name) > 1:
				duplicates.append(contour.name)
		if len(duplicates) > 0:
			dictOfDuplicates[section.index] = list(set(duplicates))
	return dictOfDuplicates


def locateTracesTooFar(series, threshold=7):
	'''Locates traces of the same name separated by <threshold (default: 7)> sections that do not contain that section'''
	return