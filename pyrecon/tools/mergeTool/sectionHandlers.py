'''Driver for merging two section objects (as per section XML file).'''
from pyrecon.classes import *
def nonGraphicalMerge(section1, sections2):
	mergedImage = mergeImages(section1, section2)
	mergedContours = mergeContours(section1, section2)
	mergedAttributes = mergeAttributes(section1, section2)
	# Combine merged properties into a section object
	return Section(mergedImage, mergedContours, mergedAttributes)
def graphicalMerge(section1, section2):
	from PySide.QtGui import QApplication
	from pyrecon.gui.mergeTool import sectionHandlers as handlersGUI
	# Merge 
	app = QApplication.instance()
	if app is None: # Create QApplication if doesn't exist
		app = QApplication([])
	newImage = mergeImages(section1, section2,
		handler=handlersGUI.sectionImages)
	newContours = mergeContours(section1, section2,
		handler=handlersGUI.sectionContours)
	newAttributes = mergeAttributes(section1, section2,
		handler=handlersGUI.sectionAttributes)
	# Gather data from handlers
	try: # GUI resolution used
		mergedImage = newImage.output
	except: # No conflict, no GUI
		mergedImage = newImage
	try: # "
		mergedContours = newContours.output
	except: # "
		mergedContours = newContours
	try: # "
		mergedAttributes = newAttributes.output
	except: # "
		mergedAttributes = newAttributes
	# Combine merged properties into a section object
	return Section(mergedImage, mergedContours, mergedAttributes)
# MERGE FUNCTIONS
# - Image
def mergeImages(sectionA, sectionB, handler=sectionImages, parent=None):
	return handler(sectionA.image, sectionB.image, parent=parent)
# - Contours
def mergeContours(sectionA, sectionB, handler=sectionContours, parent=None):
	'''Returns merged contours between two sections'''
	# Populate shapely shapes
	sectionA.popShapes()
	sectionB.popShapes()
	# Copy contour lists for both sections;
	# These lists only contain unique contours after next two functions
	contsA = [cont for cont in sectionA.contours]
	contsB = [cont for cont in sectionB.contours]
	# Find overlapping contours
	ovlpsA, ovlpsB = checkOverlappingContours(contsA, contsB)
	# Remove all non-unique contours from contsA and contsB
	for cont in ovlpsA:
		if cont in contsA:
			contsA.remove(cont)
	for cont in ovlpsB:
		if cont in contsB:
			contsB.remove(cont)
	# Separate into completely overlapping or incompletely overlapping
	compOvlp, confOvlp = separateOverlappingContours(ovlpsA, ovlpsB)
	# Identify unique contours
	uniqueA, uniqueB = contsA, contsB
	# Handle conflicts
	mergedConts = handler(uniqueA, compOvlp, confOvlp, uniqueB, sections=(sectionA,sectionB), parent=parent)
	return mergedConts
def checkOverlappingContours(contsA, contsB, threshold=(1+2**(-17)), sameName=True):
	'''Returns lists of mutually overlapping contours.''' 
	ovlpsA = [] # Section A contours that have overlaps in section B
	ovlpsB = [] # Section B contours that have overlaps in section A
	for contA in contsA:
		ovlpA = []
		ovlpB = []
		for contB in contsB:
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
	return ovlpsA, ovlpsB
def separateOverlappingContours(ovlpsA, ovlpsB, threshold=(1+2**(-17)), sameName=True):
	'''Returns a list of completely overlapping pairs and a list of conflicting overlapping pairs.'''
	compOvlps = [] # list of completely overlapping contour pairs
	confOvlps = [] # list of conflicting overlapping contour pairs
	# Check for COMPLETELY overlapping contours first (overlaps == 1)
	for contA in ovlpsA:
		for contB in ovlpsB:
			if sameName and contA.name == contB.name:
				if contA.overlaps(contB, threshold) == 1:
					compOvlps.append([contA, contB])
			elif not sameName:
				if contA.overlaps(contB, threshold) == 1:
					compOvlps.append([contA, contB])		
	# Check for CONFLICTING overlapping contours (overlaps != 0 or 1)
	for contA in ovlpsA:
		for contB in ovlpsB:
			if sameName and contA.name == contB.name:
				overlap = contA.overlaps(contB, threshold)
				if overlap != 0 and overlap != 1:
					confOvlps.append([contA, contB])
			elif not sameName:
				overlap = contA.overlaps(contB, threshold)
				if overlap != 0 and overlap != 1:
					confOvlps.append([contA, contB])
	return compOvlps, confOvlps
# - Attributes
def mergeAttributes(sectionA, sectionB, handler=sectionAttributes, parent=None):
	# extract attributes from class dictionaries
	attributes = ['name', 'index', 'thickness', 'alignLocked']
	secAatts = {} 
	secBatts = {}
	for key in attributes:
		secAatts[key] = sectionA.__dict__[key]
		secBatts[key] = sectionB.__dict__[key]
	return handler(secAatts, secBatts, parent=parent)










# SECTION
# - Image
def sectionImages(imageA, imageB):
	if imageA == imageB:
		return imageA
	padding = 20
	print('Section image conflicts:')
	print('='*(padding*3))
	# Header
	print( 'Attribute'.ljust(padding) ),
	print( 'Image A Value'.ljust(padding) ),
	print( 'Image B Value'.ljust(padding) )
	print( '---------'.ljust(padding) ),
	print( '-------------'.ljust(padding) ),
	print( '-------------'.ljust(padding) )

	# Attributes
	print( 'Source:'.ljust(padding) ),
	print( imageA.src.ljust(padding) ),
	print( imageB.src.ljust(padding) )
	print( 'Magnification:'.ljust(padding) ),
	print( str(imageA.mag).ljust(padding) ),
	print( str(imageB.mag).ljust(padding) )
	print('='*(padding*3))
	resp = 0
	while str(resp).lower() not in ['a','b']:
		resp = raw_input('Enter either A or B to choose image for merged section: ')
		if str(resp).lower() == 'a':
			return imageA
		elif str(resp).lower() == 'b':
			return imageB
# - Contours
def sectionContours(uniqueA, compOvlp, confOvlp, uniqueB, sections=None):
	'''Returns list of contours to be added to merged series'''
	outputContours = []

	# Unique: Add unique contours to output
	outputContours.extend(uniqueA)
	outputContours.extend(uniqueB)

	# Completely overlapping: Add a single copy of compOvlp pair to output
	for pair in compOvlp:
		outputContours.append(pair[0])

	# Conflicting: Handle conflicting overlaps
	if sections != None:
		print('Contour Conflicts between: '+str(sectionA.name)+' and '+str(sectionB.name))
	for pair in confOvlp:
		print('Conflicting contour overlap')
		print(pair[0].__dict__) #===
		print(pair[1].__dict__) #=== 
		sel = 0
		while str(sel).lower() not in ['a','b']:
			sel = raw_input('Please enter A, B, or both to select what to output: ')
			if str(sel).lower() == 'a':
				outputContours.append(pair[0])
			elif str(sel).lower() == 'b':
				outputContours.append(pair[1])
			else:
				outputContours.append(pair[0])
				outputContours.append(pair[1])
	return outputContours
# - Attributes
def sectionAttributes(dictA, dictB):
	outputAttributes = {}
	for attribute in ['name','index','thickness', 'alignLocked']:
		if dictA[attribute] == dictB[attribute]:
			outputAttributes[attribute] = dictA[attribute]
		else:
			print('Conflict in attribute: '+str(attribute))
			print('A:{} or B:{}'.format(dictA[attribute], dictB[attribute]))
			choice = 0
			while str(choice).lower() not in ['a','b']: 
				choice = raw_input('Enter either A or B to choose attribute: ')
				if str(choice).lower() == 'a':
					outputAttributes[attribute] = dictA[attribute]
				elif str(choice).lower() == 'b':
					outputAttributes[attribute] = dictB[attribute]
				else:
					print('Invalid entry, try again.')
	return outputAttributes