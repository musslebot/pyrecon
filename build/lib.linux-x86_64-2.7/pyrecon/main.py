'''Main, overarching functions.'''
from pyrecon.classes import Section, Series
import os, re

def openSeries(path):
	'''Returns a Series object with associated Sections from the same directory.'''
	# Process <path> and create Series object
	if '.ser' in path: # Search path for .ser 
		pathToSeries = path
	else: # or .ser in directory path?
		if path[-1] != '/':
			path += '/'
		pathToSeries = path+str([f for f in os.listdir(path) if '.ser' in f].pop())
	series = Series(pathToSeries)
	series.update(sections=True) # find sections in directory
	return series

#def merge(path1, path2, outputDirectory): #===
#    return

#def curate(path): #===
#    return

#def excel(path): #===
#    return

#def calibrate(path): #===
#    return