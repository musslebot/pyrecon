from PySide.QtCore import *
from PySide.QtGui import *
from pyrecon.pyreconGUI import *

class mergeSelection(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.seriesButton = QPushButton()
        self.sectionSelect = QListWidget()
        self.attSelect = QPushButton()
        self.imgSelect = QPushButton()
        self.contSelect = QPushButton()
    def loadFunctions(self):
        self.seriesButton.setText('Load Series')
        # self.seriesButton.clicked.connect( )
        self.attSelect.setText('A')
        self.attSelect.setToolTip('Resolve attribute conflicts')
        self.imgSelect.setText('I')
        self.imgSelect.setToolTip('Resolve image conflicts')
        self.contSelect.setText('C')
        self.contSelect.setToolTip('Resolve contour conflicts')
    def loadLayout(self):
        mainBox = QHBoxLayout()
        #--- Select What you're looking at (series, section, attributes, images, contours)
        selectBox = QVBoxLayout()
        selectBox.addWidget( self.seriesButton )
        selectBox.addWidget( self.sectionSelect )
        AICBox = QHBoxLayout()
        AICBox.addWidget( self.attSelect )
        AICBox.addWidget( self.imgSelect )
        AICBox.addWidget( self.contSelect )
        selectBox.addLayout(AICBox)
        #---
        mainBox.addLayout( selectBox )
        self.setLayout(mainBox)

class saveComplete(QWidget):
    '''Choose directory to save, then close and save.'''
    def __init__(self):
        QWidget.__init__(self)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.dirBrowse = directoryBrowse()
        self.doneButton = QPushButton()
    def loadFunctions(self):
        self.doneButton.setText('Save and Close')
        self.doneButton.clicked.connect( self.saveAndClose )
    def loadLayout(self):
        vbox = QVBoxLayout()
        vbox.addWidget( self.dirBrowse )
        vbox.addWidget( self.doneButton )
        self.setLayout(vbox)
    def saveAndClose(self): #===
        print('CLICKED SAVE AND CLOSE')