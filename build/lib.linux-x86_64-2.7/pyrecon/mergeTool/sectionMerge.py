'''Receives 2 sections and attempts to merge them into one section. Conflicts are handled by <handler>.'''
import pyrecon.mergeTool.handlers as handlers
import pyrecon.mergeTool.handlersGUI as handlersGUI

def main(section1, section2, graphical=False):
	# Check for type issues
	if section1.__class__.__name__ != section2.__class__.__name__:
		print('Invalid file type for section1 and/or section2: Must be a pyrecon.classes.Section object.')
	# Image

	# Contours
	return mergedSection

# Image
def mergeImages(sectionA, sectionB, handler=handlers.sectionImages):
	src = sectionA.image.src == sectionB.image.src
	mag = sectionA.image.mag == sectionB.image.mag
	if src & mag:
		return sectionA.image
	return handler(sectionA.image, sectionB.image)

# Contours
def mergeContours(sectionA, sectionB, handler=handlers.sectionContours):
    '''Returns merged contours between two sections'''
    # Populate shapely shapes
    sectionA.popshapes()
    sectionB.popshapes()
    
    # Copy contour lists for both sections; these lists are altered
    contsA = [cont for cont in sectionA.contours]
    contsB = [cont for cont in sectionB.contours]
    
    # Find overlapping contours
    ovlpsA, ovlpsB = checkOverlappingContours(contsA, contsB)
    
    # Separate into completely overlapping or incompletely overlapping
    compOvlp, confOvlp = separateOverlappingContours(ovlpsA, ovlpsB)

    # Identify unique contours
    uniqueA, uniqueB = contsA, contsB
    
    # Handle conflicts
    mergedConts = handler(uniqueA, compOvlp, confOvlp, uniqueB)
    
    return mergedConts

def checkOverlappingContours(contsA, contsB, threshold=(1+2**(-17)), sameName=True):
    '''Returns lists of mutually overlapping contours.''' 
    ovlpsA = [] # Section A contours that have overlaps in section B
    ovlpsB = [] # Section B contours that have overlaps in section A

    for contA in contsA:
        ovlpA = []
        ovlpB = []
        for contB in contsB:
            if sameName and contA.name == contB.name and contA.overlaps(contB, threshold) != 0:
                ovlpA.append(contA)
                ovlpB.append(contB)
            elif not sameName and contA.overlaps(contB, threshold) != 0:
                ovlpA.append(contA)
                ovlpB.append(contB)
        ovlpsA.extend(ovlpA)
        ovlpsB.extend(ovlpB)
    
    # Remove all non-unique contours from contsA and contsB
    for cont in ovlpsA:
        if cont in contsA:
            contsA.remove(cont)
    
    for cont in ovlpsB:
        if cont in contsB:
            contsB.remove(cont)

    return ovlpsA, ovlpsB

def separateOverlappingContours(ovlpsA, ovlpsB, threshold=(1+2**(-17)), sameName=True):
    '''Returns a list of completely overlapping pairs and a list of conflicting overlapping pairs.'''
    compOvlps = [] # list of completely overlapping contour pairs
    confOvlps = [] # list of conflicting overlapping contour pairs
    
    # Check for COMPLETELY overlapping contours 1st
    for contA in ovlpsA:
        for contB in ovlpsB:
            if sameName and contA.name == contB.name:
                if contA.overlaps(contB, threshold) == 1:
                    compOvlps.append([contA, contB])
            elif not sameName:
                if contA.overlaps(contB, threshold) == 1:
                    compOvlps.append([contA, contB])
                
    # Check for CONFLICTING overlapping contours
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
