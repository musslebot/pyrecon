from PySide.QtCore import *
from PySide.QtGui import *

from pyrecon.pyreconGUI import *
from pyrecon.main import openSeries

class mergeSelection(QWidget):
    '''Select what section/attributes to look at.'''
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
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
        self.seriesButton.clicked.connect( self.loadSeries )
        self.attSelect.clicked.connect( self.viewAttributes )
        self.attSelect.setText('A')
        self.attSelect.setToolTip('Resolve attribute conflicts')
        self.imgSelect.clicked.connect( self.viewImages )
        self.imgSelect.setText('I')
        self.imgSelect.setToolTip('Resolve image conflicts')
        self.contSelect.clicked.connect( self.viewContours )
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
    def loadSeries(self): #=== add series object as doubleListItem
        seriesDialog = seriesLoad()
        seriesDialog.exec_()
        try:
            self.series1 = openSeries(seriesDialog.output[0])
            self.series2 = openSeries(seriesDialog.output[1])
            self.loadSections()
        except: #=== Error message
            self.msg = QMessageBox()
            self.msg.setText('Invalid series paths!')
            self.msg.exec_()
    def loadSections(self):
        self.sectionSelect.clear() # Remove contents currently in table
        self.sectionSelect.itemDoubleClicked.connect( self.itemClicked ) # What to do when item doubleclicked
        for i in range( len(self.series1.sections) ):
            sectionItem = doubleListItem( self.series1.sections[i], self.series2.sections[i] )
            self.sectionSelect.addItem( sectionItem )
        
    def itemClicked(self, item): #===
        item.clicked()
    def viewAttributes(self): #===
        print('VIEW ATTRIBUTES')
    def viewImages(self): #===
        print('VIEW IMAGES')
    def viewContours(self): #===
        print('VIEW CONTOURS')

class doubleListItem(QListWidgetItem):
    '''This is a ListWidgetItem that contains two objects.'''
    def __init__(self, object1, object2, name=None, colors=True):
        QListWidgetItem.__init__(self)
        self.object1 = object1
        self.object2 = object2
        self.loadDetails(name,colors)
    def loadDetails(self, name, colors):
        if not name:
            try:
                self.setText(self.object1.name)
            except:
                self.setText('Unknown name')
        if colors == True and self.object1 != self.object2:
            self.setBackground(QColor('red'))
    def clicked(self): #===
        print('doubleListItem clicked!')
        if type(self.object1).__name__ == 'Section':
            self.attributes = pyrecon.mergeTool.sectionMerge.
            self.images = 
            self.contours =


class seriesLoad(QDialog):
    '''Dialog for loading series files into memory as pyrecon.classes.Series objects'''
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayouts()
    def loadObjects(self):
        self.series1 = browseWidget(browseType='series')
        self.series2 = browseWidget(browseType='series')
        self.closeButton = QPushButton()
        self.closeButton.setText('Load Series')
    def loadFunctions(self):
        self.closeButton.clicked.connect( self.loadClose )
    def loadLayouts(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.series1)
        vbox.addWidget(self.series2)
        vbox.addWidget(self.closeButton)
        self.setLayout(vbox)
    def loadClose(self):
        # Add paths to self.output
        self.output = ( str(self.series1.path.text()), str(self.series2.path.text()) )
        self.close()