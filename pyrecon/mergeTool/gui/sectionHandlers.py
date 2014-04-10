from PySide.QtCore import *
from PySide.QtGui import *
import pyrecon
import numpy as np

# SECTION RESOLUTION WRAPPER
class sectionWrapper(QTabWidget):
	'''sectionWrapper is a TabWidget. It contains multiple widgets that can be swapped via their tabs.'''
	def __init__(self, section1, section2, parent=None):
		QTabWidget.__init__(self)
		self.parent = parent
		self.section1 = section1
		self.section2 = section2
		self.loadObjects(section1, section2)
	def loadObjects(self, section1, section2):
		# Load widgest to be used as tabs
		self.attributes = pyrecon.mergeTool.sectionMerge.mergeAttributes(section1, section2, handler=sectionAttributes, parent=self)
		self.images = pyrecon.mergeTool.sectionMerge.mergeImages(
			section1, section2, handler=sectionImages, parent=self)
		self.contours = pyrecon.mergeTool.sectionMerge.mergeContours(section1, section2, handler=sectionContours, parent=self)
		# Add widgets as tabs
		# - Attributes
		self.addTab(self.attributes, '&Attributes')
		# - Images
		self.addTab(self.images, '&Images')
		# - Contours
		self.addTab(self.contours, '&Contours')
		# Check for lack of conflicts
		self.isResolved()
	def toObject(self):
		'''Returns a section object from the output of each resolution tab.'''
		'''Returns series object from the output of each resolution tab.'''
		# Determine attributes
		if self.attributes.output is None:
			print('Section attributes default to section 1')
			attributes = self.attributes.atts1
		else:
			attributes = self.attributes.output
		# Determine image
		if self.images.output is None:
			print('Section image default to section 1')
			image = self.images.img1
		else:
			image = self.images.output
		# Determine contours
		if self.contours.output is None:
			print('Section contours default to section 1')
			contours = self.contours.conts1
		else:
			contours = self.contours.output
		
		# Create merged section object
		return pyrecon.classes.Section(attributes,image,contours)
	def isResolved(self):
		'''Returns true if self.attributes/images/contours output attribute != None'''
		resolved = (self.attributes.output is not None and
					self.images.output is not None and
					self.contours.output is not None)
		# Check if parent is merge item and set bg to green
		if resolved and self.parent.__class__.__name__ == 'mergeItem':
			self.parent.setBackground(QColor('lightgreen'))
		return resolved
# - Attributes
class sectionAttributes(QWidget):
	def __init__(self, dictA, dictB, parent=None):
		QWidget.__init__(self, parent)
		self.parent = parent # parent different from parentWidget()
		self.atts1 = {}
		self.atts2 = {}
		self.output = None
		self.loadObjects(dictA,dictB)
		self.loadFunctions()
		self.loadLayout()
		self.checkEquiv()
	def loadObjects(self,dictA,dictB):
		# Extract relevant info to attribute dicts
		for key in ['name', 'index', 'thickness', 'alignLocked']:
			self.atts1[key] = dictA[key]
			self.atts2[key] = dictB[key]
		self.pick1 = QPushButton()
		self.pick2 = QPushButton()
		self.pick1.setText('Choose Section Attributes')
		self.pick2.setText('Choose Section Attributes')
		self.pick1.setMinimumHeight(50)
		self.pick2.setMinimumHeight(50)
		self.attLabel1 = QLabel()
		self.attLabel2 = QLabel()
		self.attLabel1.setText('\n'.join(str(key)+':\t'+str(self.atts1[key]) for key in self.atts1))
		self.attLabel2.setText('\n'.join(str(key)+':\t'+str(self.atts2[key]) for key in self.atts2))
		# Adjust font
		font = QFont("Arial", 14)
		self.attLabel1.setFont(font)
		self.attLabel2.setFont(font)
	def loadFunctions(self):
		self.pick1.clicked.connect( self.chooseAtt )
		self.pick2.clicked.connect( self.chooseAtt )
	def loadLayout(self):
		main = QHBoxLayout()
		sec1 = QVBoxLayout()
		sec2 = QVBoxLayout()
		# Add attLabels to QScrollArea
		self.scrollLabel1 = QScrollArea()
		self.scrollLabel2 = QScrollArea()
		self.scrollLabel1.setWidget(self.attLabel1)
		self.scrollLabel2.setWidget(self.attLabel2)
		# Add widgets to layout
		# sec1.addWidget(QLabel('Section 1 Attributes'))
		sec1.addWidget(self.scrollLabel1)
		sec1.addWidget(self.pick1)
		# sec2.addWidget(QLabel('Section 2 Attributes'))
		sec2.addWidget(self.scrollLabel2)
		sec2.addWidget(self.pick2)
		main.addLayout(sec1)
		main.addLayout(sec2)
		self.setLayout(main)
	def checkEquiv(self):
		if self.atts1 == self.atts2:
			self.output = self.atts1
			self.pick1.setStyleSheet('background-color:lightgreen;')
			self.pick2.setStyleSheet('background-color:lightgreen;')
			self.pick1.setText('NO CONFLICT!')
			self.pick2.setText('NO CONFLICT!')
	def chooseAtt(self):
		if self.sender() == self.pick1:
			self.output = self.atts1
			self.pick1.setStyleSheet('background-color:lightgreen;')
			self.pick2.setStyleSheet(QWidget().styleSheet())
		elif self.sender() == self.pick2:
			self.output = self.atts2
			self.pick2.setStyleSheet('background-color:lightgreen;')
			self.pick1.setStyleSheet(QWidget().styleSheet())
		self.parent.isResolved()
# - Image
class sectionImages(QWidget):
	def __init__(self, image1, image2, parent=None):
		QWidget.__init__(self, parent)
		self.parent = parent
		self.img1 = image1
		self.img2 = image2 
		self.output = None
		self.loadObjects()
		self.loadFunctions(image1,image2)
		self.loadLayout()
		self.checkEquiv()
	def loadObjects(self):
		# self.img1label = QLabel(self)
		# self.img2label = QLabel(self)
		self.pix1 = QLabel(self)
		self.pix2 = QLabel(self)
		self.img1detail = QLabel(self)
		self.img2detail = QLabel(self)
		self.pick1 = QPushButton(self)
		self.pick2 = QPushButton(self)
		self.pick1.setMinimumHeight(50)
		self.pick2.setMinimumHeight(50)
	def loadFunctions(self, image1, image2):
		# self.img1label.setText('Section A\'s Image\n'+'-'*17)
		# self.img1label.setAlignment(Qt.AlignHCenter)
		# self.img2label.setText('Section B\'s Image\n'+'-'*17)
		# self.img2label.setAlignment(Qt.AlignHCenter)
		self.img1detail.setText('\n'.join([(str(item)+':\t'+str(image1.__dict__[item])) for item in image1.__dict__ if item != 'transform']))
		self.img2detail.setText('\n'.join([(str(item)+':\t'+str(image2.__dict__[item])) for item in image2.__dict__ if item != 'transform']))
		# Load images
		pixmap1 = QPixmap(image1._path+image1.src)
		pixmap2 = QPixmap(image2._path+image2.src)
		self.pix1.setPixmap( pixmap1.scaled(500, 500, Qt.KeepAspectRatio) )
		self.pix2.setPixmap( pixmap2.scaled(500, 500, Qt.KeepAspectRatio) )
		if pixmap1.isNull():
			self.pix1.setText('Image not available.\nLikely due to incorrect path.')
		if pixmap2.isNull():
			self.pix2.setText('Image not available.\nLikely due to incorrect path.')
		# Choose image buttons
		self.pick1.setText('Choose this image')
		self.pick2.setText('Choose this image')
		self.pick1.clicked.connect( self.chooseImg )
		self.pick2.clicked.connect( self.chooseImg )
		# Adjust font/alignment
		font = QFont('Arial',pointSize=18)
		# self.img1label.setFont(font)
		# self.img2label.setFont(font)
		self.img1detail.setFont(font)
		self.img2detail.setFont(font)
		# self.img1label.setAlignment(Qt.AlignHCenter)
		# self.img2label.setAlignment(Qt.AlignHCenter)
		self.img1detail.setAlignment(Qt.AlignHCenter)
		self.img2detail.setAlignment(Qt.AlignHCenter)
		self.pix1.setFont(font)
		self.pix2.setFont(font)
		self.pix1.setAlignment(Qt.AlignHCenter)
		self.pix2.setAlignment(Qt.AlignHCenter)
	def loadLayout(self):
		self.setWindowTitle('PyRECONSTRUCT Section Image Resolver')
		hbox = QHBoxLayout()
		# Left image
		vbox1 = QVBoxLayout()
		# vbox1.addWidget(self.img1label)
		vbox1.addWidget(self.pix1)
		vbox1.addWidget(self.img1detail)
		vbox1.addWidget(self.pick1)
		# Right image
		vbox2 = QVBoxLayout()
		# vbox2.addWidget(self.img2label)
		vbox2.addWidget(self.pix2)
		vbox2.addWidget(self.img2detail)
		vbox2.addWidget(self.pick2)
		hbox.addLayout(vbox1)
		# hbox.addSpacing(50)
		hbox.addLayout(vbox2)
		self.setLayout(hbox)
	def checkEquiv(self):
		if self.img1 == self.img2:
			self.output = self.img1
			self.pick1.setStyleSheet('background-color:lightgreen;')
			self.pick2.setStyleSheet('background-color:lightgreen;')
			self.pick1.setText('NO CONFLICT!')
			self.pick2.setText('NO CONFLICT!')
	def chooseImg(self):
		if self.sender() == self.pick1:
			self.output = self.img1
			self.pick1.setStyleSheet('background-color:lightgreen;')
			self.pick2.setStyleSheet(QWidget().styleSheet())
		elif self.sender() == self.pick2:
			self.output = self.img2
			self.pick2.setStyleSheet('background-color:lightgreen;')
			self.pick1.setStyleSheet(QWidget().styleSheet())
		self.parent.isResolved()
# - Contours
class sectionContours(QWidget):
	def __init__(self, uniqueA, compOvlp, confOvlp, uniqueB, sections=None, parent=None):
		QWidget.__init__(self, parent)
		self.parent = parent
		self.setWindowTitle('PyRECONSTRUCT Section Contours Resolver')
		self.conts1 = uniqueA+[ovlp[0] for ovlp in compOvlp]+[ovlp[0] for ovlp in confOvlp]
		self.conts2 = uniqueB+[ovlp[1] for ovlp in compOvlp]+[ovlp[1] for ovlp in confOvlp]
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
		self.checkEquiv()
	def checkEquiv(self): #===
		if (self.inUniqueA.count() == 0 and
			self.inUniqueB.count() == 0 and
			self.inOvlp.count() == 0):
			# No conflicts
			self.finish(parent=False)
			self.doneBut.setText('NO CONFLICTS!')
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
		self.doneBut.setMinimumHeight(50)
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
		self.doneBut.setStyleSheet(QWidget().styleSheet())
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
		self.doneBut.setStyleSheet(QWidget().styleSheet())
		self.output = None
		self.parent.parent.clicked()
	def finish(self, parent=True):
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
		self.doneBut.setStyleSheet('background-color:lightgreen;')
		if parent:
			self.parent.isResolved()
class contourPixmap(QLabel):
	'''QLabel that contains a contour drawn on its region in an image'''
	def __init__(self, image, contour, pen=Qt.red):
		QLabel.__init__(self)
		self.image = image
		self.pixmap = QPixmap( image._path+image.src ) 
		self.contour = pyrecon.classes.Contour( contour.__dict__ ) # Create copy of contour to be altered for visualization
		self.transformToPixmap()
		self.crop()
		self.scale()
		self.drawOnPixmap(pen)
		self.setPixmap(self.pixmap)
	def transformToPixmap(self):
		'''Transforms points from RECONSTRUCT'S coordsys to PySide's coordSys'''
		# Convert biological points to pixel points
		self.contour.convertToPixCoords(self.image.mag)
		# Is Pixmap valid?
		if self.pixmap.isNull(): # If image doesnt exist...
			# Get shape from contour to determine size of background
			self.contour.popShape()
			minx,miny,maxx,maxy = self.contour.shape.bounds
			self.pixmap = QPixmap(maxx-minx+200,maxy-miny+200)
			self.pixmap.fill(fillColor=Qt.black)
		# Apply flip and translation to get points in PySide's image space
		flipVector = np.array( [1,-1] ) # Flip about x axis
		translationVector = np.array( [0,self.pixmap.size().height()] )
		transformedPoints = list(map(tuple,translationVector+(np.array(list(self.contour.shape.exterior.coords))*flipVector)))
		# Update self.contour's information to match transformation
		self.contour.points = transformedPoints
		self.contour.popShape()
	def crop(self):
		'''Crops image.'''
		# Determine crop region
		minx,miny,maxx,maxy = self.contour.shape.bounds
		x = minx-100 # minimum x and L-padding
		y = miny-100 # minimum y and L-padding
		width = maxx-x+100 # width and R-padding
		height = maxy-y+100 # width and R-padding
		# Crop pixmap to fit shape (with padding as defined above)
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
		# Prevent division by 0
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
class resolveOvlp(QDialog):
	def __init__(self, item):
		QDialog.__init__(self)
		self.setWindowTitle('Contour Overlap Resolution')
		self.item = item
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
		self.exec_()
	def loadObjects(self):
		# Buttons to choose contours
		self.cont1But = QPushButton('Choose Contour A')
		self.cont2But = QPushButton('Choose Contour B')
		self.bothContBut = QPushButton('Choose Both Contours')
		self.chooseButs = [self.cont1But,self.cont2But,self.bothContBut]
		for but in self.chooseButs:
			but.setMinimumHeight(50)
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
	def forceResolution(self, integer):
		if int(integer) == 1:
			self.contour = self.contour1
		elif int(integer) == 2:
			self.contour = self.contour2
		elif int(integer) == 3:
			self.contour = [self.contour1, self.contour2]
		else:
			print ('Invalid entry')
			return
		self.setBackground(QColor('lightgreen'))

