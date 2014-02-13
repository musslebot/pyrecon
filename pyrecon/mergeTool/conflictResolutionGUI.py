'''Graphical handler functions for mergeTool conflicts'''
from PySide.QtCore import *
from PySide.QtGui import *
import sys

# SECTIONS
# - Image
class sectionImages(QWidget):
	def __init__(self, image1, image2):
		QWidget.__init__(self)
		self.loadObjects()
		self.loadFunctions(image1,image2)
		self.loadLayout()
		self.image = None
		self.show()
	def loadObjects(self):
		self.img1label = QLabel(self)
		self.img2label = QLabel(self)
		self.img1detail = QLabel(self)
		self.img2detail = QLabel(self)
		self.pick1 = QPushButton(self)
		self.pick2 = QPushButton(self)
	def loadFunctions(self, image1, image2):
		self.img1 = image1
		self.img2 = image2
		self.img1label.setText('Section A\'s Image\n'+'-'*17)
		self.img1label.setAlignment(Qt.AlignHCenter)
		self.img2label.setText('Section B\'s Image\n'+'-'*17)
		self.img2label.setAlignment(Qt.AlignHCenter)
		self.img1detail.setText('\n'.join([(str(item)+':\t'+str(image1.__dict__[item])) for item in image1.__dict__ if item != 'transform']))
		self.img2detail.setText('\n'.join([(str(item)+':\t'+str(image2.__dict__[item])) for item in image2.__dict__ if item != 'transform']))
		self.pick1.setText('Choose this image')
		self.pick2.setText('Choose this image')
		self.pick1.clicked.connect( self.ret1 ) #===
		self.pick2.clicked.connect( self.ret2 ) #===
	def loadLayout(self):
		self.setWindowTitle('PyRECONSTRUCT Section Image Resolver')
		hbox = QHBoxLayout()
		# Left image
		vbox1 = QVBoxLayout()
		vbox1.addWidget(self.img1label)
		vbox1.addWidget(self.img1detail)
		vbox1.addWidget(self.pick1)
		# Right image
		vbox2 = QVBoxLayout()
		vbox2.addWidget(self.img2label)
		vbox2.addWidget(self.img2detail)
		vbox2.addWidget(self.pick2)
		hbox.addLayout(vbox1)
		hbox.addSpacing(50)
		hbox.addLayout(vbox2)
		self.setLayout(hbox)
	def ret1(self): #===
		self.image = self.img1

	def ret2(self): #===
		self.image = self.img2
# - Contours
class resolveOvlp(QWidget): #=== Not showing?
	def __init__(self, item):
		QWidget.__init__(self)
		print 'cont1: '+str(item.contour1.name)
		print 'cont2: '+str(item.contour2.name)
		layout = QHBoxLayout()
		layout.addWidget(QLabel(item.contour1.name))
		layout.addWidget(QLabel(item.contour2.name))
		self.setLayout(layout)
		# self.show()
class sectionContours(QWidget): #===
	class contourTableItem(QListWidgetItem):
		'''This class has the functionality of a QListWidgetItem while also being able to store a pointer to the contour(s) it represents.'''
		def __init__(self, contour):
			QListWidgetItem.__init__(self)
			if type(contour) == type([]):
				self.contour = None
				self.contour1 = contour[0]
				self.contour2 = contour[1]
				self.setText(self.contour1.name)
				self.setStatusTip( str(self.contour1) )
			else:
				self.contour = contour
				self.setText(contour.name)
		def clicked(self):
			a = resolveOvlp(self)
			print('Resolve item')
			a.show()
	def __init__(self, uniqueA, compOvlp, confOvlp, uniqueB):
		QWidget.__init__(self)
		self.setWindowTitle('PyRECONSTRUCT Section Contours Resolver')
		# input
		self.uniqueA = uniqueA
		self.uniqueB = uniqueB
		self.compOvlp = compOvlp
		self.confOvlp = confOvlp
		# output
		self.output = []
		# Load UI
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
		self.show()
	def loadObjects(self):
		# List contours in their appropriate listWidgets
		self.inUniqueA = QListWidget(self)
		self.inUniqueB = QListWidget(self)
		self.inOvlp = QListWidget(self)
		self.outUniqueA = QListWidget(self)
		self.outUniqueB = QListWidget(self)
		self.outOvlp = QListWidget(self)
		self.doneBut = QPushButton(self)
		self.moveSelectedA = QPushButton(self)
		self.moveSelectedO = QPushButton(self)
		self.moveSelectedB = QPushButton(self)
	def loadFunctions(self):
		# Load tables with contour objects
		self.loadTable(self.inUniqueA, self.uniqueA)
		self.loadTable(self.inUniqueB, self.uniqueB)
		self.loadTable(self.inOvlp, self.compOvlp+self.confOvlp)
		self.doneBut.setText('Merge')
		self.doneBut.clicked.connect( self.done )
		self.moveSelectedA.setText('Move Selected')
		self.moveSelectedO.setText('Move Selected')
		self.moveSelectedB.setText('Move Selected')
		self.moveSelectedA.clicked.connect( self.moveItems )
		self.moveSelectedO.clicked.connect( self.moveItems )
		self.moveSelectedB.clicked.connect( self.moveItems )
	def loadLayout(self):
		container = QVBoxLayout()
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

		container.addLayout(columnContainer)
		container.addWidget(self.doneBut)
		self.setLayout(container)
	def loadTable(self, table, items):
		'''Load <table> with <items>'''
		for item in items:
			if item.__class__.__name__ == 'Contour':
				listItem = self.contourTableItem(item)
			elif type(item) == type([]): # ovlp items are a list of two contours
				listItem = self.contourTableItem(item)
				if item in self.confOvlp: # Conflicting ovlping contour
					listItem.setBackground(QColor('red'))
			else:
				print('loadTable: Invalid input')
			table.addItem(listItem)
		table.setSelectionMode(QAbstractItemView.ExtendedSelection)
		table.itemDoubleClicked.connect(self.doubleClicked)
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
	def done(self): #===
		# Check ovlp table for conflicts (red)
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
		print str( oA+oO+oB ) #===
		#=== Check for domain1 <- contour that represents the section's image
		#=== set self.output to resolved contours
		#=== close window?
	def doubleClicked(self, item): #===
		if item.background() == QColor('red'):
			item.clicked()
		else:
			print 'Not red!'
# - Attributes
class sectionAttributes(QWidget): #===
	def __init__(self, dictA, dictB):
		QWidget.__init__(self)

# SERIES #===
# - Contours
# - ZContours
# - Attributes