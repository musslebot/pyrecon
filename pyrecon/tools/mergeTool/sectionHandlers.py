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
			return separateOverlappingContours(OvlpsA, OvlpsB, threshold, sameName)

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
