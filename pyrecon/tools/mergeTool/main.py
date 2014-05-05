from pyrecon.classes import Series, Section
from pyrecon.tools import handleXML as xml

def createMergeSet(series1, series2):
	'''This function takes in two Series objects and returns a MergeSet to be used for the mergeTool'''

	mSer = MergeSeries(series1, series2)
	mSecs = []
	for i in range( len(series1.sections) ):
		mSecs.append( MergeSection(series1.sections[i],series2.sections[i]) )
	return MergeSet( mSer, mSecs )

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
		for mergeSec in self.sectionMerges: #===
			mergedSeries.sections.append(mergeSec.toSection())
		xml.writeSeries(mergedSeries, outpath, sections=True)
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

		# Contours conflict resolution stuff
		self.uniqueA = None
		self.uniqueB = None
		self.compOvlps = None
		self.confOvlps = None

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
		separatedConts = self.getCategorizedContours(overlaps=True)
		self.uniqueA = separatedConts[0]
		self.uniqueB = separatedConts[1]
		self.compOvlps = separatedConts[2]
		self.confOvlps = separatedConts[3]
		if (len(self.uniqueA+self.uniqueB) == 0 and 
			len(self.confOvlps) == 0):
			self.contours = self.section1.contours
	def isDone(self):
		'''Boolean indicating status of merge.'''
		return (self.attributes is not None and
				self.images is not None and
				self.contours is not None)
	def doneCount(self):
		'''Number of resolved issues'''
		return (self.attributes is not None,
				self.images is not None,
				self.contours is not None).count(True)
		
	# mergeTool functions
	def getCategorizedContours(self, threshold=(1+2**(-17)), sameName=True, overlaps=False):
		'''Returns lists of mutually overlapping contours between two Section objects.'''
		compOvlps = [] # Pairs of completely (within threshold) overlapping contours 
		confOvlps = [] # Pairs of incompletely overlapping contours

		# Compute overlaps
		OvlpsA = [] # Section1 contours that have ovlps in section2
		OvlpsB = [] # Section2 contours that have ovlps in section1
		for contA in self.section1.contours:
			ovlpA = []
			ovlpB = []
			for contB in self.section2.contours:
				overlap = contA.overlaps(contB, threshold)
				# If sameName: only check contours with the same name
				if (sameName and
					contA.name == contB.name and
					overlap != 0):
					ovlpA.append(contA)
					ovlpB.append(contB)
					if overlaps:
						if overlap == 1:
							compOvlps.append([contA,contB])
						elif overlap > 0: # Conflicting (non-100%) overlap
							confOvlps.append([contA,contB])
				# If not sameName: check all contours, regardless of same name
				elif not sameName and overlap != 0:
					ovlpA.append(contA)
					ovlpB.append(contB)
					if overlaps:
						if overlap:
							compOvlps.append([contA,contB])
						elif overlap > 0: # Conflicting (non-100%) overlap
							confOvlps.append([contA,contB])
			OvlpsA.extend(ovlpA)
			OvlpsB.extend(ovlpB)

		if overlaps:
			# Return unique conts from section1, unique conts from section2, completely overlapping contours, and incompletely overlapping contours
			return (
				[cont for cont in self.section1.contours if cont not in OvlpsA],
				[cont for cont in self.section2.contours if cont not in OvlpsB],
				compOvlps, confOvlps )
		else:
			return ([cont for cont in self.section1.contours if cont not in OvlpsA],
				[cont for cont in self.section2.contours if cont not in OvlpsB])
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
	def doneCount(self):
		'''Number of resolved issues'''
		return (self.attributes is not None,
				self.contours is not None,
				self.zcontours is not None).count(True)

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
