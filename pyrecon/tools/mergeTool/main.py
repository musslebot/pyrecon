from pyrecon.main import openSeries
from pyrecon.classes import Section, Series
from pyrecon.tools import handleXML as xml
from pyrecon.tools.mergeTool import seriesHandlers as handlers
from pyrecon.gui.mergeTool import seriesHandlers as handlersGUI

class MergeWrapper:
	'''Contains MergeSeries and MergeSection objects.'''
	def __init__(self, *args, **kwargs):
		self.seriesMerge = None # MergeSeries object
		self.sectionMerges = None # List of MergeSection objects
		self.output_directory=None
		self.processArguments(args, kwargs)
	# Argument processing
	def processArguments(self, args, kwargs):
		self.processArgs(*args)
		self.processKwargs(**kwargs)
		self.checkAttributes()
	def processArgs(self, *args): #===
		return
	def processKwargs(self, **kwargs): #===
		return
	def checkAttributes(self): #===
		return
	# Class methods
	def run(self):
		'''Performs merge for <series> and <sections>'''
		self.seriesMerge.run()
		for sectionMerge in self.sectionMerges:
			sectionMerge.run()
	def save(self):
		if self.output_directory is None:
			# Ask for output_directory
			return
		# Create mergedSeries from MergeSeries object
		mergedSeries = self.series.output()
		# For each MergeSection, create section and add to mergedSeries' sections
		for section in self.sections:
			mergedSeries.sections.append( section.output() )
		# Write series/sections
		xml.writeSeries(mergedSeries, self.output_directory, sections=True)

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

class MergeSection:
	'''MergeSection contains the two sections to be merged, handlers for how to merge the sections, and functions for manipulating class data.'''
	def __init__(self, *args, **kwargs):
		# Sections to be merged
		self.section1 = None
		self.section2 = None
		# Series merge handlers
		self.handle_attributes = None
		self.handle_images = None
		self.handle_contours = None
		# Merged stuff
		self.attributes = None
		self.images = None
		self.contours = None
		# Process arguments
		self.processArguments(args, kwargs)
	# Argument processing
	def processArguments(self, *args, **kwargs):
		'''Process given arguments.'''
		def processArgs(self, args):
			for arg in args:
				print arg
		def processKwargs(self, kwargs):
			for kwarg in kwargs:
				print kwarg
	# Class methods
	def run(self):
		'''Run mergeTool using designated handler functions.'''
		return
	