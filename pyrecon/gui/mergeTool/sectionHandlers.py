from PySide.QtCore import *
from PySide.QtGui import *
import pyrecon
import numpy as np

# SECTION CONFLICT RESOLUTION GUI WRAPPER
class SectionMergeWrapper(QTabWidget):
	'''sectionWrapper is a TabWidget. It contains multiple widgets that can be swapped via their tabs.'''
	def __init__(self, MergeSection):
		QTabWidget.__init__(self)
		self.merge = MergeSection
		self.loadObjects()
	def loadObjects(self):
		# Load widgest to be used as tabs
		self.attributes = SectionAttributeHandler(self.merge)
		self.images = SectionImageHandler(self.merge)
		self.contours = SectionContourHandler(self.merge)
		# Add widgets as tabs
		self.addTab(self.attributes, '&Attributes')
		self.addTab(self.images, '&Images')
		self.addTab(self.contours, '&Contours')
	def doneCount(self):
		return self.merge.doneCount()
# - Attributes
class SectionAttributeHandler(QWidget):
	def __init__(self, MergeSection):
		QWidget.__init__(self)
		self.merge = MergeSection # MergeSection
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
		self.checkEquivalency()
	def checkEquivalency(self):
		'''Checks to see if the MergeSections' checkConflicts() function automatically handled this. SHOULD ONLY BE RUN IN INIT'''
		if self.merge.attributes is not None:
			txt = 'Attributes are equivalent, no conflict.'
			self.chooseLeft.setText(txt)
			self.chooseRight.setText(txt)
			self.chooseLeft.setStyleSheet('background-color:lightgreen;')
			self.chooseRight.setStyleSheet('background-color:lightgreen;')
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
		self.checkEquivalency()
	def checkEquivalency(self):
		'''Checks to see if the MergeSections' checkConflicts() function automatically handled this. SHOULD ONLY BE RUN IN INIT'''
		if self.merge.images is not None:
			txt = 'Images are equivalent, no conflict.'
			self.chooseLeft.setText(txt)
			self.chooseRight.setText(txt)
			self.chooseLeft.setStyleSheet('background-color:lightgreen;')
			self.chooseRight.setStyleSheet('background-color:lightgreen;')
	def loadObjects(self):
		# Pixmaps
		self.pixmap1 = QPixmap(self.merge.section1.image._path+self.merge.section1.image.src).scaled(750,750,aspectMode=Qt.KeepAspectRatio)
		self.pixmap2 = QPixmap(self.merge.section2.image._path+self.merge.section2.image.src).scaled(750,750,aspectMode=Qt.KeepAspectRatio)
		if self.pixmap1.isNull() and not self.pixmap2.isNull():
			self.pixmap1 = QPixmap(self.pixmap2.size().width(),self.pixmap2.size().height()) # empty pixmap, size to pixmap2
		if self.pixmap2.isNull() and not self.pixmap1.isNull():
			self.pixmap2 = QPixmap(self.pixmap1.size().width(),self.pixmap1.size().height()) # empty pixmap, size to pixmap1
		#=== change fill color (def: black) -- looks too similar to normal
		if self.pixmap1.isNull() and self.pixmap2.isNull():
			self.pixmap1 = QPixmap(750,750)
			self.pixmap2 = QPixmap(750,750)
		# - Pixmaps must be placed in a QLabel
		self.imgLabel1 = QLabel()
		self.imgLabel1.setPixmap( self.pixmap1 )
		self.imgLabel2 = QLabel()
		self.imgLabel2.setPixmap( self.pixmap2 )
		# Image details
		img1atts = self.merge.section1.image.attributes()
		img2atts = self.merge.section2.image.attributes()
		self.details1 = QLabel('\n'.join([str(att).upper()+':\t'+str(img1atts[att]) for att in img1atts]))
		self.details2 = QLabel('\n'.join([str(att).upper()+':\t'+str(img2atts[att]) for att in img2atts]))
		font = QFont("Arial", 14)
		self.details1.setFont(font)
		self.details2.setFont(font)
		self.details1.setWordWrap(True)
		self.details2.setWordWrap(True)
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
		# Section A's half
		leftHalf = QVBoxLayout()
		leftScrollArea = QScrollArea() # QLabels containing the pixmaps should be placed in QScrollArea, to prevent the image from taking entire screen
		leftScrollArea.setWidget(self.imgLabel1)
		leftHalf.addWidget(leftScrollArea)
		leftHalf.addWidget(self.details1)
		leftHalf.addWidget(self.chooseLeft)

		# Section B's half
		rightHalf = QVBoxLayout()
		rightScrollArea = QScrollArea()
		rightScrollArea.setWidget(self.imgLabel2)
		rightHalf.addWidget(rightScrollArea)
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
# - Contours
class SectionContourHandler(QWidget):
	def __init__(self, MergeSection):
		QWidget.__init__(self)
		self.merge = MergeSection
		# Contours
		# - Unique contours from each section
		self.uniqueA, self.uniqueB = self.merge.uniqueA, self.merge.uniqueB
		# - Complete overlap, and conflicting overlap contours
		self.compOvlp, self.confOvlp = self.merge.compOvlps, self.merge.confOvlps
		# Load UI
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
		self.checkEquivalency()
	def checkEquivalency(self):
		'''Checks to see if the MergeSections' checkConflicts() function automatically handled this. SHOULD ONLY BE RUN IN INIT'''
		if self.merge.contours is not None:
			txt = 'Contours are equivalent, no conflict.'
			self.doneBut.setText(txt)
			self.doneBut.setStyleSheet('background-color:lightgreen;')
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
		self.doneBut.setText('Save Current Status')
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
		secNameContainer.addWidget(QLabel(str(self.merge.section1.name)+' vs. '+str(self.merge.section2.name)))
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
				listItem = contourTableItem(item, [self.merge.section1.image,self.merge.section2.image])
				if type(item) == type([]):
					if item in self.confOvlp: # Conflicting ovlping contour
						listItem.setBackground(QColor('red'))
					elif item in self.compOvlp: # Completely ovlping contour
						listItem.contour = listItem.contour1 #=== set chosen contour to cont1 since they're the same
						listItem.setBackground(QColor('lightgreen'))
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
		# Move items in which table(s)?
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
		self.doneBut.setStyleSheet(QWidget().styleSheet()) # Button not green, indicates lack of save
		self.merge.contours = None # Reset MergeSection.contours
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
		output = [item.contour for item in oA]+[item.contour for item in oB]
		for item in oO:
			if type(item.contour) == type([]): # if both contours chosen in resolution
				output.extend(item.contour)
			else:
				output.append(item.contour)
		self.merge.contours = output
		self.doneBut.setStyleSheet('background-color:lightgreen;') # Button to green
	# Quick merge functions
	def onlyAContours(self): #===
		self.allUniqueA()
		self.noUniqueB()
		# move all ovlps to outOvlps
		for i in range(self.inOvlp.count()):
			self.inOvlp.item(i).setSelected(True)
		self.moveSelectedO.click()
		# Select A versions for ovlps
		for i in range(self.outOvlp.count()):
			self.outOvlp.item(i).forceResolution(1)
		self.doneBut.click()
	def onlyBContours(self): #===
		self.allUniqueB()
		self.noUniqueA()
		# move all ovlps to outOvlps
		for i in range(self.inOvlp.count()):
			self.inOvlp.item(i).setSelected(True)
		self.moveSelectedO.click()
		# Select A versions for ovlps
		for i in range(self.outOvlp.count()):
			self.outOvlp.item(i).forceResolution(2)
		self.doneBut.click()
	def allContours(self): #===
		'''choose both contours for all conflicts and move everything to output'''
		self.allUniqueA()
		self.allUniqueB()
		self.allOvlps()
		self.doneBut.click()
	def allOvlps(self):
		'''Select both versions of all overlaps and move to output'''
		for i in range(self.inOvlp.count()):
			self.inOvlp.item(i).setSelected(True)
		self.moveSelectedO.click()
		for i in range(self.outOvlp.count()):
			self.outOvlp.item(i).forceResolution(3)
	def allUniqueA(self):
		'''moves all unique A contours to output'''
		for i in range(self.inUniqueA.count()):
			self.inUniqueA.item(i).setSelected(True)
		self.moveSelectedA.click()
	def allUniqueB(self):
		'''moves all unique B contours to output'''
		for i in range(self.inUniqueB.count()):
			self.inUniqueB.item(i).setSelected(True)
		self.moveSelectedB.click()
	def noUniqueA(self):
		'''returns all outUniqueA items to inUniqueA'''
		for i in range(self.outUniqueA.count()):
			self.outUniqueA.item(i).setSelected(True)
		self.moveSelectedA.click()
	def noUniqueB(self):
		'''returns all outUniqueB items to inUniqueB'''
		for i in range(self.outUniqueB.count()):
			self.outUniqueB.item(i).setSelected(True)
		self.moveSelectedB.click()

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
		if type(contour) == type([]): # Overlapping contours are in pairs
			self.contour = None
			self.contour1 = contour[0]
			self.contour2 = contour[1]
			if type(images) == type([]): # Images for conflict resolution
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