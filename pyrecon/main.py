'''Main, overarching functions.'''
from pyrecon.classes import Section, Series
import os, re
try:
	from PySide.QtCore import *
	from PySide.QtGui import *
	print('PySide imported successfully.')
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
	app.exec_() # Start event-loop

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
	def mergeGo(self):
		self.a = mergeToolLoader()
		self.close()
	def excelGo(self): #===
		print('excelTool')
	def curateGo(self): #===
		print('curationTool')
	def calibGo(self): #===
		print('calibrationTool')

class mergeToolLoader(QWidget):
	def __init__(self, title='mergeTool Loader'):
		QWidget.__init__(self)
		self.setWindowTitle(title)
		self.loadObjects()
		self.loadFunctions()
		self.loadLayouts()
		self.show()
	def loadObjects(self):
		self.path1 = QLineEdit(self) # Line to enter path to series
		self.path1.setText('<Enter path to series 1, or browse>')
		self.path2 = QLineEdit(self)
		self.path2.setText('<Enter path to series 2, or browse>')
		self.outDir = QLineEdit(self)
		self.outDir.setText('<Enter directory to save merged files in>')
		self.browse1 = QPushButton(self) # button to browse for series
		self.browse1.setText('Browse')
		self.browse2 = QPushButton(self)
		self.browse2.setText('Browse')
		self.browse3 = QPushButton(self)
		self.browse3.setText('Browse')
		self.closeButton = QPushButton(self)
		self.closeButton.setText('Begin merge')
	def loadFunctions(self):
		for but in [self.browse1, self.browse2, self.browse3]:
			but.clicked.connect( self.browseStuff )
		self.closeButton.clicked.connect( self.loadClose )
	def loadLayouts(self):
		vbox = QVBoxLayout()
		hbox1 = QHBoxLayout()
		hbox1.addWidget(self.path1)
		hbox1.addWidget(self.browse1)
		hbox2 = QHBoxLayout()
		hbox2.addWidget(self.path2)
		hbox2.addWidget(self.browse2)
		hbox3 = QHBoxLayout()
		hbox3.addWidget(self.outDir)
		hbox3.addWidget(self.browse3)
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		vbox.addLayout(hbox3)
		vbox.addWidget(self.closeButton)
		self.setLayout(vbox)
	def browseStuff(self):
		if self.sender() == self.browse1:
			fileName = QFileDialog.getOpenFileName(self, "Load Series 1", "/home/", "Series File (*.ser)")
			self.path1.setText( str(fileName[0]) )
		elif self.sender() == self.browse2:
			fileName = QFileDialog.getOpenFileName(self, "Load Series 2", "/home/", "Series File (*.ser)")
			self.path2.setText( str(fileName[0]) )
		elif self.sender() == self.browse3:
			dirName = QFileDialog.getExistingDirectory(self)
			self.path3.setText( str(dirName) )
	def loadClose(self):
		from pyrecon import mergeTool
		# Add paths to self.output
		self.output = ( str(self.path1.text()), str(self.path2.text()), str(self.outDir.text()) )
		self.close()
		# Run mergeTool
		mergeTool.merge.main(*self.output, graphical=True)
		


