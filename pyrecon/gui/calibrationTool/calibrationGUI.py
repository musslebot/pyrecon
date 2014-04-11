from PySide.QtCore import *
from PySide.QtGui import *

from pyrecon.main import openSeries
import pyrecon.tools.calibrationTool
from pyrecon.gui.main import *

class calibrationToolStuff(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self):
		self.loadButton = QPushButton()
		self.options = calibOptions(parent=self)
		self.runButton = QPushButton()
	def loadFunctions(self):
		self.loadButton.setText('Load Series')
		self.loadButton.clicked.connect( self.loadSeries )
		self.loadButton.setMinimumHeight(50)
		self.runButton.setText('Run calibrationTool')
		self.runButton.clicked.connect( self.runCalibration )
		self.runButton.setMinimumHeight(50)
		self.runButton.setFlat(True)
	def loadLayout(self):
		main = QVBoxLayout()
		main.addWidget( self.loadButton )
		main.addWidget( self.options )
		main.addWidget( self.runButton )
		self.setLayout(main)
	def loadSeries(self):
		seriesDialog = singleSeriesLoad()
		seriesDialog.exec_()
		self.series = openSeries(seriesDialog.output)
		self.loadButton.setText('Change Series\nCurrent series:'+self.series.name)
		self.runButton.setStyleSheet(QPushButton().styleSheet())
		self.runButton.setFlat(False)
	def runCalibration(self):
		# Available options: 'auto', 'factor', 'rescale', 'outDir'
		options = self.options.parameters()
		if options['auto']: # Use autocalibration factor
			factor = pyrecon.calibrationTool.findCalFactor.findCalFactor(self.series)
			if not options['rescale']:
				# No rescale, just display the found calibration factor
				msg = QMessageBox()
				msg.setText('Calibration factor found: '+str(factor))
				msg.exec_()
			elif options['rescale']:
				# Perform rescale using findCalFactor as newMag
				pyrecon.calibrationTool.reScale.main(self.series, factor, options['outDir'])
				msg = QMessageBox()
				msg.setText('Finished rescaling using auto factor!'+'\nOutput: '+str(options['outDir']))
				msg.exec_()
		else: # Use custom calibration factor
			factor = options['factor']
			if not options['rescale']:
				msg = QMessageBox()
				msg.setText('Nothing to do here... check options.')
				msg.exec_()
			elif options['rescale']:
				# Perform rescale using custom cal factor as newMag
				pyrecon.calibrationTool.reScale.main(self.series, factor, options['outDir'])
				msg = QMessageBox()
				msg.setText('Finished rescaling using custom factor!'+'\nOutput: '+str(options['outDir']))
				msg.exec_()

class calibOptions(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.loadObjects()
		self.loadFunctions()
		self.loadLayout()
	def loadObjects(self):
		self.autoCalFactor = QCheckBox('Automatically find calibration factor', self)
		self.customCalFactor = QCheckBox('Use custom calibration factor', self)
		self.customFactor = QLineEdit()
		self.customFactor.setText('<calibration factor (float)>')
		self.reScale = QCheckBox('Rescale series', self)
		self.dirBrowse = browseWidget()
		self.dirBrowse.hide() # until rescale is checked
	def loadFunctions(self):
		self.autoCalFactor.released.connect( self.factorCheck )
		self.customCalFactor.released.connect( self.factorCheck )
		# signal a confirmation window when reScale is checked
		self.reScale.released.connect( self.reScaleCheck )
	def loadLayout(self):
		main = QVBoxLayout()
		main.addWidget(self.autoCalFactor)
		cust = QHBoxLayout()
		cust.addWidget(self.customCalFactor)
		cust.addWidget(self.customFactor)
		main.addLayout(cust)
		main.addWidget(self.reScale)
		main.addWidget(self.dirBrowse)
		self.setLayout(main)
	def factorCheck(self):
		'''Uncheck other factor option if one is checked'''
		if (self.sender() == self.autoCalFactor and
			self.autoCalFactor.isChecked()):
			self.customCalFactor.setCheckState(Qt.Unchecked)
		elif (self.sender() == self.customCalFactor and
			  self.customCalFactor.isChecked()):
			self.autoCalFactor.setCheckState(Qt.Unchecked)
	def reScaleCheck(self):
		if self.reScale.isChecked():
			self.dirBrowse.show()
		elif not self.reScale.isChecked():
			self.dirBrowse.hide()
	def parameters(self):
		'''Return the option parameters necessary for running calibrationTool'''
		parameters = {}
		# Auto or custom calibration factor?
		if self.autoCalFactor.isChecked():
			parameters['auto']=True
		elif self.customCalFactor.isChecked():
			try:
				parameters['factor']=float(self.customFactor)
			except:
				msg = QMessageBox()
				msg.setText('Invalid custom calibration factor')
				msg.exec_()
				return
		# Rescale series?
		if self.reScale.isChecked():
			parameters['rescale']=True
			parameters['outDir']=self.dirBrowse.path.text()
		else:
			parameters['rescale']=False
		return parameters


