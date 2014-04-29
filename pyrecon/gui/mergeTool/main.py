from PySide.QtCore import *
from PySide.QtGui import *

from pyrecon.main import openSeries
from pyrecon.tools.mergeTool.main import MergeSet, MergeSeries, MergeSection

from pyrecon.gui.main import BrowseOutputDirectory, DoubleSeriesLoad
from pyrecon.gui.mergeTool.sectionHandlers import SectionMergeWrapper
from pyrecon.gui.mergeTool.seriesHandlers import SeriesMergeWrapper

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
    def load(self):
        # Load DoubleSeriesBrowse widget
        loadDialog = DoubleSeriesLoad()
        s1,s2 = openSeries(loadDialog.output[0]), openSeries(loadDialog.output[1]) # Create Series objects from path
        # Make MergeSeries, MergeSection objects
        mSeries = MergeSeries(s1,s2)
        mSections = []
        for i in range(len(s1.sections)):
            mSections.append( MergeSection(s1.sections[i],s2.sections[i]) )
        # Clear setList
        self.setList.clear()
        # Create setList with new MergeSet
        self.setList.merge = MergeSet(mSeries, mSections)
        #=== Could not figure out how to make new one from class, use functions instead
        self.setList.loadObjects()
        self.setList.loadFunctions()
        self.setList.loadLayout()
    def save(self):
        # Check for conflicts
        if self.checkConflicts():
            a = BrowseOutputDirectory()
            outpath = a.output
            # Go through all setList items and save to outputdir
            self.writeMergeObjects(outpath)
    def checkConflicts(self):
        unresolved_list = [] # list of unresolved conflict names
        for i in range(self.setList.count()):
            item = self.setList.item(i)
            if item.isResolved():
                continue
            else:
                unresolved_list.append(item.merge.name)
        # Bring up dialog for unresolved conflicts
        if len(unresolved_list) > 0:
            msg = QMessageBox()
            msg.setText('Not all conflicts were resolved (red/yellow):\n'+'\n'.join(unresolved_list))
            msg.setInformativeText('Would you like to default unresolved conflicts to the first (left) series for these conflicts?')
            msg.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel)
            ret = msg.exec_()
            return (ret == QMessageBox.Ok)
        else:
            return True
    def writeMergeObjects(self, outpath):
        self.merge.writeMergeSet(outpath)

class MergeSetList(QListWidget):
    '''This class is a specialized QListWidget that contains MergeSetListItems.'''
    def __init__(self, MergeSet):
        QListWidget.__init__(self)
        self.merge = MergeSet
        self.loadObjects()
        self.loadFunctions()
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
    def clicked(self, item):
        item.clicked()
    def doubleClicked(self, item):
        '''double-clicking a mergeItem displays a small menu allowing the user to use quick merge options.'''
        items = self.selectedItems()
        # Pop open menu for user selection
        quickmerge = QuickMergeMenu()
        action = quickmerge.exec_( QCursor.pos() )
        # Perform selected action
        if action == quickmerge.selAAction:
            self.quickMergeA(items)
        elif action == quickmerge.selBAction:
            self.quickMergeB(items)
        elif action == quickmerge.selABContsActionA:
            self.quickMergeABContsA(items)
        elif action == quickmerge.selABContsActionB:
            self.quickMergeABContsB(items)
    def quickMergeA(self, items): #===
        '''Selects A version for all conflicts in items.'''
        for item in items:
            #=== perform quickmerge function
            return
    def quickMergeB(self, items): #===
        '''Selects B version for all conflicts in items.'''
        for item in items:
            #=== perform quickmerge function
            return
    def quickMergeABContsA(self, items): #===
        '''This completes the merge resolution by selecting the A version of non-contour conflicts. For contour conflicts, this selects BOTH for overlaps and also includes uniques from A and B.'''
        for item in items:
            #=== perform quickmerge function
            return
    def quickMergeABContsB(self, items): #===
        '''This completes the merge resolution by selection the B version of non-contour conflicts. For contour conflicts, this selects BOTH for overlaps and also includes uniques from A and B.'''
        for item in items:
            #=== perform quickmerge function
            return

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
    def isResolved(self):
        '''Returns true if merge conflicts are resolved.'''
        return self.resolution.merge.isDone()
    def refresh(self): #===
        '''Update colors'''
        if self.isResolved():
            self.setBackground(QColor('lightgreen'))

class QuickMergeMenu(QMenu):
    def __init__(self, parent=None):
        QMenu.__init__(self, parent)
        self.setTitle('Quick-merge')
        self.createActions()
        self.addActions()
    def createActions(self):
        # - Options for when doubleClicked
        self.selAAction = QAction(QIcon(), 'Select all left', self) # Select the A versions of all
        self.selBAction = QAction(QIcon(), 'Select all right', self) # Select the B versions of all
        self.selABContsActionA = QAction(QIcon(), 'Select both contours, left atts and images', self) # Select both for contour conflicts, A for rest
        self.selABContsActionB = QAction(QIcon(), 'Select both contours, right atts and images', self) # Select both for contour conflicts, B for rest
        # - ToolTips
        self.selAAction.setToolTip('Select the left version of everything for this item(s)')
        self.selBAction.setToolTip('Select the right version of everything for this item(s)')
        self.selABContsActionA.setToolTip('Select left&&right contours, left for images and attributes')
        self.selABContsActionB.setToolTip('Select left&&right contours, right for images and attributes')
    def addActions(self):
        # - Add options to menu
        self.addAction(self.selAAction)
        self.addAction(self.selBAction)
        self.addAction(self.selABContsActionA)
        self.addAction(self.selABContsActionB)