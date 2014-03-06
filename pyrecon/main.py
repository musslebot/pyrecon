'''Main, overarching functions.'''
from pyrecon.classes import Section, Series
import os, re
try:
	from PySide.QtCore import *
	from PySide.QtGui import *
except:
	print('Problem importing PySide. You will not be able to use GUI functions.')

def openSeries(path):
	'''Returns a Series object with associated Sections from the same directory.'''
	# Process <path> and create Series object
	if '.ser' in path: # Search path for .ser 
		pathToSeries = path
	else: # or .ser in directory path?
		if path[-1] != '/':
			path += '/'
		pathToSeries = path+str([f for f in os.listdir(path) if '.ser' in f].pop())
	series = Series(pathToSeries)
	series.update(sections=True) # find sections in directory
	return series

def merge(path1, path2, outputDirectory, *args, **kwargs): #===
	# direct arguments to mergeTool.merge; arg handling is performed there
	return 

def curate(series, thresholdForDistantTraces): #===
	return

def excel(series, outputDirectory): #===
	return

def calibrate(path): #===
	return

def start():
	app = QApplication.instance()
	if app is None: # Create QApplication if doesn't exist
		app = QApplication([])
	pickTool = toolLoader()
	app.exec_()

class toolLoader(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.loadObjects()
		self.loadFunctions()
		self.loadLayouts()
		self.show()
	def loadObjects(self):
		self.mergeBut = QPushButton('mergeTool')
		self.excelBut = QPushButton('excelTool')
		self.curateBut = QPushButton('curationTool')
		self.calibBut = QPushButton('calibrationTool')
	def loadFunctions(self):
		self.mergeBut.clicked.connect( self.mergeGo )
		self.excelBut.clicked.connect( self.excelGo )
		self.curateBut.clicked.connect( self.curateGo )
		self.calibBut.clicked.connect( self.calibGo )
	def loadLayouts(self):
		vbox = QVBoxLayout()
		vbox.addWidget(self.mergeBut)
		vbox.addWidget(self.excelBut)
		vbox.addWidget(self.curateBut)
		vbox.addWidget(self.calibBut)
		self.setLayout(vbox)
	def mergeGo(self): #===
		print('mergeTool')
		self.a = seriesLoader(title='Load Series 1')
		self.b = seriesLoader(title='Load Series 2')
	def excelGo(self): #===
		print('excelTool')
	def curateGo(self): #===
		print('curationTool')
	def calibGo(self): #===
		print('calibrationTool')

class seriesLoader(QWidget):
	def __init__(self, title='Load Series'):
		QWidget.__init__(self)
		print('start serload')
		self.setWindowTitle(title)
		self.loadObjects()
		self.loadFunctions()
		self.loadLayouts()
		self.show()
	def loadObjects(self):
		self.pathLine = QLineEdit(self) # Line to enter path to series
		self.pathLine.setText('<Enter path to series file, or browse>')
		self.browseButton = QPushButton(self) # button to browse for series
		self.browseButton.setText('Browse')
		self.closeButton = QPushButton(self)
		self.closeButton.setText('Load and Close')
	def loadFunctions(self):
		self.browseButton.clicked.connect( self.browseFiles )
		self.closeButton.clicked.connect( self.loadClose )
	def loadLayouts(self):
		vbox = QVBoxLayout()
		
		hbox = QHBoxLayout()
		hbox.addWidget(self.pathLine)
		hbox.addWidget(self.browseButton)
		
		vbox.addLayout(hbox)
		vbox.addWidget(self.closeButton)
		self.setLayout(vbox)

	def browseFiles(self):
		fileName = QFileDialog.getOpenFileName(self, "Load Series", "/home/", "Series File (*.ser)")
		self.pathLine.setText( str(fileName[0]) )
	def loadClose(self): #===
		print 'closing'
		print self.pathLine.text()
		return openSeries( self.pathLine.text() )
		self.close()


