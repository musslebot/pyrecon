from PySide.QtCore import *
from PySide.QtGui import *
import pyrecon

class sectionWrapper(QTabWidget):
	'''sectionWrapper is a TabWidget. It contains multiple widgets that can be swapped via their tabs.'''
	def __init__(self, section1, section2, parent=None):
		QTabWidget.__init__(self, parent)
		self.section1 = section1
		self.section2 = section2
		self.loadObjects(section1, section2)
	def loadObjects(self, section1, section2):
		# Load widgest to be used as tabs
		self.attributes = pyrecon.mergeTool.sectionMerge.mergeAttributes(section1, section2, handler=sectionAttributes)
		self.images = pyrecon.mergeTool.sectionMerge.mergeImages(
			section1, section2, handler=sectionImages)
		self.contours = pyrecon.mergeTool.sectionMerge.mergeContours(section1, section2, handler=sectionContours)
		# Add widgets as tabs
		self.addTab(self.attributes, '&Attributes')
		self.addTab(self.images, '&Images')
		self.addTab(self.contours, '&Contours')
	def toObject(self):
		'''Returns a section object from the output of each resolution tab.'''
		try:#===
			mergeSection = pyrecon.classes.Section(self.attributes.output,
				self.images.output,
				self.contours.output)
			return mergeSection
		except:
			print 'Could not output to Section object :('


# - Attributes
class sectionAttributes(QWidget):
	def __init__(self, dictA, dictB):
		QWidget.__init__(self)
		self.atts1 = dictA
		self.atts2 = dictB
		self.output = None
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self):
		self.attList = QListWidget()
		for key in ['name','index','thickness','alignLocked']:
			item = QListWidgetItem()
			item.setText(str(key))
			if self.atts1[key] != self.atts2[key]:
				item.setBackground(QColor('red'))
			self.attList.addItem(item)
	def loadFunctions(self):
		self.attList.itemDoubleClicked.connect( self.resItem )
	def loadLayout(self):
		vbox = QVBoxLayout()
		vbox.addWidget(self.attList)
		self.setLayout(vbox)
	def resItem(self, item):
		print('ITEM CLICKED')
# class resolveAttribute(Q)
# - Image
class sectionImages(QWidget):
	def __init__(self, image1, image2):
		QWidget.__init__(self)
		self.loadObjects()
		self.loadFunctions(image1,image2)
		self.loadLayout()
		self.img1 = image1
		self.img2 = image2 
		self.output = None
	def loadObjects(self):
		self.img1label = QLabel(self)
		self.img2label = QLabel(self)
		self.pix1 = QLabel(self)
		self.pix2 = QLabel(self)
		self.img1detail = QLabel(self)
		self.img2detail = QLabel(self)
		self.pick1 = QPushButton(self)
		self.pick2 = QPushButton(self)
	def loadFunctions(self, image1, image2):
		self.img1label.setText('Section A\'s Image\n'+'-'*17)
		self.img1label.setAlignment(Qt.AlignHCenter)
		self.img2label.setText('Section B\'s Image\n'+'-'*17)
		self.img2label.setAlignment(Qt.AlignHCenter)
		self.img1detail.setText('\n'.join([(str(item)+':\t'+str(image1.__dict__[item])) for item in image1.__dict__ if item != 'transform']))
		self.img2detail.setText('\n'.join([(str(item)+':\t'+str(image2.__dict__[item])) for item in image2.__dict__ if item != 'transform']))
		pixmap1 = QPixmap(image1._path+image1.src)
		pixmap2 = QPixmap(image2._path+image2.src)
		self.pix1.setPixmap( pixmap1.scaled(500, 500, Qt.KeepAspectRatio) )
		self.pix2.setPixmap( pixmap2.scaled(500, 500, Qt.KeepAspectRatio) )
		if pixmap1.isNull():
			self.pix1.setText('Image not available.')
			self.pix1.setAlignment(Qt.AlignHCenter)
		if pixmap2.isNull():
			self.pix2.setText('Image not available.')
			self.pix2.setAlignment(Qt.AlignHCenter)
		self.pick1.setText('Choose this image')
		self.pick2.setText('Choose this image')
		self.pick1.clicked.connect( self.ret1 )
		self.pick2.clicked.connect( self.ret2 )
	def loadLayout(self):
		self.setWindowTitle('PyRECONSTRUCT Section Image Resolver')
		hbox = QHBoxLayout()
		# Left image
		vbox1 = QVBoxLayout()
		vbox1.addWidget(self.img1label)
		vbox1.addWidget(self.pix1)
		vbox1.addWidget(self.img1detail)
		vbox1.addWidget(self.pick1)
		# Right image
		vbox2 = QVBoxLayout()
		vbox2.addWidget(self.img2label)
		vbox2.addWidget(self.pix2)
		vbox2.addWidget(self.img2detail)
		vbox2.addWidget(self.pick2)
		hbox.addLayout(vbox1)
		hbox.addSpacing(50)
		hbox.addLayout(vbox2)
		self.setLayout(hbox)
	def ret1(self):
		self.output = self.img1
		self.pick1.setBackground(QColor('lightgreen'))
		self.pick2.setBackground(QColor('red'))
	def ret2(self):
		self.output = self.img2
		self.pick2.setBackground(QColor('lightgreen'))
		self.pick1.setBackground(QColor('red'))
# - Contours
class contourPixmap(QLabel):
	'''QLabel that contains a contour drawn on its region in an image'''
	def __init__(self, image, contour, pen=Qt.red):
		QLabel.__init__(self)
		self.image = image
		self.pixmap = QPixmap( image._path+image.src ) # Create pixmap from image info
		self.contour = Contour( contour.__dict__ ) # Create copy of contour to be altered for visualization
		self.transformToPixmap()
		self.crop()
		self.scale()
		self.drawOnPixmap(pen)
		self.setPixmap(self.pixmap)
	def transformToPixmap(self):
		'''Transforms points from RECONSTRUCT'S coordsys to PySide's coordSys'''
		self.contour.convertToPixCoords(self.image.mag) # Convert biological points to pixel points
		flipVector = np.array( [1,-1] ) # Flip about x axis
		# Is Pixmap valid? #=== probably a better way than using hardcoded values for new size
		if self.pixmap.isNull(): # If image doesnt exist...
			self.pixmap = QPixmap(2000,1000) # Make new 2000x1000 pixmap with white background
			self.pixmap.fill(fillColor=Qt.white)
		translationVector = np.array( [0,self.pixmap.size().height()] )
		# Apply flip and translation to get points in PySide's image space
		# 	transformedPts = (oldPts*flipVector)+translationVector
		transformedPoints = list(map(tuple,translationVector+(np.array(list(self.contour.shape.exterior.coords))*flipVector)))
		# Update self.contour's information to match transformation
		self.contour.points = transformedPoints
		self.contour.popShape()
	def crop(self):
		'''Crops image.'''
		# Determine crop region
		x = self.contour.shape.bounds[0]-100
		y = self.contour.shape.bounds[1]-100
		width = self.contour.shape.bounds[2]-x+100
		height = self.contour.shape.bounds[3]-y+100
		# Crop image to defined rectangle
		self.pixmap = self.pixmap.copy(x,y,width,height)
		# Adjust points to crop region
		cropVector = np.array( [x,y] )
		croppedPoints = list(map(tuple, np.array(self.contour.points)-cropVector ))
		self.contour.points = croppedPoints
		self.contour.popShape()
	def scale(self):
		# Scale image
		preCropSize = self.pixmap.size()
		self.pixmap = self.pixmap.copy().scaled( 500, 500, Qt.KeepAspectRatio ) #=== is copy necessary?
		# Scale points
		preWidth = float(preCropSize.width())
		preHeight = float(preCropSize.height())
		# Prevent division by 0.0
		if preWidth == 0.0 or preHeight == 0.0:
			preWidth = 1.0
			preHeight = 1.0
		wScale = self.pixmap.size().width()/preWidth
		hScale = self.pixmap.size().height()/preHeight
		scale = np.array([wScale,hScale])
		scaledPoints = list(map(tuple,np.array(self.contour.points)*scale))
		self.contour.points = scaledPoints
		self.contour.popShape()
	def drawOnPixmap(self, pen=Qt.red):
		# Create polygon to draw
		polygon = QPolygon()
		for point in self.contour.points:
			polygon.append( QPoint(*point) )
		# Draw polygon on pixmap
		painter = QPainter()
		painter.begin(self.pixmap)
		painter.setPen(pen)
		painter.drawConvexPolygon(polygon)
class resolveOvlp(QWidget):
	def __init__(self, item):
		QWidget.__init__(self)
		self.setWindowTitle('Contour Overlap Resolution')
		self.item = item
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self):
		# Buttons to choose contours
		self.cont1But = QPushButton('Choose Contour 1')
		self.cont2But = QPushButton('Choose Contour 2')
		self.bothContBut = QPushButton('Choose Both Contours')
		# Labels to hold pixmap
		self.pix1 = None
		self.pix2 = None
	def loadFunctions(self):
		self.cont1But.clicked.connect( self.finish )
		self.cont2But.clicked.connect( self.finish )
		self.bothContBut.clicked.connect( self.finish )
		self.pix1 = contourPixmap(self.item.image1, self.item.contour1)
		self.pix2 = contourPixmap(self.item.image2, self.item.contour2, pen=Qt.cyan)
	def loadLayout(self):
		container = QVBoxLayout() # Contains everything
		# - Contains Images
		imageContainer = QHBoxLayout()
		imageContainer.addWidget(self.pix1)
		imageContainer.addWidget(self.pix2)
		# - Contains buttons
		butBox = QHBoxLayout()
		butBox.addWidget(self.cont1But)
		butBox.addWidget(self.cont2But)
		# Add other containers to container
		container.addLayout(imageContainer)
		container.addLayout(butBox)
		container.addWidget(self.bothContBut)
		self.setLayout(container)
	def finish(self): # Return int associated with selected contour
		if self.sender() == self.cont1But:
			self.done(1)
		elif self.sender() == self.cont2But:
			self.done(2)
		elif self.sender() == self.bothContBut:
			self.done(3)
class contourTableItem(QListWidgetItem):
	'''This class has the functionality of a QListWidgetItem while also being able to store a pointer to the contour(s) it represents.'''
	def __init__(self, contour, images):
		QListWidgetItem.__init__(self)
		if type(contour) == type([]):
			self.contour = None
			self.contour1 = contour[0]
			self.contour2 = contour[1]
			if type(images) == type([]):
				self.image1 = images[0]
				self.image2 = images[1]
			self.setText(self.contour1.name)
		else:
			self.contour = contour
			self.setText(contour.name)
	def clicked(self):
		item = self
		msg = resolveOvlp(item)
		resolution = msg.result() # msg returns an int referring to the selected contour
		if resolution == 1:
			self.contour = self.contour1
			self.setBackground(QColor('lightgreen'))
		elif resolution == 2:
			self.contour = self.contour2
			self.setBackground(QColor('lightgreen'))
		elif resolution == 3:
			self.contour = [self.contour1, self.contour2]
			self.setBackground(QColor('lightgreen'))
class sectionContours(QWidget):
	def __init__(self, uniqueA, compOvlp, confOvlp, uniqueB, sections=None):
		QWidget.__init__(self)
		self.setWindowTitle('PyRECONSTRUCT Section Contours Resolver')
		# input
		self.uniqueA = uniqueA
		self.uniqueB = uniqueB
		self.compOvlp = compOvlp
		self.confOvlp = confOvlp
		if sections != None:
			self.sections = sections
			self.s1name = sections[0].name
			self.s2name = sections[1].name
		# output
		self.output = None
		# Load UI
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self):
		# List contours in their appropriate listWidgets
		self.inUniqueA = QListWidget(self)
		self.inUniqueB = QListWidget(self)
		self.inOvlp = QListWidget(self)
		self.outUniqueA = QListWidget(self)
		self.outUniqueB = QListWidget(self)
		self.outOvlp = QListWidget(self)
		self.doneBut = QPushButton(self) # Merge button
		self.moveSelectedA = QPushButton(self)
		self.moveSelectedO = QPushButton(self)
		self.moveSelectedB = QPushButton(self)
	def loadFunctions(self):
		# Load tables with contour objects
		self.loadTable(self.inUniqueA, self.uniqueA)
		self.loadTable(self.inUniqueB, self.uniqueB)
		self.loadTable(self.inOvlp, self.compOvlp+self.confOvlp)
		for table in [self.inUniqueA, self.inUniqueB, self.inOvlp, self.outUniqueA, self.outUniqueB, self.outOvlp]:
			table.setSelectionMode(QAbstractItemView.ExtendedSelection)
			table.itemDoubleClicked.connect(self.doubleClickCheck)
		self.doneBut.setText('Merge')
		self.doneBut.clicked.connect( self.finish )
		self.moveSelectedA.setText('Move Selected')
		self.moveSelectedO.setText('Move Selected')
		self.moveSelectedB.setText('Move Selected')
		self.moveSelectedA.clicked.connect( self.moveItems )
		self.moveSelectedO.clicked.connect( self.moveItems )
		self.moveSelectedB.clicked.connect( self.moveItems )
	def loadLayout(self):
		container = QVBoxLayout()
		secNameContainer = QHBoxLayout()
		secNameContainer.setAlignment(Qt.AlignHCenter)
		secNameContainer.addWidget(QLabel(str(self.s1name)+' vs. '+str(self.s2name)))
		columnContainer = QHBoxLayout()
		
		labelContainer = QVBoxLayout()
		labelContainer.addWidget(QLabel('Input'))
		labelContainer.addWidget(QLabel('Output'))
		columnContainer.addLayout(labelContainer)

		uniqueAColumn = QVBoxLayout()
		uniqueALabel = QLabel('Section A\'s Unique Contours')
		uniqueAColumn.addWidget(uniqueALabel)
		uniqueAColumn.addWidget(self.inUniqueA)
		uniqueAColumn.addWidget(self.moveSelectedA)
		uniqueAColumn.addWidget(self.outUniqueA)
		columnContainer.addLayout(uniqueAColumn)

		overlapColumn = QVBoxLayout()
		overlapLabel = QLabel('Overlapping Contours')
		overlapColumn.addWidget(overlapLabel)
		overlapColumn.addWidget(self.inOvlp)
		overlapColumn.addWidget(self.moveSelectedO)
		overlapColumn.addWidget(self.outOvlp)
		columnContainer.addLayout(overlapColumn)

		uniqueBColumn = QVBoxLayout()
		uniqueBLabel = QLabel('Section B\'s Unique Contours')
		uniqueBColumn.addWidget(uniqueBLabel)
		uniqueBColumn.addWidget(self.inUniqueB)
		uniqueBColumn.addWidget(self.moveSelectedB)
		uniqueBColumn.addWidget(self.outUniqueB)
		columnContainer.addLayout(uniqueBColumn)

		container.addLayout(secNameContainer)
		container.addLayout(columnContainer)
		container.addWidget(self.doneBut)
		self.setLayout(container)
	def loadTable(self, table, items):
		'''Load <table> with <items>'''
		for item in items:
			if item.__class__.__name__ == 'Contour' or type(item) == type([]):
				# Item can be a contour or list of 2 contours, they are handled differently in contourTableItem class upon initialization
				listItem = contourTableItem(item, [self.sections[0].image,self.sections[1].image])
				if type(item) == type([]):
					if item in self.confOvlp: # Conflicting ovlping contour
						listItem.setBackground(QColor('red'))
					elif item in self.compOvlp: # Completely ovlping contour
						listItem.contour = listItem.contour1 # set chosen contour to cont1 since they're the same
						self.outOvlp.addItem(listItem)
						continue
				table.addItem(listItem)
			else:
				print 'Invalid item for contourListWidget'
	def doubleClickCheck(self, item):
		if item.background() == QColor('red') or item.background() == QColor('lightgreen'):
			item.clicked() # See contourTableItem class
	def moveItems(self):
		# Move items in what table(s)?
		if self.sender() == self.moveSelectedA:
			inTable = self.inUniqueA
			outTable = self.outUniqueA
		elif self.sender() == self.moveSelectedO:
			inTable = self.inOvlp
			outTable = self.outOvlp
		elif self.sender() == self.moveSelectedB:
			inTable = self.inUniqueB
			outTable = self.outUniqueB
		# Now move items
		selectedIn = inTable.selectedItems()
		selectedOut = outTable.selectedItems()
		for item in selectedIn:
			outTable.addItem( inTable.takeItem(inTable.row(item)) )
		for item in selectedOut:
			inTable.addItem( outTable.takeItem(outTable.row(item)) )
		inTable.clearSelection()
		outTable.clearSelection()
	def finish(self):
		# Check ovlp table for unresolved conflicts (red)
		numItems = self.outOvlp.count()
		for i in range(numItems):
			item = self.outOvlp.item(i)
			if item.background() == QColor('red'):
				msg = QMessageBox(self)
				msg.setText('Conflict not resolved. Abort merge...')
				msg.exec_()
				return
		# Gather items from tables
		oA = [] # Unique A
		for i in range(self.outUniqueA.count()):
			oA.append(self.outUniqueA.item(i))
		oO = [] # Overlap
		for i in range(self.outOvlp.count()):
			oO.append(self.outOvlp.item(i))
		oB = [] # Unique B
		for i in range(self.outUniqueB.count()):
			oB.append(self.outUniqueB.item(i))
		# Check for domain1
		if ('domain1' not in [item.contour1.name for item in oO] and
		'domain1' not in [item.contour.name for item in oA] and
		'domain1' not in [item.contour.name for item in oB]):
			msg = QMessageBox(self)
			msg.setText('"domain1" was not found in any output column. The "domain1" contour is essential for correctly mapping contours to their place on the image. Merge aborted.')
			msg.exec_()
			return
		# set self.output to chosen contours
		self.output = [item.contour for item in oA]+[item.contour for item in oB]
		for item in oO:
			if type(item.contour) == type([]): # if both contours chosen in resolution
				self.output.extend(item.contour)
			else:
				self.output.append(item.contour)
		self.close()