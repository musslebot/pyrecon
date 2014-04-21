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

