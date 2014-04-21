# handleXML is imported in .update()
import os
class Section:
	def __init__(self, *args, **kwargs):
		self.name = None # Series name + index
		self.index = None
		self.thickness = None
		self.alignLocked = None
		#Non-attributes
		self.image = None
		self.contours = []
		self._path = None
		self.processArguments(args, kwargs)
	def processArguments(self, args, kwargs):
		'''Populates data from the *args and **kwargs arguments via self.update.'''
		# 1) ARGS
		for arg in args:
			try:
				self.update(arg)
			except:
				print('Could not process Section arg: '+str(arg))
		# 2) KWARGS #===
		for kwarg in kwargs:
			try:
				self.update(kwarg)
			except:
				print('Could not process Section kwarg: '+str(kwarg))
# MUTATORS
	def update(self, *args): #=== **kwargs eventually, need a way to choose overwrite or append to contours
		'''Changes Section data from arguments. Assesses type of argument then determines where to place it.'''
		for arg in args: # Assess type
			# Dictionary argument
			if type(arg) == type({}):
				for key in arg:
					# Dict:Attribute
					if key in self.__dict__:
						self.__dict__[key] = arg[key]
					# Dict:List
					elif type(arg[key]) == type([]):
						for item in arg[key]:
							if item.__class__.__name__ == 'Image':
								self.image = item
							elif item.__class__.__name__ == 'Contour':
								self.contours.append(item)
					# Dict:Image
					elif arg[key].__class__.__name__ == 'Image':
						self.image = arg[key]
					# Dict:Contour
					elif arg[key].__class__.__name__ == 'Contour':
						self.contours.append(arg[key])
			# String argument
			elif type(arg) == type(''): # Possible path to XML?
				import pyrecon.tools.handleXML as xml
				self.update(*xml.process(arg))
				self.name = arg.split('/')[-1]
				self._path = os.path.dirname(arg)
				if self._path[-1] != '/':
					self._path += '/'
			# Contour argument
			elif arg.__class__.__name__ == 'Contour':
				self.contours.append(arg)
			# Image argument
			elif arg.__class__.__name__ == 'Image':
				self.image = arg
			# List argument
			elif type(arg) == type([]):
				for item in arg:
					if item.__class__.__name__ == 'Contour':
						self.contours.append(item)
					elif item.__class__.__name__ == 'Image':
						self.image = item
		if self.image.__class__.__name__ == 'Image':
			self.image._path = self._path
	def popShapes(self):
		for contour in self.contours:
			contour.popShape()
# ACCESSORS
	def __len__(self):
		'''Return number of contours in Section object'''
		return len(self.contours)
	def __eq__(self, other):
		'''Allows use of == between multiple objects'''
		return (self.thickness == other.thickness and
				self.index == other.thickness and
				self.alignLocked == other.alignLocked and
				self.image == other.image and
				self.contours == other.contours)
	def __ne__(self, other):
		'''Allows use of != between multiple objects'''
		return not self.__eq__(other)
	def eq(self, other, eqType=None): #===
		'''Check equivalency with the option for type of attributes to compare. Default: __eq__'''
		if not eqType:
			return self.__eq__(other)
		elif eqType.lower() == 'attributes':
			return (self.thickness == other.thickness and
					self.index == other.index and
					self.alignLocked == other.alignLocked)
		elif eqType.lower() in ['images', 'image']:
			return (self.image == other.image)
		elif eqType.lower() in ['contours', 'contour']:
			return (self.contours == other.contours)
	def attributes(self):
		'''Returns a dict of this Section's attributes'''
		return {'name':self.name,
				'index':self.index,
				'thickness':self.thickness,
				'alignLocked':self.alignLocked
			}
# mergeTool functions
def getOverlappingContours(self, other, threshold=(1+2**(-17)), sameName=True, detailed=False):
	'''Returns lists of mutually overlapping contours between two Section objects.'''
	selfOvlps = [] # Self contours that have ovlps in other
	otherOvlps = [] # Other contours that have ovlps in self
	for contA in self.contours:
		ovlpA = []
		ovlpB = []
		for contB in other.contours:
			# If sameName: only check contours with the same name
			if sameName and contA.name == contB.name and contA.overlaps(contB, threshold) != 0:
				ovlpA.append(contA)
				ovlpB.append(contB)
			# If not sameName: check all contours, regardless of same name
			elif not sameName and contA.overlaps(contB, threshold) != 0:
				ovlpA.append(contA)
				ovlpB.append(contB)
		ovlpsA.extend(ovlpA)
		ovlpsB.extend(ovlpB)
	if not detailed:
		return ovlpsA, ovlpsB
	else:
		return separateOverlappingContours(ovlpsA, ovlpsB, threshold, sameName)
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