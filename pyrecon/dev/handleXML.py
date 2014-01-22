from lxml import etree as ET
# from pyrecon.dev.classesDev import Section, Image, Transform #=== PROBLEMS IMPORTING, Loop?

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
		print('Problem processing: '+str(path)+'\n\thandleXML.process()')

def sectionAttributes(node):
	'''Returns a Section attribute dictionary for a given node.'''
	attributes = {}
	attributes['index']=int(node.get('index'))
	attributes['thickness']=float(node.get('thickness'))
	attributes['alignLocked']=bool(node.get('alignLocked').upper())
	return attributes

def imageAttributes(node):
	'''Returns an Image attribute dictionary for a given node.'''
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
	'''Returns a Transform attribute dicitonary for a given node.'''
	attributes = {}
	attributes['dim'] = int(node.get('dim'))
	attributes['xcoef'] = [int(x) for x in node.get('xcoef').strip().split(' ')]
	attributes['ycoef'] = [int(x) for x in node.get('ycoef').strip().split(' ')]
	return attributes

def processSectionFile(tree): #===
	'''Returns attribute dictionary, image object, and contour list associated with a Section's XML <tree>'''
	root = tree.getroot()

	attributes = sectionAttributes(root)

	# Process images and contours
	images = []
	contours = []
	for transform in root:
		print('Transform about to be created') #===
 		transformObject = Transform( transformAttributes(transform) ) # Create transform object for current XML tree node
		print('TransformObject created') #===
		for child in transform:
			if child.tag == 'Image':
				# images.append( Image(imageAttributes(child),transformObject) ) # Create image object and append to images
				print('Image about to be created') #===
				#images.append( Image(imageAttributes(child)) ) # Create image object and append to images
				print('Image created and appended') #===		
			elif child.tag == 'Contour':
				print('Contour found and skipped') #===

	#=== DEBUG STATEMENTS
	print('Section Attributes: '+str(attributes))
	print('Section Image: '+str(images))
	print('Section Contours: '+str(contours))
	#===
	
	return attributes, images, contours

