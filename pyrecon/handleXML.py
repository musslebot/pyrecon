from pyrecon.classes import Contour, Image, Section, Series, Transform, ZContour
from lxml import etree as ET # lxml parsing library Element Tree module
import os, re

# MAIN XML PROCESS DRIVER
def process(path): #===
	'''Process XML file defined by path'''
	tree = ET.parse(path)
	root = tree.getroot()
	if root.tag == 'Section': # Process Section
		return processSectionFile(tree)
	elif root.tag == 'Series': # Process Series
		return processSeriesFile(tree)

# Process Files
def processSeriesFile(tree):
	root = tree.getroot()
	attributes = seriesAttributes(root)
	contours = None
	zcontours = None
	for elem in root:
		if elem.tag == 'Contour':
			contour = Contour(contourAttributes(elem), None)
			if contours == None:
				contours = []
			contours.append(contour)
		elif elem.tag == 'ZContour':
			zcontour = ZContour(zContourAttributes(elem)) #===
			if zcontours == None:
				zcontours = []
			zcontours.append(zcontour)
	return attributes, contours, zcontours
def processSectionFile(tree):
	'''Returns attribute dictionary, image object, and contour list associated with a Section's XML <tree>'''
	root = tree.getroot()

	attributes = sectionAttributes(root)

	# Process images and contours
	images = []
	contours = None
	for transform in root:
		tForm = Transform( transformAttributes(transform) )
		for child in transform:
			if child.tag == 'Image':
				img = Image( imageAttributes(child), tForm )
				images.append(img)
			elif child.tag == 'Contour':
				cont = Contour( contourAttributes(child), tForm)
				if contours == None:
					contours = []
				contours.append(cont)
 
	# Get first image from images list
	try:
		image = images.pop()
	except:
		image = None

	# Connect 'domain1' contour with section image
	for contour in contours:
		if contour.name == 'domain1':
			contour.image = image

	return attributes, image, contours

# Process attributes from tree nodes
def contourAttributes(node):
	try: # Contours in Sections
		attributes = {}
		attributes['name'] = str(node.get('name'))
		attributes['comment'] = str(node.get('comment'))
		attributes['hidden'] = node.get('hidden').capitalize() == 'True'
		attributes['closed'] = node.get('closed').capitalize() == 'True'
		attributes['simplified'] = node.get('simplified').capitalize() == 'True'
		attributes['mode'] = int(node.get('mode'))
		attributes['border'] = tuple(float(x) for x in node.get('border').strip().split(' '))
		attributes['fill'] = tuple(float(x) for x in node.get('fill').strip().split(' '))
		attributes['points'] = zip([float(x.replace(',','')) for x in node.get('points').split()][0::2], [float(x.replace(',','')) for x in node.get('points').split()][1::2])
	except: # Contours in Series
		try:
			attributes = {}
			attributes['name'] = str(node.get('name'))
			attributes['closed'] = node.get('closed').capitalize() == 'True'
			attributes['mode'] = int(node.get('mode'))
			attributes['border'] = tuple(float(x) for x in node.get('border').strip().split(' '))
			attributes['fill'] = tuple(float(x) for x in node.get('fill').strip().split(' '))
			attributes['points'] = zip([int(x.replace(',','')) for x in node.get('points').split()][0::2], [int(x.replace(',','')) for x in node.get('points').split()][1::2])
		except:
			print('Problem retrieving contourAttributes')
	return attributes
def imageAttributes(node):
	attributes = {}
	attributes['src'] = str(node.get('src'))
	attributes['mag'] = float(node.get('mag'))
	attributes['contrast'] = float(node.get('contrast'))
	attributes['brightness'] = float(node.get('brightness'))
	attributes['red'] = node.get('red').capitalize() == 'True'
	attributes['green'] = node.get('green').capitalize() == 'True'
	attributes['blue'] = node.get('blue').capitalize() == 'True'
	return attributes
def sectionAttributes(node):
	attributes = {}
	attributes['index']=int(node.get('index'))
	attributes['thickness']=float(node.get('thickness'))
	attributes['alignLocked']=node.get('alignLocked').upper() == 'True'
	return attributes
def seriesAttributes(node):
	attributes = {}
	attributes['index'] = int(node.get('index'))
	attributes['viewport'] = tuple(float(x) for x in node.get('viewport').split(' '))
	attributes['units'] = str(node.get('units'))
	attributes['autoSaveSeries'] = node.get('autoSaveSeries').capitalize() == 'True'
	attributes['autoSaveSection'] = node.get('autoSaveSection').capitalize() == 'True'
	attributes['warnSaveSection'] = node.get('warnSaveSection').capitalize() == 'True'
	attributes['beepDeleting'] = node.get('beepDeleting').capitalize() == 'True'
	attributes['beepPaging'] = node.get('beepPaging').capitalize() == 'True'
	attributes['hideTraces'] = node.get('hideTraces').capitalize() == 'True'
	attributes['unhideTraces'] = node.get('unhideTraces').capitalize() == 'True'
	attributes['hideDomains'] = node.get('hideDomains').capitalize() == 'True'
	attributes['unhideDomains'] = node.get('hideDomains').capitalize() == 'True'
	attributes['useAbsolutePaths'] = node.get('useAbsolutePaths').capitalize() == 'True'
	attributes['defaultThickness'] = float(node.get('defaultThickness'))
	attributes['zMidSection'] = node.get('zMidSection').capitalize() == 'True'
	attributes['thumbWidth'] = int(node.get('thumbWidth'))
	attributes['thumbHeight'] = int(node.get('thumbHeight'))
	attributes['fitThumbSections'] = node.get('fitThumbSections').capitalize() == 'True'
	attributes['firstThumbSection'] = int(node.get('firstThumbSection'))
	attributes['lastThumbSection'] = int(node.get('lastThumbSection'))
	attributes['skipSections'] = int(node.get('skipSections'))
	attributes['displayThumbContours'] = node.get('displayThumbContours').capitalize() == 'True'
	attributes['useFlipbookStyle'] = node.get('useFlipbookStyle').capitalize()  == 'True'
	attributes['flipRate'] = int(node.get('flipRate'))
	attributes['useProxies'] = node.get('useProxies').capitalize() == 'True'
	attributes['widthUseProxies'] = int(node.get('widthUseProxies'))
	attributes['heightUseProxies'] = int(node.get('heightUseProxies'))
	attributes['scaleProxies'] = float(node.get('scaleProxies'))
	attributes['significantDigits'] = int(node.get('significantDigits'))
	attributes['defaultBorder'] = tuple(float(x) for x in node.get('defaultBorder').split(' '))
	attributes['defaultFill'] = tuple(float(x) for x in node.get('defaultFill').split(' '))
	attributes['defaultMode'] = int(node.get('defaultMode'))
	attributes['defaultName'] = str(node.get('defaultName'))
	attributes['defaultComment'] = str(node.get('defaultComment'))
	attributes['listSectionThickness'] = node.get('listSectionThickness').capitalize() == 'True'
	attributes['listDomainSource'] = node.get('listDomainSource').capitalize() == 'True'
	attributes['listDomainPixelsize'] = node.get('listDomainPixelsize').capitalize() == 'True'
	attributes['listDomainLength'] = node.get('listDomainLength').capitalize() == 'True'
	attributes['listDomainArea'] = node.get('listDomainArea').capitalize() == 'True'
	attributes['listDomainMidpoint'] = node.get('listDomainMidpoint').capitalize() == 'True'
	attributes['listTraceComment'] = node.get('listTraceComment').capitalize() == 'True'
	attributes['listTraceLength'] = node.get('listTraceLength').capitalize()  == 'True'
	attributes['listTraceArea'] = node.get('listTraceArea').capitalize() == 'True'
	attributes['listTraceCentroid'] = node.get('listTraceCentroid').capitalize() == 'True'
	attributes['listTraceExtent'] = node.get('listTraceExtent').capitalize() == 'True'
	attributes['listTraceZ'] = node.get('listTraceZ').capitalize() == 'True'
	attributes['listTraceThickness'] = node.get('listTraceThickness').capitalize() == 'True'
	attributes['listObjectRange'] = node.get('listObjectRange').capitalize() == 'True'
	attributes['listObjectCount'] = node.get('listObjectCount').capitalize() == 'True'
	attributes['listObjectSurfarea'] = node.get('listObjectSurfarea').capitalize() == 'True'
	attributes['listObjectFlatarea'] = node.get('listObjectFlatarea').capitalize() == 'True'
	attributes['listObjectVolume'] = node.get('listObjectVolume').capitalize() == 'True'
	attributes['listZTraceNote'] = node.get('listZTraceNote').capitalize() == 'True'
	attributes['listZTraceRange'] = node.get('listZTraceRange').capitalize() == 'True'
	attributes['listZTraceLength'] = node.get('listZTraceLength').capitalize() == 'True'
	attributes['borderColors'] = [tuple(float(x) for x in x.split(' ') if x != '') for x in [x.strip() for x in node.get('borderColors').split(',')] if len(tuple(float(x) for x in x.split(' ') if x != '')) == 3]
	attributes['fillColors'] = [tuple(float(x) for x in x.split(' ') if x != '') for x in [x.strip() for x in node.get('fillColors').split(',')] if len(tuple(float(x) for x in x.split(' ') if x != '')) == 3]
	attributes['offset3D'] = tuple(float(x) for x in node.get('offset3D').split(' '))
	attributes['type3Dobject'] = int(node.get('type3Dobject'))
	attributes['first3Dsection'] = int(node.get('first3Dsection'))
	attributes['last3Dsection'] = int(node.get('last3Dsection'))
	attributes['max3Dconnection'] = int(node.get('max3Dconnection'))
	attributes['upper3Dfaces'] = node.get('upper3Dfaces').capitalize() == 'True'
	attributes['lower3Dfaces'] = node.get('lower3Dfaces').capitalize() == 'True'
	attributes['faceNormals'] = node.get('faceNormals').capitalize() == 'True'
	attributes['vertexNormals'] = node.get('vertexNormals').capitalize() == 'True'
	attributes['facets3D'] = int(node.get('facets3D'))
	attributes['dim3D'] = tuple(float(x) for x in node.get('dim3D').split())
	attributes['gridType'] = int(node.get('gridType'))
	attributes['gridSize'] = tuple(float(x) for x in node.get('gridSize').split(' '))
	attributes['gridDistance'] = tuple(float(x) for x in node.get('gridDistance').split(' '))
	attributes['gridNumber'] = tuple(float(x) for x in node.get('gridNumber').split(' '))
	attributes['hueStopWhen'] = int(node.get('hueStopWhen'))
	attributes['hueStopValue'] = int(node.get('hueStopValue'))
	attributes['satStopWhen'] = int(node.get('satStopWhen'))
	attributes['satStopValue'] = int(node.get('satStopValue'))
	attributes['brightStopWhen'] = int(node.get('brightStopWhen'))
	attributes['brightStopValue'] = int(node.get('brightStopValue'))
	attributes['tracesStopWhen'] = node.get('tracesStopWhen').capitalize()
	attributes['areaStopPercent'] = int(node.get('areaStopPercent'))
	attributes['areaStopSize'] = int(node.get('areaStopSize'))
	attributes['ContourMaskWidth'] = int(node.get('ContourMaskWidth'))
	attributes['smoothingLength'] = int(node.get('smoothingLength'))
	attributes['mvmtIncrement'] = tuple(float(x) for x in node.get('mvmtIncrement').split(' '))
	attributes['ctrlIncrement'] = tuple(float(x) for x in node.get('ctrlIncrement').split(' '))
	attributes['shiftIncrement'] = tuple(float(x) for x in node.get('shiftIncrement').split(' '))
	return attributes
def transformAttributes(node):
	def intorfloat(input):
		if '.' in input:
			return float(input)
		else:
			return int(input)
	attributes = {}
	attributes['dim'] = int(node.get('dim'))
	attributes['xcoef'] = [intorfloat(x) for x in node.get('xcoef').strip().split(' ')]
	attributes['ycoef'] = [intorfloat(x) for x in node.get('ycoef').strip().split(' ')]
	return attributes
def zContourAttributes(node):
	attributes = {}
	attributes['name'] = str(node.get('name'))
	attributes['closed'] = node.get('closed').capitalize() == 'True'
	attributes['border'] = tuple(float(x) for x in node.get('border').split(' '))
	attributes['fill'] = tuple(float(x) for x in node.get('fill').split(' '))
	attributes['mode'] = int(node.get('mode'))
	attributes['points'] = [(float(x.split(' ')[0]), float(x.split(' ')[1]), int(x.split(' ')[2])) for x in [x.strip() for x in node.get('points').split(',')] if len(tuple(float(x) for x in x.split(' ') if x != '')) == 3]
	return attributes

# Write objects to XML
def objectToElement(object):
	'''Returns an ElementTree Element for <object> that is appropriate for writing to an XML file.'''
	def contourToElement(contour):
		try: # Contour in Section
			element = ET.Element("Contour",
				name=str(contour.name),
				hidden=str(contour.hidden).lower(),
				closed=str(contour.closed).lower(),
				simplified=str(contour.simplified).lower(),
				border=str(contour.border[0])+' '+str(contour.border[1])+' '+str(contour.border[2]),
				fill=str(contour.fill[0])+' '+str(contour.fill[1])+' '+str(contour.fill[2]),
				mode=str(contour.mode),
				points= ', '.join([str(pt[0])+' '+str(pt[1]) for pt in contour.points])+','
				)
		except:
			try: # Contour in Series
				element = ET.Element("Contour",
				name=str(contour.name),
				closed=str(contour.closed).lower(),
				border=str(contour.border[0])+' '+str(contour.border[1])+' '+str(contour.border[2]),
				fill=str(contour.fill[0])+' '+str(contour.fill[1])+' '+str(contour.fill[2]),
				mode=str(contour.mode),
				points= ', '.join([str(pt[0])+' '+str(pt[1]) for pt in contour.points])+','
				)
			except:
				print('Problem creating Contour element')
		return element
	def imageToElement(image):
		element = ET.Element("Image",
			mag=str(image.mag),
			contrast=str(image.contrast),
			brightness=str(image.brightness),
			red=str(image.red).lower(),
			green=str(image.red).lower(),
			blue=str(image.blue).lower(),
			src=str(image.src)
			)
		return element
	def sectionToElement(section):
		element = ET.Element("Section",
			index=str(section.index),
			thickness=str(section.thickness),
			alignLocked=str(section.alignLocked).lower()
			)
		return element
	def seriesToElement(series):
		return element
	def transformToElement(transform):
		element = ET.Element("Transform",
			dim=str(transform.dim),
			xcoef=' '+' '.join([str(item) for item in transform.xcoef]),
			ycoef=' '+' '.join([str(item) for item in transform.ycoef])
			)
		return element
	def zcontourToElement(zcontour):
		return element
	if object.__class__.__name__ == 'Contour':
		return contourToElement(object)
	elif object.__class__.__name__ == 'Image':
		return imageToElement(object)
	elif object.__class__.__name__ == 'Section':
		return sectionToElement(object)
	elif object.__class__.__name__ == 'Series':
		return seriesToElement(object)
	elif object.__class__.__name__ == 'Transform':
		return transformToElement(object)
	elif object.__class__.__name__ == 'ZContour':
		return zcontourToElement(object)

def writeSection(section, directory): #=== attributes being change to true
	'''Writes <section> to an XML file in directory'''
	if str(directory[-1]) != '/':
		directory += '/'
	outpath = str(directory) + str(section.name)
	
	# Make root (Section attributes: index, thickness, alignLocked)
	root = objectToElement(section)
	
	# Image: Transform, Image, Contour
	image = objectToElement(section.image)
	imageContour = objectToElement([cont for cont in section.contours if cont.name == 'domain1'].pop())
	imageTransform = objectToElement([cont for cont in section.contours if cont.name == 'domain1'].pop().transform)
	imageTransform.append(image)
	imageTransform.append(imageContour)
	#Append image node to root
	root.append(imageTransform)

	# Contours and Transforms
	for contour in section.contours:
		if contour.name != 'domain1':
			contTransform = objectToElement(contour.transform)
			cont = objectToElement(contour)
			contTransform.append(cont)
			root.append(contTransform)

	# Make tree and write
	elemtree = ET.ElementTree(root)
	elemtree.write(outpath, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def writeSeries(series, directory, sections=False): #===
	'''Writes <series> to an XML file in directory'''
	# Pre-writing checks
	# Make sure directory is correctly input
	if directory[-1] != '/':
		directory += '/'
    # Check if directory exists, make if does not exist
	if not os.path.exists(outpath):
		os.makedirs(outpath)
	seriesoutpath = directory+series.name+'.ser'
    # Raise error if this file already exists to prevent overwrite
	if os.path.exists(seriesoutpath):
		raise IOError('\nFilename %s already exists.\nCancelled write to avoid overwrite'%seriesoutpath)
        
    #Build series root element
	attributes = series.__dict__ # take away name, contours, zcontours, sections


    # #=== The following are copy/paste from old function
    # 	attributes, contours = self.output()
    #     root = ET.Element(self.tag, attdict)
    #     #Build contour elements and append to root
    #     for contour in contours:
    #         root.append( ET.Element(contour.tag,contour.output()) )
    
    #     strlist = ET.tostringlist(root)
    #     #==========================================================================
    #     # Needs to be in order: hideTraces/unhideTraces/hideDomains/unhideDomains
    #         # Fix order:
    #     strlist = strlist[0].split(' ') # Separate single string into multiple strings for each elem
    #     count = 0
    #     for elem in strlist:
    #         if 'hideTraces' in elem and 'unhideTraces' not in elem:
    #             strlist.insert(1, strlist.pop(count))
    #         count += 1
    #     count = 0
    #     for elem in strlist:
    #         if 'unhideTraces' in elem:
    #             strlist.insert(2, strlist.pop(count))
    #         count += 1
    #     count = 0
    #     for elem in strlist:
    #         if 'hideDomains' in elem and 'unhideDomains' not in elem:
    #             strlist.insert(3, strlist.pop(count))
    #         count += 1
    #     count = 0
    #     for elem in strlist:
    #         if 'unhideDomains' in elem:
    #             strlist.insert(4, strlist.pop(count))
    #         count += 1
    #     #==========================================================================
    #         # Recombine into list of single str
    #     tempstr = ''
    #     for elem in strlist:
    #         tempstr += elem + ' '
    #     strlist = []
    #     strlist.append( tempstr.rstrip(' ') ) # Removes last blank space
    
    #     # Write to .ser file
    #     f = open(seriesoutpath, 'w')
    #     f.write('<?xml version="1.0"?>\n')
    #     f.write('<!DOCTYPE Section SYSTEM "series.dtd">\n\n')
    #     for elem in strlist:
    #         if '>' not in elem:
    #             f.write(elem),
    #         else:
    #             elem = elem+'\n'
    #             f.write(elem)
    #             if '/' in elem:
    #                 f.write('\n')        
    #     print('DONE')
    #     print('\tSeries output to: '+str(outpath+self.name+'.ser'))
	# Write sections too
	if sections == True:
		for sec in series.sections:
			writeSections(sec, directory)