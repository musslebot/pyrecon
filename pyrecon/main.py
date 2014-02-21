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

#def calibrate(path): #===
#    return

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
	def excelGo(self): #===
		print('excelTool')
	def curateGo(self): #===
		print('curationTool')
	def calibGo(self): #===
		print('calibrationTool')

