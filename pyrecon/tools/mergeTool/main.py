from pyrecon.classes import Series, Section
from pyrecon.tools import handleXML as xml

class MergeSet:
	'''This class takes in a MergeSeries object and a list(MergeSection objects).'''
	def __init__(self, *args, **kwargs):
		self.seriesMerge = None # MergeSeries object
		self.sectionMerges = None # List of MergeSection objects
		self.processArguments(args, kwargs)

	# Argument processing
	def processArguments(self, args, kwargs):
		'''Process given arguments.'''
		for arg in args:
			if arg.__class__.__name__ == 'MergeSeries':
				self.seriesMerge = arg
				self.name = arg.name
			elif type(arg) == type([]):
				self.sectionMerges = arg
			else:
				print 'Cannot process argument:',arg
		for kwarg in kwargs:
			print kwarg+':',kwargs[kwarg] #===

	def isDone(self):
		sectionsDone = True
		for section in self.sectionMerges:
			if not section.isDone():
				sectionsDone = False
				break
		return (self.seriesMerge.isDone() and sectionsDone)
	def writeMergeSet(self, outpath): #===
		'''Writes self.seriesMerge and self.sectionMerges to XML'''
		mergedSeries = self.seriesMerge.toSeries()
		mergedSeries.name = self.seriesMerge.name.replace('.ser','')
		xml.writeSeries(mergedSeries,outpath)
		for mergeSec in self.sectionMerges:
			xml.writeSection(mergeSec.toSection(), outpath)
		print 'Done!' #===
class MergeSection:
	'''This class manages data about two Section objects that are undergoing a merge.'''
	def __init__(self, *args, **kwargs):
		# Sections to be merged
		self.section1 = None
		self.section2 = None

		# Merged stuff
		self.attributes = None
		self.images = None
		self.contours = None

		# Process arguments
		self.processArguments(args, kwargs)
		self.checkConflicts()

	# Argument processing
	def processArguments(self, args, kwargs):
		'''Process given arguments.'''
		for arg in args:
			# Section object
			if arg.__class__.__name__ == 'Section':
				if not self.section1:
					self.section1 = arg
					self.name = arg.name
				elif not self.section2:
					self.section2 = arg
				else:
					print 'MergeSection already contains two Sections...'
		for kwarg in kwargs:
			print kwarg+':',kwargs[kwarg] #===

	def checkConflicts(self):
		'''Automatically sets merged stuff if they are equivalent'''
		# Are attributes equivalent?
		if self.section1.attributes() == self.section2.attributes():
			self.attributes = self.section1.attributes()
		# Are images equivalent?
		if self.section1.image == self.section2.image:
			self.images = self.section1.image
		# Are contours equivalent?
		uniques = self.getUniqueContours()
		ovlps = self.getOverlappingContours(separate=True)
		if (len(uniques[0]+uniques[1]) == 0 and 
			len(ovlps[1]) == 0):
			self.contours = self.section1.contours
	def isDone(self):
		'''Boolean indicating status of merge.'''
		return (self.attributes is not None and
				self.images is not None and
				self.contours is not None)
		
	# mergeTool functions
	def getUniqueContours(self):
		ovlpsA, ovlpsB = self.getOverlappingContours()
		uniqueA = [cont for cont in self.section1.contours if cont not in ovlpsA]
		uniqueB = [cont for cont in self.section2.contours if cont not in ovlpsB]
		return uniqueA, uniqueB
	def getOverlappingContours(self, threshold=(1+2**(-17)), sameName=True, separate=False):
		'''Returns lists of mutually overlapping contours between two Section objects.'''
		OvlpsA = [] # Section1 contours that have ovlps in section2
		OvlpsB = [] # Section2 contours that have ovlps in section1
		for contA in self.section1.contours:
			ovlpA = []
			ovlpB = []
			for contB in self.section2.contours:
				# If sameName: only check contours with the same name
				if sameName and contA.name == contB.name and contA.overlaps(contB, threshold) != 0:
					ovlpA.append(contA)
					ovlpB.append(contB)
				# If not sameName: check all contours, regardless of same name
				elif not sameName and contA.overlaps(contB, threshold) != 0:
					ovlpA.append(contA)
					ovlpB.append(contB)
			OvlpsA.extend(ovlpA)
			OvlpsB.extend(ovlpB)
		if not separate:
			return OvlpsA, OvlpsB
		else:
			return MergeSection.separateOverlappingContours(OvlpsA, OvlpsB, threshold, sameName)
	@staticmethod
	def separateOverlappingContours(ovlpsA, ovlpsB, threshold=(1+2**(-17)), sameName=True):
		'''Returns a list of completely overlapping pairs and a list of conflicting overlapping pairs.'''
		compOvlps = [] # list of completely overlapping contour pairs
		confOvlps = [] # list of conflicting overlapping contour pairs
		for contA in ovlpsA:
			for contB in ovlpsB:
				overlap = contA.overlaps(contB, threshold)
				if sameName and contA.name == contB.name:
					if overlap == 1:
						compOvlps.append([contA, contB])
					elif overlap != 0 and overlap != 1:
						confOvlps.append([contA, contB])
				elif not sameName:
					if overlap == 1:
						compOvlps.append([contA, contB])
					elif overlap != 0 and overlap != 1:
						confOvlps.append([contA, contB])
		return compOvlps, confOvlps
	def toSection(self):
		'''Returns a section object from self.attributes, self.images, and self.contours. Defaults any of these items to the self.section1 version if they are None (not resolved).'''
		return Section(
			self.attributes if self.attributes is not None else self.section1.attributes(),
			self.images if self.images is not None else self.section1.image,
			self.contours if self.contours is not None else self.section1.contours
			)
class MergeSeries:
	'''MergeSeries contains the two series to be merged, handlers for how to merge the series, and functions for manipulating class data.'''
	def __init__(self, *args, **kwargs):
		# Series to be merged
		self.series1 = None
		self.series2 = None

		# Merged stuff
		self.attributes = None
		self.contours = None
		self.zcontours = None

		# Process arguments
		self.processArguments(args, kwargs)
		self.checkConflicts()

	# Argument processing
	def processArguments(self, args, kwargs):
		'''Process given arguments.'''
		for arg in args:
			if arg.__class__.__name__ == 'Series':
				if not self.series1:
					self.series1 = arg
					self.name = arg.name+'.ser'
				elif not self.series2:
					self.series2 = arg
				else:
					print 'MergeSeries already contains two Series...'
		for kwarg in kwargs:
			print kwarg+':',kwargs[kwarg]
	def checkConflicts(self):
		'''Automatically set merged stuff for equivalent things.'''
		# Are attributes equivalent?
		if self.series1.attributes() == self.series2.attributes():
			self.attributes = self.series1.attributes()
		# Are contours equivalent?
		if self.series1.contours == self.series2.contours:
			self.contours = self.series1.contours
		# Are zcontours equivalent?
		if self.series1.zcontours == self.series2.zcontours:
			self.zcontours = self.series1.zcontours
	def isDone(self):
		'''Boolean indicating status of merge.'''
		return (self.attributes is not None and
				self.contours is not None and
				self.zcontours is not None)

	# mergeTool functions
	def getCategorizedZContours(self, threshold=(1+2**(-17))):
		'''Returns unique series1 zcontours, unique series2 zcontours, and overlapping contours.'''
		copyConts1 = [cont for cont in self.series1.zcontours]
		copyConts2 = [cont for cont in self.series2.zcontours]
		overlaps = []
		for contA in copyConts1:
			for contB in copyConts2:
				if contA.name == contB.name and contA.overlaps(contB, threshold):
					# If overlaps, append to overlap list and remove from unique lists
					overlaps.append(contA)
					copyConts1.remove(contA)
					copyConts2.remove(contB)
		return copyConts1, copyConts2, overlaps
	def toSeries(self):
		'''Returns a series object from self.attributes, self.contours, and self.zcontours. Defaults any of these items to the self.series1 version if they are None (not resolved).'''
		return Series(
			self.attributes if self.attributes is not None else self.series1.attributes(),
			self.contours if self.contours is not None else self.series1.contours,
			self.zcontours if self.zcontours is not None else self.series1.zcontours
			)
