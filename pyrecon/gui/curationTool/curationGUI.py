from PySide.QtCore import *
from PySide.QtGui import *

from pyrecon.main import openSeries
from pyrecon.gui.main import SingleSeriesLoad
import pyrecon.tools.curationTool

class curationToolStuff(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.loadButton = QPushButton()
        self.options = curateOptions(parent=self)
        self.runButton = QPushButton()
        self.outputWidget = outputBox()
    def loadFunctions(self):
        self.loadButton.setText('Load Series')
        self.loadButton.clicked.connect( self.loadSeries )
        self.loadButton.setMinimumHeight(50)
        self.runButton.setText('Run curationTool')
        self.runButton.clicked.connect( self.runCuration )
        self.runButton.setMinimumHeight(50)
        self.runButton.setFlat(True)
    def loadLayout(self):
        main = QVBoxLayout()
        main.addWidget( self.loadButton )
        main.addWidget( self.options )
        main.addWidget( self.runButton )
        self.setLayout(main)
    def loadSeries(self):
        seriesDialog = SingleSeriesLoad()
        self.series = openSeries(seriesDialog.output)
        self.loadButton.setText('Change Series\nCurrent series:'+self.series.name)
        self.runButton.setStyleSheet(QPushButton().styleSheet())
        self.runButton.setFlat(False)
    def runCuration(self):
        curationOut = pyrecon.curationTool.main(self.series, *self.options.parameters(), printOut=False)
        self.outputWidget.loadOutput(curationOut)

class curateOptions(QWidget):
    '''Allows the user to select curationTool functions and parameters.'''
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.optionLabel = QLabel()
        self.optionLabel.setText('Select what curationTool functions to be used:')
        self.duplicate = QCheckBox('D&uplicate traces')
        self.distant = QCheckBox('D&istant traces')
        self.reverse = QCheckBox('&Reverse traces')

        self.distanceParameter = QComboBox()
        self.distanceParameter.addItems([str(i) for i in range(1,201)])
    def loadFunctions(self):
        self.duplicate.setToolTip('Locate duplicate traces:\nTraces that perfectly overlap on a single section.')
        self.distant.setToolTip('Locate traces separated by a certain number of sections. Select section number from list.')
        self.reverse.setToolTip('Locate reverse traces.')
    def loadLayout(self):
        main = QVBoxLayout()

        duplicateOpt = QHBoxLayout()
        duplicateOpt.addWidget(self.duplicate)

        distantOpt = QHBoxLayout()
        distantOpt.addWidget(self.distant)
        distantOpt.addWidget(self.distanceParameter)

        reverseOpt = QHBoxLayout()
        reverseOpt.addWidget(self.reverse)

        main.addWidget(self.optionLabel)
        main.addLayout(duplicateOpt)
        main.addLayout(distantOpt)
        main.addLayout(reverseOpt)
        self.setLayout(main)
    def parameters(self):
        '''Return the option parameters necessary for running curationTool'''
        try:
            return (self.distanceParameter.currentIndex()+1,
                    self.duplicate.isChecked(),
                    self.distant.isChecked(),
                    self.reverse.isChecked())
        except:
            msg = QMessageBox()
            msg.setText('Error determining options')
            msg.exec_()

class outputBox(QWidget):
    '''Contains the output of the curationTool, with the ability to save as a txt file.'''
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.scrollArea = QScrollArea()
        self.saveButton = QPushButton()
    def loadFunctions(self):
        self.saveButton.setText('Save to .txt')
        self.saveButton.clicked.connect( self.saveToText )
        self.saveButton.setMinimumHeight(50)
        self.saveButton.setFlat(True)
    def loadLayout(self):
        main = QVBoxLayout()
        main.addWidget(self.scrollArea)
        main.addWidget(self.saveButton)
        self.setLayout(main)
    def loadOutput(self, output):
        text = QLabel()
        for fxnOutput in output:
            for lineOut in fxnOutput:
                text.setText(text.text()+lineOut+'\n')
        self.scrollArea.setWidget(text)
        self.saveButton.setFlat(False)
    def saveToText(self):
        print(self.scrollArea.widget().text())
        saveDia = saveDialog()
        saveDia.exec_()
        fileName = saveDia.output
        newFile = open(fileName, 'a')
        newFile.write(self.scrollArea.widget().text())

class saveDialog(QDialog):
    def __init__(self, textToSave=None):
        QDialog.__init__(self)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.directory = browseWidget()
        self.fileName = QLineEdit()
        self.doneButton = QPushButton()
    def loadFunctions(self):
        self.fileName.setText('Enter name of .txt file')
        self.doneButton.setText('Done')
        self.doneButton.clicked.connect( self.finish )
        self.doneButton.setMinimumHeight(50)
    def loadLayout(self):
        main = QVBoxLayout()

        main.addWidget(self.directory)
        main.addWidget(self.fileName)
        main.addWidget(self.doneButton)
        self.setLayout(main)

    def finish(self):
        fileName = self.fileName.text()
        if '.txt' not in fileName:
            fileName += '.txt'
        self.output = self.directory.path.text()+'/'+fileName
        self.close()

