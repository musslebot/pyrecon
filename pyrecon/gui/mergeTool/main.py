from PySide.QtCore import *
from PySide.QtGui import *

from pyrecon.main import openSeries
import pyrecon.tools.handleXML as xml
from pyrecon.gui.mergeTool.sectionHandlers import SectionMergeWrapper
from pyrecon.gui.mergeTool.seriesHandlers import SeriesMergeWrapper
from pyrecon.tools.mergeTool.main import MergeSet

class MergeSetWrapper(QWidget):
    '''This class is a single widget that contains all necessary widgets for resolving conflicts in a MergeSet.'''
    def __init__(self, MergeSet):
        QWidget.__init__(self)
        self.setWindowTitle('PyRECONSTRUCT mergeTool')
        self.merge = MergeSet
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.loadResolutions()
        #=== create slot that links with MergeSetList to update current resolutionStack index
    def loadObjects(self):
        self.navigator = MergeSetNavigator(self.merge) # Buttons and list of MergeObjects
        self.resolutionStack = QStackedWidget() # Contains all of the resolution wrappers
    def loadFunctions(self):
        #=== connect self.resolutionStack.setCurrent index to MergeSetList.itemClicked
        return
    def loadLayout(self):
        container = QHBoxLayout()
        container.addWidget(self.navigator)
        container.addWidget(self.resolutionStack)
        self.setLayout(container)
    def loadResolutions(self):
        if self.merge is not None:
            print 'loading resolutions into stack'
            for itemIndex in range( self.navigator.setList.count() ):
                self.resolutionStack.addWidget( self.navigator.setList.item(itemIndex).resolution )
            self.resolutionStack.setCurrentIndex(0)
        else:
            self.navigator.load() #===

class MergeSetNavigator(QWidget):
    '''This class provides buttons for loading and saving MergeSets as well as a list for choosing current conflict to manage.'''
    def __init__(self, MergeSet):
        QWidget.__init__(self)
        self.merge = MergeSet
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.loadButton = QPushButton('&Load')
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
    def save(self): #===
        print 'MergeSetNavigator.save()'
        # Load BrowseOutputDir widget #===

class MergeSetList(QListWidget):
    '''This class is a specialized QListWidget that contains MergeSetListItems.'''
    def __init__(self, MergeSet):
        QListWidget.__init__(self)
        self.merge = MergeSet
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        #=== make signal that connects to MergeSetWrapper to load new resolution window
    def loadObjects(self):
        # Load MergeObjects into list
        self.addItem( MergeSetListItem(self.merge.seriesMerge) ) # Load MergeSeries
        for MergeSection in self.merge.sectionMerges: # Load MergeSections
            self.addItem( MergeSetListItem(MergeSection) )
    def loadFunctions(self): #===
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # What to do when item clicked?
        self.itemClicked.connect( self.clicked ) #===
        # What to do when item doubleClicked?
        self.itemDoubleClicked.connect( self.doubleClicked ) #===
    def loadLayout(self):
        return
    def clicked(self, item): #===
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
        if self.merge.__class__.__name__ == 'MergeSection':
            self.resolution = SectionMergeWrapper(self.merge)
        elif self.merge.__class__.__name__ == 'MergeSeries':
            self.resolution = SeriesMergeWrapper(self.merge)
        else:
            print 'Unknown resolution type, could not make wrapper'
    def clicked(self):
        print 'MergeSetListItem.clicked()' #===
        if not self.merge.isDone():
            self.setBackground(QColor('yellow'))
        else:
            self.setBackground(QColor('lightgreen'))
    def doubleClicked(self):
        print 'MergeSetListItem.doubleClicked()'
        # Necessary? #===