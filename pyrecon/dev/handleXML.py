from lxml import etree as ET

def process(path):
	'''Process XML file defined by path'''
	tree = ET.parse(path)
	root = tree.getroot()
	if root.tag == 'Section': # Process Section
		return processSectionFile(tree)
	elif root.tag == 'Series': # Process Series
		return processSeriesFile(tree)

# SECTION
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

def sectionAttributes(node):
	attributes = {}
	attributes['index']=int(node.get('index'))
	attributes['thickness']=float(node.get('thickness'))
	attributes['alignLocked']=bool(node.get('alignLocked').upper())
	return attributes

# CONTOUR
def contourAttributes(node): #=== finish points and img (removed)
	attributes = {}
	attributes['name'] = str(node.get('name'))
	attributes['comment'] = str(node.get('comment'))
	attributes['hidden'] = bool(node.get('hidden').capitalize())
	attributes['closed'] = bool(node.get('closed').capitalize())
	attributes['simplified'] = bool(node.get('simplified').capitalize())
	attributes['mode'] = int(node.get('mode'))
	attributes['border'] = [float(x) for x in node.get('border').strip().split(' ')]
	attributes['fill'] = [float(x) for x in node.get('fill').strip().split(' ')]
	attributes['points'] = zip([float(x.replace(',','')) for x in node.get('points').split()][0::2], [float(x.replace(',','')) for x in node.get('points').split()][1::2])
	return attributes   

def makeContourObject(attributes, transformObject):
	from pyrecon.dev.classesDev import Contour
	contourObject = Contour(attributes, transformObject)
	return contourObject

# IMAGE
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

def makeImageObject(attributes, transformObject):
	from pyrecon.dev.classesDev import Image
	imageObject = Image(attributes, transformObject)
	return imageObject

# TRANSFORM
def transformAttributes(node):
	attributes = {}
	attributes['dim'] = int(node.get('dim'))
	attributes['xcoef'] = [int(x) for x in node.get('xcoef').strip().split(' ')]
	attributes['ycoef'] = [int(x) for x in node.get('ycoef').strip().split(' ')]
	return attributes

def makeTransformObject(attributes):
	from pyrecon.dev.classesDev import Transform
	transformObject = Transform(attributes)
	return transformObject

# Series
def processSeriesFile(tree): #===
	print('Series file!') #===
	root = tree.getroot()
	attributes = seriesAttributes(root)
	return attributes #contours, zcontours
def seriesAttributes(node): #===
	attributes = {}
	attributes['index'] = int(node.get('index'))
	attributes['viewport'] = [float(x) for x in node.get('viewport').split(' ')]
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
	# attributes['defaultThickness'] = 
	# attributes['zMidSection'] = 
	# attributes['thumbWidth'] = 
	# attributes['thumbHeight'] = 
	# attributes['fitThumbSections'] = 
	# attributes['firstThumbSection'] = 
	# attributes['lastThumbSection'] = 
	# attributes['skipSections'] = 
	# attributes['displayThumbContours'] = 
	# attributes['useFlipbookStyle'] = 
	# attributes['flipRate'] = 
	# attributes['useProxies'] = 
	# attributes['widthUseProxies'] = 
	# attributes['heightUseProxies'] = 
	# attributes['scaleProxies'] = 
	# attributes['significantDigits'] = 
	# attributes['defaultBorder'] = 
	# attributes['defaultFill'] = 
	# attributes['defaultMode'] = 
	# attributes['defaultName'] = 
	# attributes['defaultComment'] = 
	# attributes['listSectionThickness'] = 
	# attributes['listDomainSource'] = 
	# attributes['listDomainPixelsize'] = 
	# attributes['listDomainLength'] = 
	# attributes['listDomainArea'] =
	# attributes['listDomainMidpoint'] =
	# attributes['listTraceComment'] =
	# attributes['listTraceLength'] = 
	# attributes['listTraceArea'] = 
	# attributes['listTraceCentroid'] = 
	# attributes['listTraceExtent'] = 
	# attributes['listTraceZ'] = 
	# attributes['listTraceThickness'] =
	# attributes['listObjectRange'] = 
	# attributes['listObjectCount'] = 
	# attributes['listObjectSurfarea'] = 
	# attributes['listObjectFlatarea'] = 
	# attributes['listObjectVolume'] = 
	# attributes['listZTraceNote'] = 
	# attributes['listZTraceRange'] = 
	# attributes['listZTraceLength'] = 
	# attributes['borderColors'] = 
	# attributes['fillColors'] =
	# attributes['offset3D'] = 
	# attributes['type3Dobject'] = 
	# attributes['first3Dsection'] = 
	# attributes['last3Dsection'] = 
	# attributes['max3Dconnection'] = 
	# attributes['upper3Dfaces'] = 
	# attributes['lower3Dfaces'] = 
	# attributes['faceNormals'] =
	# attributes['vertexNormals'] = 
	# attributes['facets3D'] = 
	# attributes['dim3D'] = 
	# attributes['gridType'] = 
	# attributes['gridSize'] = 
	# attributes['gridDistance'] = 
	# attributes['gridNumber'] = 
	# attributes['hueStopWhen'] = 
	# attributes['hueStopValue'] = 
	# attributes['satStopWhen'] = 
	# attributes['satStopValue'] = 
	# attributes['brightStopWhen'] = 
	# attributes['brightStopValue'] = 
	# attributes['tracesStopWhen'] = 
	# attributes['areaStopPercent'] = 
	# attributes['areaStopSize'] = 
	# attributes['ContourMaskWidth'] =
	# attributes['smoothingLength'] =
	# attributes['mvmtIncrement'] =
	# attributes['ctrlIncrement'] = 
	# attributes['shiftIncrement'] =
	return attributes