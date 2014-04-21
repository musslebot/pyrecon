from PySide.QtCore import *
from PySide.QtGui import *
import pyrecon
import numpy as np

# SECTION RESOLUTION WRAPPER
# class sectionWrapper(QTabWidget):
# 	'''sectionWrapper is a TabWidget. It contains multiple widgets that can be swapped via their tabs.'''
# 	def __init__(self, MergeSection=None, parent=None):
# 		QTabWidget.__init__(self)
# 		self.parent = parent
# 		self.merge = MergeSection
# 		self.loadObjects(MergeSection.section1, MergeSection.section2)
# 	def loadObjects(self, section1, section2):
# 		# Load widgest to be used as tabs
# 		self.attributes = self.merge.mergeAttributes()
# 		self.images = self.merge.mergeImages()
# 		self.contours = self.merge.mergeContours()
# 		# Add widgets as tabs
# 		# - Attributes
# 		self.addTab(self.attributes, '&Attributes')
# 		# - Images
# 		self.addTab(self.images, '&Images')
# 		# - Contours
# 		self.addTab(self.contours, '&Contours')
# 		# Check for lack of conflicts
# 		self.isResolved()
# 	def toObject(self):
# 		'''Returns a section object from the output of each resolution tab.'''
# 		'''Returns series object from the output of each resolution tab.'''
# 		# Determine attributes
# 		if self.attributes.output is None:
# 			print('Section attributes default to section 1')
# 			attributes = self.attributes.atts1
# 		else:
# 			attributes = self.attributes.output
# 		# Determine image
# 		if self.images.output is None:
# 			print('Section image default to section 1')
# 			image = self.images.img1
# 		else:
# 			image = self.images.output
# 		# Determine contours
# 		if self.contours.output is None:
# 			print('Section contours default to section 1')
# 			contours = self.contours.conts1
# 		else:
# 			contours = self.contours.output
		
# 		# Create merged section object
# 		return pyrecon.classes.Section(attributes,image,contours)
# 	def isResolved(self):
# 		'''Returns true if self.attributes/images/contours output attribute != None'''
# 		resolved = (self.attributes.output is not None and
# 					self.images.output is not None and
# 					self.contours.output is not None)
# 		# Check if parent is merge item and set bg to green
# 		if resolved and self.parent.__class__.__name__ == 'mergeItem':
# 			self.parent.setBackground(QColor('lightgreen'))
# 		return resolved
# - Attributes
class SectionAttributeHandler(QWidget):
	def __init__(self, mergeObject):
		QWidget.__init__(self)
		self.merge = mergeObject # MergeSection
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self):
		# Buttons to resolve conflict
		self.chooseLeft = QPushButton('Choose These Attributes')
		self.chooseRight = QPushButton('Choose These Attributes')
		# - Button looks
		self.chooseLeft.setMinimumHeight(50)
		self.chooseRight.setMinimumHeight(50)
		# Labels for displaying attributes
		self.leftLabel = QLabel()
		self.rightLabel = QLabel()
		# - Load text into labels
		self.leftLabel.setText('\n'.join(str(key)+':\t'+str(self.merge.section1.attributes()[key]) for key in self.merge.section1.attributes()))
		self.rightLabel.setText('\n'.join(str(key)+':\t'+str(self.merge.section2.attributes()[key]) for key in self.merge.section2.attributes()))
		# - Adjust font
		font = QFont("Arial", 14)
		self.leftLabel.setFont(font)
		self.rightLabel.setFont(font)
	def loadFunctions(self):
		# Button functions
		self.chooseLeft.clicked.connect( self.choose )
		self.chooseRight.clicked.connect( self.choose )
	def loadLayout(self):
		container = QHBoxLayout()
		# Left half (section1)
		leftHalf = QVBoxLayout()
		leftHalf.addWidget( self.leftLabel )
		leftHalf.addWidget( self.chooseLeft )
		# Right half (section2)
		rightHalf = QVBoxLayout()
		rightHalf.addWidget( self.rightLabel )
		rightHalf.addWidget( self.chooseRight )
		# Add halves to container
		container.addLayout( leftHalf )
		container.addLayout( rightHalf )
		self.setLayout( container ) 
	def choose(self):
		if self.sender() == self.chooseLeft:
			self.merge.attributes = self.merge.section1.attributes()
			self.chooseLeft.setStyleSheet('background-color:lightgreen;')
			self.chooseRight.setStyleSheet(QWidget().styleSheet())
		elif self.sender() == self.chooseRight:
			self.merge.attributes = self.merge.section2.attributes()
			self.chooseLeft.setStyleSheet(QWidget().styleSheet())
			self.chooseRight.setStyleSheet('background-color:lightgreen;')
# - Images
class SectionImageHandler(QWidget):
	def __init__(self, MergeSection):
		QWidget.__init__(self)
		self.merge = MergeSection
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self):
		# Pixmaps
		self.pixmap1 = QPixmap(self.merge.section1.image._path+self.merge.section1.image.src)
		self.pixmap2 = QPixmap(self.merge.section2.image._path+self.merge.section2.image.src)
		# - Pixmaps must be displayed in QLabel
		self.imgLabel1 = QLabel()
		self.imgLabel1.setPixmap( self.pixmap1 )
		self.imgLabel2 = QLabel()
		self.imgLabel2.setPixmap( self.pixmap2 )
		# Image details
		self.details1 = QLabel()
		self.details2 = QLabel()
		# Buttons to resolve conflicts
		self.chooseLeft = QPushButton('Choose This Image')
		self.chooseLeft.setMinimumHeight(50)
		self.chooseRight = QPushButton('Choose This Image')
		self.chooseRight.setMinimumHeight(50)
	def loadFunctions(self):
		self.chooseLeft.clicked.connect( self.choose )
		self.chooseRight.clicked.connect( self.choose )
	def loadLayout(self):
		container = QHBoxLayout()
		
		leftHalf = QVBoxLayout()
		imageLabel1 = QLabel()
		if self.pixmap1.isNull():
			self.imgLabel1.setText('Image 1 not available.')
			scrollableImage1 = self.imgLabel1
		else:
			imageLabel1.setPixmap(self.pixmap1)
			scrollableImage1 = QScrollArea()
			scrollableImage1.setWidget(imageLabel1)
		leftHalf.addWidget(scrollableImage1)
		leftHalf.addWidget(self.details1)
		leftHalf.addWidget(self.chooseLeft)
		
		rightHalf = QVBoxLayout()
		imageLabel2 = QLabel()
		if self.pixmap2.isNull():
			self.imgLabel2.setText('Image 2 not available.') #=== set a size
			scrollableImage2 = self.imgLabel2
		else:
			imageLabel2.setPixmap(self.pixmap2)
			scrollableImage2 = QScrollArea()
			scrollableImage2.setWidget(imageLabel2)
		rightHalf.addWidget(scrollableImage2)
		rightHalf.addWidget(self.details2)
		rightHalf.addWidget(self.chooseRight)
		
		container.addLayout(leftHalf)
		container.addLayout(rightHalf)
		self.setLayout(container)
	def choose(self):
		if self.sender() == self.chooseLeft:
			self.merge.images = self.merge.section1.image
			self.chooseLeft.setStyleSheet('background-color:lightgreen;')
			self.chooseRight.setStyleSheet(QWidget().styleSheet())
		elif self.sender() == self.chooseRight:
			self.merge.images = self.merge.section2.image
			self.chooseLeft.setStyleSheet(QWidget().styleSheet())
			self.chooseRight.setStyleSheet('background-color:lightgreen;')

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
		self.pix1 = QLabel(self)
		self.pix2 = QLabel(self)
		self.img1detail = QLabel(self)
		self.img2detail = QLabel(self)
		self.pick1 = QPushButton(self)
		self.pick2 = QPushButton(self)
		self.pick1.setMinimumHeight(50)
		self.pick2.setMinimumHeight(50)
	def loadFunctions(self, image1, image2):
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
		self.img1detail.setFont(font)
		self.img2detail.setFont(font)
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
		'''Check if images are equal. If so, automerge'''
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
	def checkEquiv(self):
		'''Check if there are any unique contours. If not, call finish()'''
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

