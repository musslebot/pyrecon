'''Driver for merging two series objects (as per .ser XML file). Does not take into account differences in the sections associated with this series -- refer to sectionMerge.py for merging sections.'''
from pyrecon.classes import *

class MergeSeries:
	'''MergeSeries contains the two series to be merged, handlers for how to merge the series, and functions for manipulating class data.'''
	def __init__(self, *args, **kwargs):
		# Series to be merged
		self.series1 = None
		self.series2 = None
		# Handlers
		self.handle_attributes = None 
		self.handle_contours = None
		self.handle_zcontours = None
		# Merged stuff
		self.attributes = None
		self.contours = None
		self.zcontours = None
		# Process arguments
		self.processArguments(args, kwargs)
	# Argument processing
	def processArguments(self, args, kwargs):
		'''Process given arguments.'''
		self.processArgs(*args)
		self.processKwargs(**kwargs)
		self.checkAttributes() # Make sure all necessary data is complete
	def processArgs(self, *args):
		for arg in args:
			# Series object
			if arg.__class__.__name__ == 'Series':
				if self.series1 is None:
					self.series1 = arg
				elif self.series2 is None:
					self.series2 = arg
	def processKwargs(self, **kwargs): #===
		for kwarg in kwargs:
			print kwarg, kwargs[kwarg]
	def checkAttributes(self): #===
		if self.series1 is None or self.series2 is None:
			print '1 or more Series object is not present'
	# Class methods
	def run(self): #===
		'''Run mergeTool using designated handler functions.'''
		# If graphical
		# - Make seriesWrapper

		return
	def output(self):
		return Series(self.attributes, self.contours, self.zcontours)


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
