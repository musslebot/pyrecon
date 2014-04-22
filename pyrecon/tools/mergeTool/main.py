from pyrecon.main import openSeries
from pyrecon.classes import Section, Series
from pyrecon.tools import handleXML as xml

class MergeSet:
	'''This object contains MergeSeries and MergeSection objects. This can then be passed into mergeTool functions.'''
	def __init__(self, *args, **kwargs):
		self.seriesMerge = None # MergeSeries object
		self.sectionMerge = None # List of MergeSection objects
		self.output_directory = None
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
			# Ask for output_directory #===
			return
		# Create mergedSeries from MergeSeries object
		mergedSeries = self.series.output()
		# For each MergeSection, create section and add to mergedSeries' sections
		for section in self.sections:
			mergedSeries.sections.append( section.output() )
		# Write series/sections
		xml.writeSeries(mergedSeries, self.output_directory, sections=True)

def main():
	return
	