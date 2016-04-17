from PySide.QtCore import *
from PySide.QtGui import *
import pyrecon

# SERIES CONFLICT RESOLUTION GUI WRAPPER
class SeriesMergeWrapper(QTabWidget):
	'''seriesWrapper is a TabWidget. It contains multiple widgets that can be swapped via tabs.'''
	def __init__(self, MergeSeries):
		QTabWidget.__init__(self)
		self.merge = MergeSeries
		self.loadObjects()
	def loadObjects(self):
		# Load widgets to be used as tabs
		self.attributes = SeriesAttributeHandler(self.merge)
		self.contours = SeriesContourHandler(self.merge)
		self.zcontours = SeriesZContourHandler(self.merge)
		# Add widgets as tabs
		self.addTab(self.attributes, '&Attributes')
		self.addTab(self.contours, '&Contours')
		self.addTab(self.zcontours, '&ZContours')
	def doneCount(self):
		return self.merge.doneCount()
# - Attributes
class SeriesAttributeHandler(QWidget):
	def __init__(self, MergeSeries):
		QWidget.__init__(self)
		self.merge = MergeSeries
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
		self.checkEquivalency()
	def checkEquivalency(self):
		'''Checks to see if conflict already resolved. Should be run only during __init__'''
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
		self.leftLabel.setText('\n'.join(str(key)+':\t'+str(self.merge.series1.attributes()[key]) for key in self.merge.series1.attributes()))
		self.rightLabel.setText('\n'.join(str(key)+':\t'+str(self.merge.series2.attributes()[key]) for key in self.merge.series2.attributes()))
		self.leftLabel.setWordWrap(True)
		self.rightLabel.setWordWrap(True)
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
		# Left half (series1)
		leftHalf = QVBoxLayout()
		leftScroll = QScrollArea()
		leftScroll.setWidget(self.leftLabel)
		leftHalf.addWidget( leftScroll )
		leftHalf.addWidget( self.chooseLeft )
		# Right half (series2)
		rightHalf = QVBoxLayout()
		rightScroll = QScrollArea()
		rightScroll.setWidget(self.rightLabel)
		rightHalf.addWidget( rightScroll )
		rightHalf.addWidget( self.chooseRight )
		# Add halves to container
		container.addLayout( leftHalf )
		container.addLayout( rightHalf )
		self.setLayout( container ) 
	def choose(self):
		if self.sender() == self.chooseLeft:
			self.merge.attributes = self.merge.series1.attributes()
			self.chooseLeft.setStyleSheet('background-color:lightgreen;')
			self.chooseRight.setStyleSheet(QWidget().styleSheet())
		elif self.sender() == self.chooseRight:
			self.merge.attributes = self.merge.series2.attributes()
			self.chooseLeft.setStyleSheet(QWidget().styleSheet())
			self.chooseRight.setStyleSheet('background-color:lightgreen;')
# - Contours
class SeriesContourHandler(QWidget):
	def __init__(self, MergeSeries):
		QWidget.__init__(self)
		self.merge = MergeSeries
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
		self.checkEquivalency()
	def checkEquivalency(self):
		'''Checks to see if conflict already resolved. Should be run only during __init__'''
		if self.merge.contours is not None:
			txt = 'Contours are equivalent, no conflict.'
			self.chooseLeft.setText(txt)
			self.chooseRight.setText(txt)
			self.chooseLeft.setStyleSheet('background-color:lightgreen;')
			self.chooseRight.setStyleSheet('background-color:lightgreen;')
	def loadObjects(self):
		# Buttons to resolve conflicts
		self.chooseLeft = QPushButton('Choose These Contours')
		self.chooseRight = QPushButton('Choose These Contours')
		# - Button looks
		self.chooseLeft.setMinimumHeight(50)
		self.chooseRight.setMinimumHeight(50)
		# Labels for displaying contours (text)
		self.leftLabel = QLabel()
		self.rightLabel = QLabel()
		for cont in self.merge.series1.contours:
			self.leftLabel.setText(str(self.leftLabel.text())+'\n'.join(str(contour.__dict__) for contour in self.merge.series1.contours)+'\n')
		for cont in self.merge.series2.contours:
			self.rightLabel.setText(str(self.rightLabel.text())+'\n'.join(str(contour.__dict__) for contour in self.merge.series2.contours)+'\n')
		self.leftLabel.setWordWrap(True)
		self.rightLabel.setWordWrap(True)
		# Adjust font
		font = QFont("Arial", 14)
		self.leftLabel.setFont(font)
		self.rightLabel.setFont(font)
	def loadFunctions(self):
		# Button functions
		self.chooseLeft.clicked.connect( self.choose )
		self.chooseRight.clicked.connect( self.choose )
	def loadLayout(self):
		container = QHBoxLayout()
		# Left half (series1)
		leftHalf = QVBoxLayout()
		leftScroll = QScrollArea()
		leftScroll.setWidget(self.leftLabel) # Set scrollarea widget as leftlabel
		leftHalf.addWidget( leftScroll )
		leftHalf.addWidget( self.chooseLeft )
		# Right half (series2)
		rightHalf = QVBoxLayout()
		rightScroll = QScrollArea()
		rightScroll.setWidget(self.rightLabel)
		rightHalf.addWidget( rightScroll )
		rightHalf.addWidget( self.chooseRight )
		# Add halves to container
		container.addLayout( leftHalf )
		container.addLayout( rightHalf )
		self.setLayout( container ) 
	def choose(self):
		if self.sender() == self.chooseLeft:
			self.merge.contours = self.merge.series1.contours
			self.chooseLeft.setStyleSheet('background-color:lightgreen;')
			self.chooseRight.setStyleSheet(QWidget().styleSheet())
		elif self.sender() == self.chooseRight:
			self.merge.contours = self.merge.series2.contours
			self.chooseRight.setStyleSheet('background-color:lightgreen;')
			self.chooseLeft.setStyleSheet(QWidget().styleSheet())
# - ZContours #===
class SeriesZContourHandler(QWidget):
	def __init__(self, MergeSeries):
		QWidget.__init__(self)
		self.merge = MergeSeries
		
		container = QVBoxLayout()
		container.setAlignment(Qt.AlignHCenter)

		self.label = QLabel('All unique ZContours were kept and all non-unique ZContours were merged. Double click series object in the list to change this.') #===
		self.label.setFont(QFont("Arial",18))
		self.label.setWordWrap(True)
		self.label.setAlignment(Qt.AlignHCenter)

		self.scroll = QScrollArea()
		self.scroll.setWidget(self.label)
		self.scroll.setAlignment(Qt.AlignHCenter)
		container.addWidget(self.scroll)
		self.setLayout(container)

		# add leftover, unique zcontours to merged zcontour list
		unique1, unique2, overlaps = self.merge.getCategorizedZContours()
		self.merge.zcontours = unique1+unique2+overlaps
