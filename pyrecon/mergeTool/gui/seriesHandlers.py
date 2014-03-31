from PySide.QtCore import *
from PySide.QtGui import *
import pyrecon

class seriesWrapper(QTabWidget):
	'''seriesWrapper is a TabWidget. It contains multiple widgets that can be swapped bia their tabs.'''
	def __init__(self, series1, series2, parent=None):
		QTabWidget.__init__(self)
		self.parent = parent
		self.series1 = series1
		self.series2 = series2
		self.loadObjects()
	def loadObjects(self):
		# Load widgets to be used as tabs
		self.attributes = pyrecon.mergeTool.seriesMerge.mergeAttributes(self.series1, self.series2, handler=seriesAttributes, parent=self)
		self.contours = pyrecon.mergeTool.seriesMerge.mergeContours(
			self.series1, self.series2, handler=seriesContours, parent=self)
		self.zcontours = pyrecon.mergeTool.seriesMerge.mergeZContours(
			self.series1, self.series2, handler=seriesZContours, parent=self)
		# Add widgets as tabs
		self.addTab(self.attributes, '&Attributes')
		self.addTab(self.contours, '&Contours')
		self.addTab(self.zcontours, '&ZContours')
	def toObject(self):
		'''Returns series object from the output of each resolution tab.'''
		# Determine attributes
		if self.attributes.output is None:
			print('Series attributes default to series 1')
			attributes = self.attributes.atts1
		else:
			attributes = self.attributes.output
		# Determine contours
		if self.contours.output is None:
			print('Series contours default to series 1')
			contours = self.contours.conts1
		else:
			contours = self.contours.output
		# Determine zcontours
		if self.zcontours.output is None:
			print('Series zcontours default to series 1')
			zcontours = self.zcontours.zconts1
		else:
			zcontours = self.zcontours.output
		
		# Create merged series object
		return pyrecon.classes.Series(attributes,contours,zcontours)
	def isResolved(self):
		'''Return true if self.attributes/contours/zcontours output attribute != None'''
		resolved = (self.attributes.output is not None and
					self.contours.output is not None and
					self.zcontours.output is not None)
		# Check if parent is merge item and set bg to green
		if resolved and self.parent.__class__.__name__ == 'mergeItem':
			self.parent.setBackground(QColor('lightgreen'))
		return resolved

# - Attributes
class seriesAttributes(QWidget):
	def __init__(self, dictA, dictB, parent=None):
		QWidget.__init__(self, parent)
		self.parent = parent # parent may not be .parentWidget()
		self.setWindowTitle('Series Attributes')
		self.atts1 = {}
		self.atts2 = {}
		self.output = None
		self.loadObjects(dictA,dictB)
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self,dictA,dictB):
		for key in dictA:
			if key not in ['path','zcontours','contours', 'sections']: # ignore zcontours, contours, sections -- they have their own merge functions
				self.atts1[key] = dictA[key]
				self.atts2[key] = dictB[key]
		self.pick1 = QPushButton()
		self.pick2 = QPushButton()
		self.pick1.setText('Choose Series Attributes')
		self.pick2.setText('Choose Series Attributes')
		self.pick1.setMinimumHeight(50)
		self.pick2.setMinimumHeight(50)
		self.attLabel1 = QLabel()
		self.attLabel2 = QLabel()
		self.attLabel1.setWordWrap(True)
		self.attLabel2.setWordWrap(True)
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
		ser1 = QVBoxLayout()
		ser2 = QVBoxLayout()
		# Add attLabels to QScrollArea
		self.scrollLabel1 = QScrollArea()
		self.scrollLabel2 = QScrollArea()
		self.scrollLabel1.setWidget(self.attLabel1)
		self.scrollLabel2.setWidget(self.attLabel2)
		# Add widgets to layout
		# ser1.addWidget(QLabel('Series A Attributes'))
		ser1.addWidget(self.scrollLabel1)
		ser1.addWidget(self.pick1)
		# ser2.addWidget(QLabel('Series B Attributes'))
		ser2.addWidget(self.scrollLabel2)
		ser2.addWidget(self.pick2)
		main.addLayout(ser1)
		main.addLayout(ser2)
		self.setLayout(main)
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
# - Contours
class seriesContours(QWidget):
	def __init__(self, contsA, contsB, parent=None):
		QWidget.__init__(self, parent)
		self.parent = parent
		self.setWindowTitle('Series Contours')
		self.conts1 = contsA
		self.conts2 = contsB
		self.output = None
		self.loadObjects(contsA,contsB)
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self,dictA,dictB):
		self.pick1 = QPushButton()
		self.pick2 = QPushButton()
		self.pick1.setText('Choose Series Contours')
		self.pick2.setText('Choose Series Contours')
		self.pick1.setMinimumHeight(50)
		self.pick2.setMinimumHeight(50)
		self.contLabel1 = QLabel()
		self.contLabel2 = QLabel()
		self.contLabel1.setWordWrap(True)
		self.contLabel2.setWordWrap(True)
		for cont in self.conts1:
			self.contLabel1.setText(str(self.contLabel1.text())+'\n'.join(str(contour.__dict__) for contour in self.conts1)+'\n')
		for cont in self.conts2:
			self.contLabel2.setText(str(self.contLabel2.text())+'\n'.join(str(contour.__dict__) for contour in self.conts2)+'\n')
		# Adjust font
		font = QFont("Arial", 14)
		self.contLabel1.setFont(font)
		self.contLabel2.setFont(font)
	def loadFunctions(self):
		self.pick1.clicked.connect( self.chooseConts )
		self.pick2.clicked.connect( self.chooseConts )
	def loadLayout(self):
		main = QHBoxLayout()
		ser1 = QVBoxLayout()
		ser2 = QVBoxLayout()
		# Add attLabels to QScrollArea
		self.scrollLabel1 = QScrollArea()
		self.scrollLabel2 = QScrollArea()
		self.scrollLabel1.setWidget(self.contLabel1)
		self.scrollLabel2.setWidget(self.contLabel2)
		# Add widgets to layout
		# ser1.addWidget(QLabel('Section A Attributes'))
		ser1.addWidget(self.scrollLabel1)
		ser1.addWidget(self.pick1)
		# ser2.addWidget(QLabel('Section B Attributes'))
		ser2.addWidget(self.scrollLabel2)
		ser2.addWidget(self.pick2)
		main.addLayout(ser1)
		main.addLayout(ser2)
		self.setLayout(main)
	def chooseConts(self):
		if self.sender() == self.pick1:
			self.output = self.conts1
			self.pick1.setStyleSheet('background-color:lightgreen;')
			self.pick2.setStyleSheet(QWidget().styleSheet())
		elif self.sender() == self.pick2:
			self.output = self.conts2
			self.pick2.setStyleSheet('background-color:lightgreen;')
			self.pick1.setStyleSheet(QWidget().styleSheet())
		self.parent.isResolved()
# - ZContours #===
class seriesZContours(QWidget):
	def __init__(self, uniqueA, uniqueB, mergedZConts, parent=None):
		QWidget.__init__(self, parent)
		self.parent = parent
		self.setWindowTitle('Series ZContours')
		self.uniqueA = uniqueA
		self.uniqueB = uniqueB
		self.merged = mergedZConts
		box = QVBoxLayout()
		box.setAlignment(Qt.AlignHCenter)
		self.lab = QLabel('All unique ZContours were kept and all non-unique ZContours were merged.') #===
		self.lab.setFont(QFont("Arial",18))
		box.addWidget(self.lab)
		self.setLayout(box)
		# add leftover, unique zcontours to merged zcontour list
		self.merged.extend(self.uniqueA)
		self.merged.extend(self.uniqueB)
		self.output = self.merged
		self.parent.isResolved()