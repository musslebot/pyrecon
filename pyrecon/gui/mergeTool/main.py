from PySide.QtCore import *
from PySide.QtGui import *

from pyrecon.main import openSeries
import pyrecon.tools.handleXML as xml
from pyrecon.gui.mergeTool.sectionHandlers import SectionMergeWrapper
from pyrecon.gui.mergeTool.seriesHandlers import SeriesMergeWrapper
from pyrecon.tools.mergeTool.main import MergeSet

class MergeSetWrapper(QWidget):
    '''This class is a single widget that contains all necessary widgets for resolving conflicts in a MergeSet and handles the signal/slots between them.'''
    def __init__(self, MergeSet):
        QWidget.__init__(self)
        self.setWindowTitle('PyRECONSTRUCT mergeTool')
        self.merge = MergeSet
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.loadResolutions()
    def loadObjects(self):
        self.navigator = MergeSetNavigator(self.merge) # Buttons and list of MergeObjects
        self.resolutionStack = QStackedWidget() # Contains all of the resolution wrappers
    def loadFunctions(self):
        # QStackedWidget needs to respond to setList.itemClicked
        self.navigator.setList.itemClicked.connect( self.updateCurrent )
    def loadLayout(self):
        container = QHBoxLayout()
        container.addWidget(self.navigator)
        container.addWidget(self.resolutionStack)
        self.setLayout(container)
    def loadResolutions(self):
        if self.merge is not None:
            for itemIndex in range( self.navigator.setList.count() ):
                self.resolutionStack.addWidget( self.navigator.setList.item(itemIndex).resolution )
            self.navigator.setList.item(0).clicked() # Show MergeSeries
    def updateCurrent(self, item):
        '''Updates currently shown resolution based on an item received from self.navigator.setList'''
        self.resolutionStack.setCurrentIndex( self.navigator.setList.indexFromItem(item).row() ) # Get row that the item belongs to

class MergeSetNavigator(QWidget):
    '''This class provides buttons for loading and saving MergeSets as well as a list for choosing current conflict to manage.'''
    def __init__(self, MergeSet):
        QWidget.__init__(self)
        self.merge = MergeSet
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        #=== check if all resolved, if so call .save()
    def loadObjects(self):
        self.loadButton = QPushButton('&Change MergeSet')
        self.loadButton.setMinimumHeight(50)
        self.setList = MergeSetList(self.merge)
        self.saveButton = QPushButton('&Save')
        self.saveButton.setMinimumHeight(50)
    def loadFunctions(self):
        self.loadButton.clicked.connect( self.load )
        self.saveButton.clicked.connect( self.save )
    def loadLayout(self):
        container = QVBoxLayout()
        container.addWidget( self.loadButton )
        container.addWidget( self.setList )
        container.addWidget( self.saveButton )
        self.setLayout(container)
    def load(self): #===
        print 'MergeSetNavigator.load()'
        # Load DoubleSeriesBrowse widget #===
        # set self.setList.merge to loaded DoubleSeries
        # Call MergeSetList.loadObjects with new mergeset
    def save(self): #===
        print 'MergeSetNavigator.save()'
        # Load BrowseOutputDir widget #===
        # Go through all setList items and save to outputdir #===

class MergeSetList(QListWidget):
    '''This class is a specialized QListWidget that contains MergeSetListItems.'''
    def __init__(self, MergeSet):
        QListWidget.__init__(self)
        self.merge = MergeSet
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        # Load MergeObjects into list
        self.addItem( MergeSetListItem(self.merge.seriesMerge) ) # Load MergeSeries
        for MergeSection in self.merge.sectionMerges: # Load MergeSections
            self.addItem( MergeSetListItem(MergeSection) )
    def loadFunctions(self):
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # What to do when item clicked?
        self.itemClicked.connect( self.clicked )
        # What to do when item doubleClicked?
        self.itemDoubleClicked.connect( self.doubleClicked )
    def loadLayout(self):
        return
    def clicked(self, item):
        item.clicked()
    def doubleClicked(self, item): # Take into account, clicked is also called when doubleClicked() #===
        item.doubleClicked()

class MergeSetListItem(QListWidgetItem):
    '''This is a specialized QListWidgetItem that contains either a MergeSection or MergeSeries object and the widget used for its resolution'''
    def __init__(self, MergeObject):
        QListWidgetItem.__init__(self)
        self.merge = MergeObject
        self.resolution = None
        self.loadDetails()
    def loadDetails(self):
        self.setText(self.merge.name)
        self.setFont(QFont("Arial", 14))
        # Resolution (type specific MergeWrapper)
        if self.merge.__class__.__name__ == 'MergeSection':
            self.resolution = SectionMergeWrapper(self.merge)
        elif self.merge.__class__.__name__ == 'MergeSeries':
            self.resolution = SeriesMergeWrapper(self.merge)
        else:
            print 'Unknown resolution type, could not make wrapper'
        # Check status, choose color
        if not self.merge.isDone():
            self.setBackground(QColor('red'))
        else:
            self.setBackground(QColor('lightgreen'))
    def clicked(self):
        if self.merge.isDone():
            self.setBackground(QColor('lightgreen'))
        else:
            self.setBackground(QColor('yellow'))
    def doubleClicked(self):
        print 'MergeSetListItem.doubleClicked()'
        # Necessary? #===