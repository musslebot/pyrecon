#!/usr/bin/python
from pyrecon.tools.classes import *

def getDups(series):
	duplicateDict = series.locateDuplicates()
	for sec in duplicateDict:
		print 'Section index: '+str(sec)
		for thing in duplicateDict[sec]:
			print thing.name

def locateTracesTooFar(series, threshold=7):
	'''Locates traces of the same name separated by <threshold (default: 7)> sections that do not contain that section'''
	return