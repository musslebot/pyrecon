'''Driver for merging two section objects (as per section XML file).'''
from pyrecon.classes import *
from pyrecon.gui.mergeTool.sectionHandlers import sectionAttributes, sectionImages, sectionContours
from pyrecon.tools import handleXML as xml

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
		self.loadHandlers()
	# Argument processing
	def processArguments(self, args, kwargs):
		'''Process given arguments.'''
		for arg in args:
			print arg #===
			# Section object
			if arg.__class__.__name__ == 'Section':
				if not self.section1:
					self.section1 = arg
				elif not self.section2:
					self.section2 = arg
				else:
					print 'MergeSection already contains two sections...'
		for kwarg in kwargs:
			print kwarg+':',kwargs[kwarg] #===
	def loadHandlers(self, handleType='graphical'):
		self.handle_attributes = sectionAttributes
		self.handle_images = sectionImages
		self.handle_contours = sectionContours
	# Merge functions
	def mergeImages(self):
		return self.handle_images(self.section1.image, self.section2.image)
	def mergeAttributes(self):
		# extract attributes from class dictionaries
		attributes = ['name', 'index', 'thickness', 'alignLocked']
		secAatts = {} 
		secBatts = {}
		for key in attributes:
			secAatts[key] = sectionA.__dict__[key]
			secBatts[key] = sectionB.__dict__[key]
		return self.handle_attributes(sec1atts, sec2atts)
	def mergeContours(self):
		return self.handle_contours(self.section1.contours, self.section2.contours)
	def save(self, directory=None):
		mergedSection = Section(self.attributes, self.images, self.contours)
		return mergedSection