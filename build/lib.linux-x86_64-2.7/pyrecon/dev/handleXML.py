from lxml import etree as ET # lxml parsing library Element Tree module

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
			contour = makeContourObject(contourAttributes(elem), None)
			if contours == None:
				contours = []
			contours.append(contour)
		elif elem.tag == 'ZContour':
			zcontour = makeZContourObject(zContourAttributes(elem)) #===
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
		tForm = makeTransformObject( transformAttributes(transform) )
		for child in transform:
			if child.tag == 'Image':
				img = makeImageObject( imageAttributes(child), tForm )
				images.append(img)
			elif child.tag == 'Contour':
				cont = makeContourObject( contourAttributes(child), tForm)
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
		attributes['hidden'] = bool(node.get('hidden').capitalize())
		attributes['closed'] = bool(node.get('closed').capitalize())
		attributes['simplified'] = bool(node.get('simplified').capitalize())
		attributes['mode'] = int(node.get('mode'))
		attributes['border'] = tuple(float(x) for x in node.get('border').strip().split(' '))
		attributes['fill'] = tuple(float(x) for x in node.get('fill').strip().split(' '))
		attributes['points'] = zip([float(x.replace(',','')) for x in node.get('points').split()][0::2], [float(x.replace(',','')) for x in node.get('points').split()][1::2])
	except: # Contours in Series
		try:
			attributes = {}
			attributes['name'] = str(node.get('name'))
			attributes['closed'] = bool(node.get('closed').capitalize())
			attributes['mode'] = int(node.get('mode'))
			attributes['border'] = tuple(float(x) for x in node.get('border').strip().split(' '))
			attributes['fill'] = tuple(float(x) for x in node.get('fill').strip().split(' '))
			attributes['points'] = zip([float(x.replace(',','')) for x in node.get('points').split()][0::2], [float(x.replace(',','')) for x in node.get('points').split()][1::2])
		except:
			print('Problem retrieving contourAttributes')
	return attributes
def imageAttributes(node):
	attributes = {}
	attributes['src'] = str(node.get('src'))
	attributes['mag'] = float(node.get('mag'))
	attributes['contrast'] = float(node.get('contrast'))
	attributes['brightness'] = float(node.get('brightness'))
	attributes['red'] = bool(node.get('red').capitalize())
	attributes['green'] = bool(node.get('green').capitalize())
	attributes['blue'] = bool(node.get('blue').capitalize())
	return attributes
def sectionAttributes(node):
	attributes = {}
	attributes['index']=int(node.get('index'))
	attributes['thickness']=float(node.get('thickness'))
	attributes['alignLocked']=bool(node.get('alignLocked').upper())
	return attributes
def seriesAttributes(node):
	attributes = {}
	attributes['index'] = int(node.get('index'))
	attributes['viewport'] = tuple(float(x) for x in node.get('viewport').split(' '))
	attributes['units'] = str(node.get('units'))
	attributes['autoSaveSeries'] = bool(node.get('autoSaveSeries').capitalize())
	attributes['autoSaveSection'] = bool(node.get('autoSaveSection').capitalize())
	attributes['warnSaveSection'] = bool(node.get('warnSaveSection').capitalize())
	attributes['beepDeleting'] = bool(node.get('beepDeleting').capitalize())
	attributes['beepPaging'] = bool(node.get('beepPaging').capitalize())
	attributes['hideTraces'] = bool(node.get('hideTraces').capitalize())
	attributes['unhideTraces'] = bool(node.get('unhideTraces').capitalize())
	attributes['hideDomains'] = bool(node.get('hideDomains').capitalize())
	attributes['unhideDomains'] = bool(node.get('hideDomains').capitalize())
	attributes['useAbsolutePaths'] = bool(node.get('useAbsolutePaths').capitalize())
	attributes['defaultThickness'] = float(node.get('defaultThickness'))
	attributes['zMidSection'] = bool(node.get('zMidSection').capitalize())
	attributes['thumbWidth'] = int(node.get('thumbWidth'))
	attributes['thumbHeight'] = int(node.get('thumbHeight'))
	attributes['fitThumbSections'] = bool(node.get('fitThumbSections').capitalize())
	attributes['firstThumbSection'] = int(node.get('firstThumbSection'))
	attributes['lastThumbSection'] = int(node.get('lastThumbSection'))
	attributes['skipSections'] = int(node.get('skipSections'))
	attributes['displayThumbContours'] = bool(node.get('displayThumbContours').capitalize())
	attributes['useFlipbookStyle'] = bool(node.get('useFlipbookStyle').capitalize()) 
	attributes['flipRate'] = int(node.get('flipRate'))
	attributes['useProxies'] = bool(node.get('useProxies').capitalize())
	attributes['widthUseProxies'] = int(node.get('widthUseProxies'))
	attributes['heightUseProxies'] = int(node.get('heightUseProxies'))
	attributes['scaleProxies'] = float(node.get('scaleProxies'))
	attributes['significantDigits'] = int(node.get('significantDigits'))
	attributes['defaultBorder'] = tuple(float(x) for x in node.get('defaultBorder').split(' '))
	attributes['defaultFill'] = tuple(float(x) for x in node.get('defaultFill').split(' '))
	attributes['defaultMode'] = int(node.get('defaultMode'))
	attributes['defaultName'] = str(node.get('defaultName'))
	attributes['defaultComment'] = str(node.get('defaultComment'))
	attributes['listSectionThickness'] = bool(node.get('listSectionThickness').capitalize())
	attributes['listDomainSource'] = bool(node.get('listDomainSource').capitalize())
	attributes['listDomainPixelsize'] = bool(node.get('listDomainPixelsize').capitalize())
	attributes['listDomainLength'] = bool(node.get('listDomainLength').capitalize())
	attributes['listDomainArea'] = bool(node.get('listDomainArea').capitalize())
	attributes['listDomainMidpoint'] = bool(node.get('listDomainMidpoint').capitalize())
	attributes['listTraceComment'] = bool(node.get('listTraceComment').capitalize())
	attributes['listTraceLength'] = bool(node.get('listTraceLength').capitalize()) 
	attributes['listTraceArea'] = bool(node.get('listTraceArea').capitalize())
	attributes['listTraceCentroid'] = bool(node.get('listTraceCentroid').capitalize())
	attributes['listTraceExtent'] = bool(node.get('listTraceExtent').capitalize())
	attributes['listTraceZ'] = bool(node.get('listTraceZ').capitalize())
	attributes['listTraceThickness'] = bool(node.get('listTraceThickness').capitalize())
	attributes['listObjectRange'] = bool(node.get('listObjectRange').capitalize())
	attributes['listObjectCount'] = bool(node.get('listObjectCount').capitalize())
	attributes['listObjectSurfarea'] = bool(node.get('listObjectSurfarea').capitalize())
	attributes['listObjectFlatarea'] = bool(node.get('listObjectFlatarea').capitalize())
	attributes['listObjectVolume'] = bool(node.get('listObjectVolume').capitalize())
	attributes['listZTraceNote'] = bool(node.get('listZTraceNote').capitalize())
	attributes['listZTraceRange'] = bool(node.get('listZTraceRange').capitalize())
	attributes['listZTraceLength'] = bool(node.get('listZTraceLength').capitalize())
	attributes['borderColors'] = [tuple(float(x) for x in x.split(' ') if x != '') for x in [x.strip() for x in node.get('borderColors').split(',')] if len(tuple(float(x) for x in x.split(' ') if x != '')) == 3]
	attributes['fillColors'] = [tuple(float(x) for x in x.split(' ') if x != '') for x in [x.strip() for x in node.get('fillColors').split(',')] if len(tuple(float(x) for x in x.split(' ') if x != '')) == 3]
	attributes['offset3D'] = tuple(float(x) for x in node.get('offset3D').split(' '))
	attributes['type3Dobject'] = int(node.get('type3Dobject'))
	attributes['first3Dsection'] = int(node.get('first3Dsection'))
	attributes['last3Dsection'] = int(node.get('last3Dsection'))
	attributes['max3Dconnection'] = int(node.get('max3Dconnection'))
	attributes['upper3Dfaces'] = bool(node.get('upper3Dfaces').capitalize())
	attributes['lower3Dfaces'] = bool(node.get('lower3Dfaces').capitalize())
	attributes['faceNormals'] =bool(node.get('faceNormals').capitalize())
	attributes['vertexNormals'] = bool(node.get('vertexNormals').capitalize())
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
	attributes['tracesStopWhen'] = bool(node.get('tracesStopWhen').capitalize())
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
	attributes['closed'] = bool(node.get('closed').capitalize())
	attributes['border'] = tuple(float(x) for x in node.get('border').split(' '))
	attributes['fill'] = tuple(float(x) for x in node.get('fill').split(' '))
	attributes['mode'] = int(node.get('mode'))
	attributes['points'] = [tuple(float(x) for x in x.split(' ') if x != '') for x in [x.strip() for x in node.get('points').split(',')] if len(tuple(float(x) for x in x.split(' ') if x != '')) == 3]
	return attributes

# Create objects (prevents import loop)
def makeContourObject(attributes, transformObject):
	from pyrecon.dev.classesDev import Contour
	contourObject = Contour(attributes, transformObject)
	return contourObject
def makeImageObject(attributes, transformObject):
	from pyrecon.dev.classesDev import Image
	imageObject = Image(attributes, transformObject)
	return imageObject
def makeTransformObject(attributes):
	from pyrecon.dev.classesDev import Transform
	transformObject = Transform(attributes)
	return transformObject
def makeZContourObject(attributes):
	from pyrecon.dev.classesDev import ZContour
	zcontourObject = ZContour(attributes)
	return zcontourObject
