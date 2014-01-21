from lxml import etree as ET

def process(path):
	'''Process XML file defined by path'''
	try:
		# Determine type of XML file and process
		tree = ET.parse(path)
		root = tree.getroot()
		if root.tag == 'Section':
			return processSectionFile(tree)
	except:
		print('Problem processing: '+str(path))

def processSectionFile(tree):
	'''Returns attribute dictionary, image object, and contour list associated with <tree>'''
	root = tree.getroot()
	# Gather attributes
	attributes = {}
	attributes['index']=int(root.get('index'))
	attributes['thickness']=float(root.get('thickness'))
	attributes['alignLocked']=bool(root.get('alignLocked').upper())
	
	# Gather image #===

	image = 'Image object' #===

	# Gather contours #===
	contours = []
	return attributes, image, contours
