from PySide.QtCore import *
from PySide.QtGui import *

from pyrecon.pyreconGUI import *
from pyrecon.main import openSeries
from pyrecon.mergeTool.gui import sectionHandlers, seriesHandlers

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
    def loadFunctions(self):
        self.seriesButton.setText('Load Series')
        self.seriesButton.clicked.connect( self.loadSeries )
    def loadLayout(self):
        mainBox = QHBoxLayout()
        #--- Select What you're looking at (series, section, attributes, images, contours)
        selectBox = QVBoxLayout()
        selectBox.addWidget( self.seriesButton )
        selectBox.addWidget( self.sectionSelect )
        #---
        mainBox.addLayout( selectBox )
        self.setLayout(mainBox)
    def loadSeries(self): #=== add series object as doubleListItem
        seriesDialog = seriesLoad()
        seriesDialog.exec_()
        try:
            self.series1 = openSeries(seriesDialog.output[0])
            self.series2 = openSeries(seriesDialog.output[1])
            seriesItem = doubleListItem(self.series1, self.series2)
            self.sectionSelect.clear() # Remove contents currently in table
            self.sectionSelect.addItem( seriesItem )
            self.seriesButton.setText('Change Series')
            self.loadSections()
        except: #=== Error message
            print('mergeGUI.loadSeries() error') #===
            self.msg = QMessageBox()
            self.msg.setText('Invalid series paths!')
            self.msg.exec_()
    def loadSections(self):
        self.sectionSelect.itemDoubleClicked.connect( self.itemClicked ) # What to do when item doubleclicked
        for i in range( len(self.series1.sections) ):
            sectionItem = doubleListItem( self.series1.sections[i], self.series2.sections[i] )
            self.sectionSelect.addItem( sectionItem )
    def itemClicked(self, item): #===
        item.clicked()
        self.parentWidget().parentWidget().setCentralWidget(item.resolution) # parentWidget() is DockWidget, parentWidget()x2 is MainWindow

class doubleListItem(QListWidgetItem):
    '''This is a ListWidgetItem that contains two objects.'''
    def __init__(self, object1, object2, name=None, colors=True):
        QListWidgetItem.__init__(self)
        self.object1 = object1
        self.object2 = object2
        self.resolution = None # Holds the conflict resolution wrapper
        self.loadDetails(name,colors)
    def loadDetails(self, name, colors):
        if not name:
            try:
                self.setText(self.object1.name)
            except:
                self.setText('Unknown name')
        if colors == True and self.object1 != self.object2:
            self.setBackground(QColor('red'))
    def clicked(self): #=== add series resolution
        if self.object1.__class__.__name__ == 'Section':
            self.resolution = sectionHandlers.sectionWrapper(self.object1, self.object2)
        #     self.attributes = pyrecon.mergeTool.sectionMerge.mergeAttributes(
        #         self.object1, self.object2, handler=sectionHandlers.sectionAttributes)
        #     self.images = pyrecon.mergeTool.sectionMerge.mergeImages(
        #         self.object1, self.object2, handler=sectionHandlers.sectionImages)
        #     self.contours = pyrecon.mergeTool.sectionMerge.mergeContours(
        #         self.object1, self.object2, handler=sectionHandlers.sectionContours)
        elif self.object1.__class__.__name__ == 'Series':
            print ('Series item doubleclicked, placeholder for ser conflict resolution') #===

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