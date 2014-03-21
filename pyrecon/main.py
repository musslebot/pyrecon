'''Main, overarching functions.'''
from pyrecon.classes import Section, Series
import os
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

def start():
	app = QApplication.instance()
	if app is None: # Create QApplication if doesn't exist
		app = QApplication([])
	pickTool = toolLoader()
	app.exec_() # Start event-loop

# class excelToolLoader(QWidget):
# 	def __init__(self, title='excelTool Loader'):
# 		QWidget.__init__(self)
# 		self.setWindowTitle(title)
# 		self.resize(QSize(300,100))
# 		self.loadObjects()
# 		self.loadFunctions()
# 		self.loadLayouts()
# 		self.show()
# 	def loadObjects(self):
# 		self.path = QLineEdit(self)
# 		self.path.setText('<Enter path to series, or browse>')
# 		self.outDir = QLineEdit(self)
# 		self.outDir.setText('<Enter directory to save .xlsx file>')
# 		self.browse = QPushButton(self)
# 		self.browse.setText('Browse')
# 		self.browse2 = QPushButton(self)
# 		self.browse2.setText('Browse')
# 		self.doneBut = QPushButton(self)
# 		self.doneBut.setText('Begin excelTool')
# 	def loadFunctions(self):
# 		self.browse.clicked.connect( self.browseStuff )
# 		self.browse2.clicked.connect( self.browseStuff )
# 		self.doneBut.clicked.connect( self.finish )
# 	def loadLayouts(self):
# 		vbox = QVBoxLayout()
# 		hbox = QHBoxLayout()
# 		hbox.addWidget(self.path)
# 		hbox.addWidget(self.browse)
# 		hbox2 = QHBoxLayout()
# 		hbox2.addWidget(self.outDir)
# 		hbox2.addWidget(self.browse2)
# 		vbox.addLayout(hbox)
# 		vbox.addLayout(hbox2)
# 		vbox.addWidget(self.doneBut)
# 		self.setLayout(vbox)
# 	def browseStuff(self):
# 		if self.sender() == self.browse:
# 			fileName = QFileDialog.getOpenFileName(self, "Load Series 1", "/home/", "Series File (*.ser)")
# 			self.path.setText( str(fileName[0]) )
# 		elif self.sender() == self.browse2:
# 			dirName = QFileDialog.getExistingDirectory(self)
# 			self.outDir.setText( str(dirName) )
# 	def finish(self):
# 		from pyrecon import excelTool
# 		self.output = ( str(self.path.text()), str(self.outDir.text()) )
# 		self.close()
# 		excelTool.excelTool.main(*self.output)
# class curationToolLoader(QWidget):
# 	def __init__(self, title='curationTool Loader'):
# 		QWidget.__init__(self)
# 		self.setWindowTitle(title)
# 		self.resize(QSize(300,100))
# 		self.loadObjects()
# 		self.loadFunctions()
# 		self.loadLayouts()
# 		self.show()
# 	def loadObjects(self):
# 		self.path = QLineEdit(self)
# 		self.path.setText('<Enter path to series, or browse>')
# 		self.distance = QLineEdit(self)
# 		self.distance.setText('<Enter distance threshold (integer)>')
# 		self.browse = QPushButton(self)
# 		self.browse.setText('Browse')
# 		self.doneBut = QPushButton(self)
# 		self.doneBut.setText('Begin curationTool')
# 	def loadFunctions(self):
# 		self.browse.clicked.connect( self.browseStuff )
# 		self.doneBut.clicked.connect( self.finish )
# 	def loadLayouts(self):
# 		vbox = QVBoxLayout()
# 		hbox = QHBoxLayout()
# 		hbox.addWidget(self.path)
# 		hbox.addWidget(self.browse)
# 		hbox2 = QHBoxLayout()
# 		hbox2.addWidget(self.distance)
# 		vbox.addLayout(hbox)
# 		vbox.addLayout(hbox2)
# 		vbox.addWidget(self.doneBut)
# 		self.setLayout(vbox)
# 	def browseStuff(self):
# 		if self.sender() == self.browse:
# 			fileName = QFileDialog.getOpenFileName(self, "Load Series", "/home/", "Series File (*.ser)")
# 			self.path.setText( str(fileName[0]) )
# 	def finish(self):
# 		from pyrecon import curationTool
# 		# Add paths to self.output
# 		self.output = ( str(self.path.text()), int(self.distance.text()) )
# 		self.close()
# 		# Run mergeTool
# 		curationTool.curationTool.main(*self.output)
# class calibrationToolLoader(QWidget):
# 	def __init__(self, title='calibrationTool Loader'):
# 		QWidget.__init__(self)
# 		self.setWindowTitle(title)
# 		self.resize(QSize(375,100))
# 		self.loadObjects()
# 		self.loadFunctions()
# 		self.loadLayouts()
# 		self.show()
# 	def loadObjects(self):
# 		self.path1 = QLineEdit(self)
# 		self.path1.setText('<Enter path to series, or browse>')
# 		self.browse1 = QPushButton(self)
# 		self.browse1.setText('Browse')
# 		self.outDir = QLineEdit(self)
# 		self.outDir.setText('<Enter directory to save calibrated series in>')
# 		self.browse2 = QPushButton(self)
# 		self.browse2.setText('Browse')
# 		self.doneBut = QPushButton(self)
# 		self.doneBut.setText('Begin calibrationTool')
# 	def loadFunctions(self):
# 		self.browse1.clicked.connect( self.browseStuff )
# 		self.browse2.clicked.connect( self.browseStuff )
# 		self.doneBut.clicked.connect( self.finish )
# 	def loadLayouts(self):
# 		vbox = QVBoxLayout()
# 		hbox1 = QHBoxLayout()
# 		hbox1.addWidget(self.path1)
# 		hbox1.addWidget(self.browse1)
# 		vbox.addLayout(hbox1)
# 		hbox2 = QHBoxLayout()
# 		hbox2.addWidget(self.outDir)
# 		hbox2.addWidget(self.browse2)
# 		vbox.addLayout(hbox2)
# 		vbox.addWidget(self.doneBut)
# 		self.setLayout(vbox)
# 	def browseStuff(self):
# 		if self.sender() == self.browse1:
# 			fileName = QFileDialog.getOpenFileName(self, "Load Series", "/home/", "Series File (*.ser)")
# 			self.path1.setText( str(fileName[0]) )
# 		elif self.sender() == self.browse2:
# 			dirName = QFileDialog.getExistingDirectory(self)
# 			self.outDir.setText( str(dirName) )
# 	def finish(self):
# 		from pyrecon import calibrationTool
# 		self.output = ( str(self.path1.text()), str(self.outDir.text()) )
# 		self.close()
# 		calibrationTool.reScale.main(self.output[0], calibrationTool.findCalFactor.findCalFactor(self.output[0]), self.output[1])