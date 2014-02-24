'''Graphical handler functions for mergeTool conflicts'''
from PySide.QtCore import *
from PySide.QtGui import *

# SECTIONS
# - Attributes
class sectionAttributes(QWidget): #=== Section A's attributes are default as of now
	def __init__(self, dictA, dictB):
		QWidget.__init__(self)
		self.output = {}
		self.output['name'] = dictA['name']
		self.output['index'] = dictA['index']
		self.output['thickness'] = dictA['thickness']
		self.output['alignLocked'] = dictA['alignLocked']
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
		self.show()
	def loadObjects(self):
		self.img1label = QLabel(self)
		self.img2label = QLabel(self)
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
	def ret1(self):
		self.output = self.img1
		self.close()
	def ret2(self):
		self.output = self.img2
		self.close()
# - Contours
class resolveOvlp(QMessageBox): #=== still needs to display actual contour picture
	def __init__(self, item):
		QMessageBox.__init__(self)
		self.setWindowTitle('Contour Overlap Resolution')
		self.item = item
		self.loadObjects()
		self.loadText()
		self.exec_()
	def loadObjects(self):
		# Buttons to choose contours
		self.cont1But = self.addButton("Choose Contour 1", QMessageBox.ActionRole)
		self.cont2But = self.addButton("Choose Contour 2", QMessageBox.ActionRole)
	def loadText(self):
		self.setText('Choose Contour 1 or 2.\n\nClick \'show details\' to see more info.')
		details = ''
		details += 'Name:\n\t{}\t{}\n'.format(self.item.contour1.name,self.item.contour2.name)
		details += 'Comment:\n\t{}\t{}\n'.format(self.item.contour1.comment,self.item.contour2.comment)
		details += 'Hidden:\n\t{}\t{}\n'.format(self.item.contour1.hidden,self.item.contour2.hidden)
		details += 'Closed:\n\t{}\t{}\n'.format(self.item.contour1.closed,self.item.contour2.closed)
		details += 'Simplified:\n\t{}\t{}\n'.format(self.item.contour1.simplified,self.item.contour2.simplified)
		details += 'Mode:\n\t{}\t{}\n'.format(self.item.contour1.mode,self.item.contour2.mode)
		details += 'Border:\n\t{}\t{}\n'.format(self.item.contour1.border,self.item.contour2.border)
		details += 'Fill:\n\t{}\t{}\n'.format(self.item.contour1.fill,self.item.contour2.fill)
		details += 'Points:\n\t'+'\n\t'.join([str(thing[0])+' vs '+str(thing[1]) for thing in zip(self.item.contour1.points,self.item.contour2.points)])
		self.setDetailedText(details)
class contourTableItem(QListWidgetItem):
	'''This class has the functionality of a QListWidgetItem while also being able to store a pointer to the contour(s) it represents.'''
	def __init__(self, contour):
		QListWidgetItem.__init__(self)
		if type(contour) == type([]):
			self.contour = None
			self.contour1 = contour[0]
			self.contour2 = contour[1]
			self.setText(self.contour1.name)
		else:
			self.contour = contour
			self.setText(contour.name)
	def clicked(self):
		item = self
		msg = resolveOvlp(item)
		if msg.clickedButton() == msg.cont1But:
			self.contour = self.contour1
			self.setBackground(QColor('lightgreen'))
		elif msg.clickedButton() == msg.cont2But:
			self.contour = self.contour2
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
			self.s1name = sections[0].name
			self.s2name = sections[1].name
		# output
		self.output = None
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
		for table in [self.inUniqueA, self.inUniqueB, self.inOvlp, self.outUniqueA, self.outUniqueB, self.outOvlp]:
			table.setSelectionMode(QAbstractItemView.ExtendedSelection)
			table.itemDoubleClicked.connect(self.doubleClickCheck)
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
				listItem = contourTableItem(item)
				if type(item) == type([]) and item in self.confOvlp: # Conflicting ovlping contour
					listItem.setBackground(QColor('red'))
				elif type(item) == type([]) and item in self.compOvlp: # Completely ovlping contour
					listItem.contour = listItem.contour1 # set chosen contour to cont1 since they're the same
				table.addItem(listItem)
			else:
				print 'Invalid item for contourListWidget'
	def doubleClickCheck(self, item):
		if item.background() == QColor('red') or item.background() == QColor('lightgreen'):
			item.clicked()	
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
	def done(self):
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
		oO = [] # Overlap #=== pick correct item
		for i in range(self.outOvlp.count()):
			oO.append(self.outOvlp.item(i))
		oB = [] # Unique B
		for i in range(self.outUniqueB.count()):
			oB.append(self.outUniqueB.item(i))
		# Check for domain1 <- contour that represents the section's image
		if ('domain1' not in [item.contour1.name for item in oO] and
		'domain1' not in [item.contour.name for item in oA] and
		'domain1' not in [item.contour.name for item in oB]):
			msg = QMessageBox(self)
			msg.setText('"domain1" was not found in any output column. The "domain1" contour essential for correctly mapping contours to their place on the image. Merge aborted.')
			msg.exec_()
			return
		# set self.output to chosen contours
		self.output = [item.contour for item in oA]+[item.contour for item in oO]+[item.contour for item in oB]
		self.close()

# SERIES
# - Attributes #=== low priority, return A's for now
class seriesAttributes(QWidget):
	def __init__(self, dictA, dictB):
		QWidget.__init__(self)
		self.setWindowTitle('Series Attributes')
		box = QVBoxLayout()
		self.lab = QLabel('This is a placeholder until complete. Attributes from series1 are kept for now. x out of window') #===
		box.addWidget(self.lab)
		self.setLayout(box)
		self.output = {}
		for key in dictA:
			if key not in ['zcontours','contours', 'sections']: # ignore zcontours, contours, sections -- they have their own merge functions
				self.output[key] = dictA[key]
		self.show()
# - Contours #=== low priority, return A's for now
class seriesContours(QWidget):
	def __init__(self, contsA, contsB):
		QWidget.__init__(self)
		self.setWindowTitle('Series Contours')
		box = QVBoxLayout()
		self.lab = QLabel('This is a placeholder until complete. Contours from series1 are kept for now. x out of window') #===
		box.addWidget(self.lab)
		self.setLayout(box)
		self.output = contsA #===
		self.show()
# - ZContours #=== HIGH PRIORITY, add uniques to merged
class seriesZContours(QWidget):
	def __init__(self, zConts1, zConts2, mergedZConts):
		QWidget.__init__(self)
		self.setWindowTitle('Series ZContours')
		box = QVBoxLayout()
		self.lab = QLabel('This is a placeholder until complete. ZContours from both series are kept for now. x out of window') #===
		box.addWidget(self.lab)
		self.setLayout(box)
		# add leftover, unique zcontours to ser3zconts
		mergedZConts.extend(zConts1)
		mergedZConts.extend(zConts2)
		self.output = mergedZConts
		self.show()