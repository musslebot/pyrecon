from lxml import etree as ET
from pyrecon.dev import classesDev

def process(path):
	'''Process XML file defined by path'''
	try:
		# Determine type of XML file and process
		tree = ET.parse(path)
		root = tree.getroot()
		if root.tag == 'Section': # Process Section
			return processSectionFile(tree)
		elif root.tag == 'Series': # Process Series
			return processSeriesFile(tree)
	except:
		print('Problem processing: '+str(path))

def sectionAttributes(node):
	attributes = {}
	attributes['index']=int(node.get('index'))
	attributes['thickness']=float(node.get('thickness'))
	attributes['alignLocked']=bool(node.get('alignLocked').upper())
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

def transformAttributes(node): #===
	attributes = {}
	attributes['dim'] = int(node.get('dim'))
	attributes['xcoef'] = node.get('xcoef').strip().split(' ')
	attributes['ycoef'] = node.get('ycoef').strip().split(' ')
	return attributes

def processSectionFile(tree): #===
	'''Returns attribute dictionary, image object, and contour list associated with a section <tree>'''
	# Process attributes
	root = tree.getroot()
	attributes = sectionAttributes(root)

	# Process images and contours
	images = []
	contours = []
	for transform in root:
		# Create transform object
		transformObject = Transform() #===
		for child in transform:
			if child.tag == 'Image':
				)
				images.append( Image(imgAttributes, transformObject) ) )
			
			elif child.tag == 'Contour':
				# Create contour object #===
				contours.append( (contour, transform) )

	def processSectionContours(tree): #===
		contours = [] # Gather all contours
		# Remove redundant contours
		return contours
	
	attributes = processSectionAttributes(tree)
	image = processSectionImages(tree)
	contours = processSectionContours(tree)
	
	return attributes, image, contours

