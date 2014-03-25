from PySide.QtCore import *
from PySide.QtGui import *
import pyrecon

class seriesWrapper(QTabWidget):
	'''seriesWrapper is a TabWidget. It contains multiple widgets that can be swapped bia their tabs.'''
	def __init__(self, series1, series2, parent=None):
		QTabWidget.__init__(self, parent)
		self.series1 = series1
		self.series2 = series2
		self.loadObjects(series1, series2)
	def loadObjects(self, series1, series2):
		# Load widgets to be used as tabs
		self.attributes = pyrecon.mergeTool.seriesMerge.mergeAttributes(series1, series2, handler=seriesAttributes)
		# TEMPORARY PLACEHOLDERS #===
		self.contours = QLabel('Contour placeholder')
		self.zcontours = QLabel('ZContour placeholder')
			#===
		# self.contours = pyrecon.mergeTool.seriesMerge.mergeContours(
		# 	series1, series2, handler=seriesContours)
		# self.zcontours = pyrecon.mergeTool.seriesMerge.mergeZContours(series1, series2, handler=seriesZContours)
		self.addTab(self.attributes, '&Attributes')
		self.addTab(self.contours, '&Contours')
		self.addTab(self.zcontours, '&ZContours')
	def toObject(self):
		'''Returns series object from the output of each resolution tab.'''
		try: #===
			mergeSeries = pyrecon.classes.Series(self.attributes.output,
				self.contours.output,
				self.zcontours.output)
		except:
			print 'Could not output to Series object :('

# - Attributes #=== low priority, return one or other for now
class seriesAttributes(QWidget):
	def __init__(self, dictA, dictB):
		QWidget.__init__(self)
		self.atts1 = {}
		self.atts2 = {}
		self.output = None
		self.loadObjects(dictA,dictB)
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self,dictA,dictB):
		for key in dictA:
			if key not in ['name','path','zcontours','contours', 'sections']: # ignore zcontours, contours, sections -- they have their own merge functions
				self.atts1[key] = dictA[key]
				self.atts2[key] = dictB[key]
		# Create QLabels that display attributes
		self.attLabel1 = QLabel()
		self.attLabel2 = QLabel()
		self.attLabel1.setText('Series 1 Attributes:\n'+'\n'.join(str(self.atts1[key]) for key in self.atts1))
		self.attLabel2.setText('Series 2 Attributes:\n'+'\n'.join(str(self.atts2[key]) for key in self.atts2))
	def loadFunctions(self): #=== QLabel has no click
		# self.attLabel1.clicked.connect( self.chooseAtt )
		# self.attLabel2.clicked.connect( self.chooseAtt )
		return
	def loadLayout(self):
		main = QHBoxLayout()
		main.addWidget(self.attLabel1)
		main.addWidget(self.attLabel2)
		self.setLayout(main)
	def chooseAtt(self):
		if self.sender() == self.attLabel1:
			print('Series 1 attributes chosen!')
		elif self.sender() == self.attLabel2:
			print('Series 2 attributes chosen!')
		else: #===
			print('What?!?!!?')		
# - Contours #=== low priority, return A's for now
class seriesContours(QDialog):
	def __init__(self, contsA, contsB):
		QDialog.__init__(self)
		self.setWindowTitle('Series Contours')
		box = QVBoxLayout()
		self.lab = QLabel('This is a placeholder until complete. Contours from series1 are kept for now. x out of window') #===
		self.closeBut = QPushButton(self)
		self.closeBut.setText('Close and continue')
		self.closeBut.clicked.connect( self.close )
		box.addWidget(self.lab)
		box.addWidget(self.closeBut)
		self.setLayout(box)
		self.output = contsA #===
		self.exec_()
# - ZContours #=== HIGH PRIORITY, add uniques from zConts1,zConts2 to merged
class seriesZContours(QDialog):
	def __init__(self, zConts1, zConts2, mergedZConts):
		QDialog.__init__(self)
		self.setWindowTitle('Series ZContours')
		box = QVBoxLayout()
		self.lab = QLabel('This is a placeholder until complete. ZContours from both series are kept for now. x out of window') #===
		self.closeBut = QPushButton(self )
		self.closeBut.setText('Close and continue')
		self.closeBut.clicked.connect( self.close )
		box.addWidget(self.lab)
		box.addWidget(self.closeBut)
		self.setLayout(box)
		# add leftover, unique zcontours to ser3zconts
		mergedZConts.extend(zConts1)
		mergedZConts.extend(zConts2)
		self.output = mergedZConts
		self.exec_()