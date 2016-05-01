from PySide.QtCore import *
from PySide.QtGui import *

from pyrecon import openSeries
from pyrecon.gui.mergetool_section import SectionMergeWrapper
from pyrecon.gui.mergetool_series import SeriesMergeWrapper
from pyrecon.tools.mergetool import MergeSet, MergeSeries, MergeSection


class PyreconMainWindow(QMainWindow):
    '''Main PyRECONSTRUCT window.'''
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setWindowTitle('MergeTool')
        self.show()
        newSize = QDesktopWidget().availableGeometry().size() / 4
        self.resize( newSize )
        self.statusBar().showMessage('Ready! Welcome to PyRECONSTRUCT')
        self.loadMergeTool()
    def loadMergeTool(self):
        from pyrecon.tools.mergetool import createMergeSet
        loadDialog = DoubleSeriesLoad() # User locates 2 series
        s1 = openSeries(loadDialog.output[0])
        s2 = openSeries(loadDialog.output[1])
        mSet = createMergeSet( s1, s2 )
        self.setCentralWidget( MergeSetWrapper(mSet) )


class BrowseWidget(QWidget):
    '''Provides a QLineEdit and button for browsing through a file system. browseType can be directory, file or series but defaults to directory.'''
    def __init__(self, browseType='directory'):
        QWidget.__init__(self)
        self.loadObjects(browseType)
        self.loadFunctions(browseType)
        self.loadLayout()
    def loadObjects(self, browseType):
        # Path entry area
        self.path = QLineEdit()
        if browseType == 'directory':
            title = 'Enter or browse path to directory'
        elif browseType == 'series':
            title = 'Enter or browse path'
        else:
            title = 'Enter or browse path to file'
        self.path.setText(title)
        # Browse button
        self.browseButton = QPushButton()
        self.browseButton.setText('Browse')
    def loadFunctions(self, browseType):
        if browseType == 'directory':
            self.browseButton.clicked.connect( self.browseDir )
        elif browseType == 'series':
            self.browseButton.clicked.connect( self.browseSeries )
        else:
            self.browseButton.clicked.connect( self.browseFile )
    def loadLayout(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.path)
        hbox.addWidget(self.browseButton)
        self.setLayout(hbox)
    def browseDir(self):
        dirName = QFileDialog.getExistingDirectory(self)
        self.path.setText( str(dirName) )
    def browseFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "/home/")
        self.path.setText( str(fileName[0]) )
    def browseSeries(self):
        fileName = QFileDialog.getOpenFileName(self, "Open Series", "/home/", "Series File (*.ser)")
        self.path.setText( str(fileName[0]) )


class BrowseOutputDirectory(QDialog):
    '''Starts a popup dialog for choosing a directory in which to save a series'''
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.path = BrowseWidget()
        self.doneBut = QPushButton()
    def loadFunctions(self):
        self.doneBut.setText('Write Series')
        self.doneBut.clicked.connect( self.finish )
    def loadLayout(self):
        main = QVBoxLayout()
        main.addWidget(self.path)
        main.addWidget(self.doneBut)
        self.setLayout(main)
    def finish(self):
        self.output = str(self.path.path.text())
        if 'Enter or browse' not in self.output or self.output == '':
            self.done(1)
        else:
            msg=QMessageBox()
            msg.setText('Invalid output directory: '+str(self.output))
            msg.exec_()
            return


class DoubleSeriesLoad(QDialog):
    '''Dialog for loading series files into memory as pyrecon.classes.Series objects'''
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.series1 = BrowseWidget(browseType='series')
        self.series2 = BrowseWidget(browseType='series')
        self.closeButton = QPushButton()
        self.closeButton.setText('Load Series')
    def loadFunctions(self):
        self.closeButton.clicked.connect( self.loadClose )
    def loadLayout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.series1)
        vbox.addWidget(self.series2)
        vbox.addWidget(self.closeButton)
        self.setLayout(vbox)
    def loadClose(self):
        # Add paths to self.output
        self.output = ( str(self.series1.path.text()),
                        str(self.series2.path.text()) )
        self.close()

if __name__ == '__main__':
    app = QApplication.instance()
    if app == None:
        app = QApplication([])
    a = PyreconMainWindow()
    app.exec_()
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
        #=== Could not figure out how to make new one and replace, use init functions instead
        self.setList.loadObjects()
        self.setList.loadFunctions()
    def save(self):
        # Check for conflicts
        if self.checkConflicts():
            a = BrowseOutputDirectory()
            outpath = a.output
            # Go through all setList items and save to outputdir
            self.writeMergeObjects(outpath)
        #===
        msg = QMessageBox()
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setText('Would you like to close mergeTool?')
        ret = msg.exec_()
        if ret == QMessageBox.Yes:
            self.parentWidget().close()
            self.parentWidget().parentWidget().done(1) #=== doesnt work from MainWindow
        elif ret == QMessageBox.No:
            return

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
        self.refreshAll()
    def refreshAll(self): #=== may freeze with higher num items?
        '''Refreshes (item.refresh()) all items in the list'''
        for i in range( self.count() ):
            self.item(i).refresh()
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
    def quickMergeA(self, items):
        '''Selects A (left) version for all conflicts in items.'''
        for item in items:
            if item.merge.__class__.__name__ == 'MergeSection':
                item.resolution.attributes.chooseLeft.click()
                item.resolution.images.chooseLeft.click()
                item.resolution.contours.onlyAContours()
            elif item.merge.__class__.__name__ == 'MergeSeries':
                item.resolution.attributes.chooseLeft.click()
                item.resolution.contours.chooseLeft.click()
                item.merge.zcontours = item.merge.series1.zcontours #===
            item.refresh()

    def quickMergeB(self, items):
        '''Selects B (right) version for all conflicts in items.'''
        for item in items:
            if item.merge.__class__.__name__ == 'MergeSection':
                item.resolution.attributes.chooseRight.click()
                item.resolution.images.chooseRight.click()
                item.resolution.contours.onlyBContours()
            elif item.merge.__class__.__name__ == 'MergeSeries':
                item.resolution.attributes.chooseRight.click()
                item.resolution.contours.chooseRight.click()
                item.merge.zcontours = item.merge.series2.zcontours #===
            item.refresh()
    def quickMergeABContsA(self, items): #===
        '''This completes the merge resolution by selecting the A (left) version of non-contour conflicts (attributes & images). For contour conflicts, this selects BOTH (left & right) for overlaps and uniques.'''
        for item in items:
            if item.merge.__class__.__name__ == 'MergeSection':
                item.resolution.attributes.chooseLeft.click()
                item.resolution.images.chooseLeft.click()
                item.resolution.contours.allContours()
            elif item.merge.__class__.__name__ == 'MergeSeries':
                item.resolution.attributes.chooseLeft.click()
                item.resolution.contours.chooseLeft.click()
                # zconts
                item_1_uniques, item_2_uniques, ovlps = item.merge.getCategorizedZContours()
                item.merge.zcontours = item_1_uniques+item_2_uniques+ovlps
            item.refresh()
    def quickMergeABContsB(self, items): #===
        '''This completes the merge resolution by selection the B (right) version of non-contour conflicts (attributes & images). For contour conflicts, this selects BOTH (left & right) for overlaps and uniques.'''
        for item in items:
            if item.merge.__class__.__name__ == 'MergeSection':
                item.resolution.attributes.chooseRight.click()
                item.resolution.images.chooseRight.click()
                item.resolution.contours.allContours()
            elif item.merge.__class__.__name__ == 'MergeSeries':
                item.resolution.attributes.chooseRight.click()
                item.resolution.contours.chooseRight.click()
                # zconts
                item_1_uniques, item_2_uniques, ovlps = item.merge.getCategorizedZContours()
                item.merge.zcontours = item_1_uniques+item_2_uniques+ovlps
            item.refresh()

class MergeSetListItem(QListWidgetItem):
    '''This is a specialized QListWidgetItem that contains either a MergeSection or MergeSeries object and the widget used for its resolution'''
    def __init__(self, MergeObject):
        QListWidgetItem.__init__(self)
        self.merge = MergeObject
        self.resolution = None
        self.loadDetails()
        self.refresh() # update colors
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
    def clicked(self):
        if self.merge.isDone():
            self.setBackground(QColor('lightgreen'))
        elif self.merge.doneCount() > 0:
            self.setBackground(QColor('yellow'))
        else:
            self.setBackground(QColor('red'))
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
        elif self.resolution.doneCount() > 0:
            self.setBackground(QColor('yellow'))
        else:
            self.setBackground(QColor('red'))

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


def start():
    """Begin GUI application (pyrecon.gui.main)"""
    app = QApplication.instance()
    if app is None:  # Create QApplication if doesn"t exist
        app = QApplication([])
    gui = PyreconMainWindow()
    app.exec_()  # Start event-loop

