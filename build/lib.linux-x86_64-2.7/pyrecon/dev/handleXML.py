from lxml import etree as ET

def process(path):
	'''Process XML file defined by path'''
	tree = ET.parse(path)
	root = tree.getroot()
	if root.tag == 'Section': # Process Section
		return processSectionFile(tree)
	elif root.tag == 'Series': # Process Series
		return processSeriesFile(tree)

def processSectionFile(tree): #===
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
		print contour.attributes['name']
		if contour.attributes['name'] == 'domain1':
			print 'match'
			contour.image = image

	return attributes, image, contours

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

def makeImageObject(attributes, transformObject):
	from pyrecon.dev.classesDev import Image
	imageObject = Image(attributes, transformObject)
	return imageObject

def makeContourObject(attributes, transformObject):
	from pyrecon.dev.classesDev import Contour
	contourObject = Contour(attributes, transformObject)
	return contourObject