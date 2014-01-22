from lxml import etree as ET

def process(path):
	'''Process XML file defined by path'''
	try:
		# Determine type of XML file and process
		tree = ET.parse(path)
		root = tree.getroot()
		if root.tag == 'Section':
			return processSectionFile(tree)
		elif root.tag == 'Series':
			return processSeriesFile(tree)
	except:
		print('Problem processing: '+str(path))

def processSectionFile(tree): #===
	'''Returns attribute dictionary, image object, and contour list associated with <tree>'''
	def processSectionAttributes(tree):
		attributes = {}
		attributes['index']=int(root.get('index'))
		attributes['thickness']=float(root.get('thickness'))
		attributes['alignLocked']=bool(root.get('alignLocked').upper())
		return attributes
	def processSectionImages(tree): #===
		images = [] # Gather all Image nodes
		image = ''
		# Reduce to 1 image
		return image
	def processSectionContours(tree): #===
		contours = [] # Gather all contours
		# Remove redundant contours
		return contours
	return attributes, image, contours

def processSeriesFile(tree): #===
	return
