from PySide.QtCore import *
from PySide.QtGui import *

import pyrecon.handleXML as xml
from pyrecon.pyreconGUI import *
from pyrecon.main import openSeries
from pyrecon.mergeTool.gui import sectionHandlers, seriesHandlers

class mergeSelection(QWidget):
    '''Select what section/series to look at.'''
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.loadButton = QPushButton()
        self.loadButton.setMinimumHeight(50)
        self.finishedButton = QPushButton()
        self.finishedButton.setMinimumHeight(50)
        self.mergeSelect = QListWidget()
    def loadFunctions(self):
        self.loadButton.setText('&Load Series')
        self.loadButton.clicked.connect( self.loadSeries )
        self.finishedButton.setText('&Finish Merge') 
        self.finishedButton.clicked.connect( self.finishMerge )
        # What to do when an item is clicked
        self.mergeSelect.setSelectionMode( QAbstractItemView.ExtendedSelection ) #===
        self.mergeSelect.itemClicked.connect( self.itemClicked )
        self.mergeSelect.itemDoubleClicked.connect( self.itemDoubleClicked ) #===
        # Hide list and finish button until series successfully loaded
        self.mergeSelect.hide()
        self.finishedButton.hide()
    def loadLayout(self):
        mainBox = QHBoxLayout()
        #--- Select What you're looking at (series, section, attributes, images, contours)
        selectBox = QVBoxLayout()
        selectBox.addWidget( self.loadButton )
        selectBox.addWidget( self.mergeSelect )
        selectBox.addWidget( self.finishedButton )
        #---
        mainBox.addLayout( selectBox )
        self.setLayout(mainBox)
    def loadSeries(self):
        # Open dialog for entering/browsing series paths
        seriesDialog = doubleSeriesLoad()
        seriesDialog.exec_()
        # Process dialog arguments
        self.series1 = openSeries(seriesDialog.output[0])
        self.series2 = openSeries(seriesDialog.output[1])
        # Clear current series
        self.mergeSelect.clear() # Delete contents currently in table
        # Make new series item
        seriesItem = mergeItem(self.series1, self.series2)
        self.mergeSelect.addItem( seriesItem )
        # Add mergeItem's resolution widget to mainWindow's resolutionStack
        self.parentWidget().parentWidget().resolutionStack.addWidget(seriesItem.resolution)
        self.loadButton.setText('Change Series')
        # Load sections as mergeItems
        self.loadSections()
        # Display buttons
        self.mergeSelect.show() 
        self.finishedButton.show()
    def loadSections(self):
        for i in range( len(self.series1.sections) ):
            sectionItem = mergeItem( self.series1.sections[i], self.series2.sections[i] )
            self.mergeSelect.addItem( sectionItem )
            # Add mergeItem's resolution widget to mainWindow's resolutionStack
            self.parentWidget().parentWidget().resolutionStack.addWidget(sectionItem.resolution)
    def itemClicked(self, item):
        '''clicking a mergeItem opens a detailed conflict resolution window for the user to interact with'''
        self.parentWidget().parentWidget().resolutionStack.setCurrentWidget(item.resolution)
        item.clicked()
    def itemDoubleClicked(self, item):
        '''double-clicking a mergeItem displays a small menu allowing the user to use quick merge options.'''
        items = self.mergeSelect.selectedItems()
        # Make menu
        dcMenu = QMenu()
        # - Options for when doubleClicked
        selAAction = QAction(QIcon(), 'select A all', self) # Select the A versions of all
        selBAction = QAction(QIcon(), 'select B all', self) # Select the B versions of all
        selABContsActionA = QAction(QIcon(), 'select both contours, rest A', self) # Select both for contour conflicts, A for rest
        selABContsActionB = QAction(QIcon(), 'select both contours, rest B', self) # Select both for contour conflicts, B for rest
        # - ToolTips
        selAAction.setToolTip('Select the A version of everything for this item(s)')
        selBAction.setToolTip('Select the B version of everything for this item(s)')
        selABContsActionA.setToolTip('Select A&&B contours, A for everything else')
        selABContsActionB.setToolTip('Select A&&B contours, B for everything else')
        # - Add options to menu
        dcMenu.addAction(selAAction)
        dcMenu.addAction(selBAction)
        dcMenu.addAction(selABContsActionA)
        dcMenu.addAction(selABContsActionB)

        # Pop open menu for user selection
        action = dcMenu.exec_( QCursor.pos() )

        # Perform selected action
        if action == selAAction:
            self.quickMergeA(items)
        elif action == selBAction:
            self.quickMergeB(items)
        elif action == selABContsActionA:
            self.quickMergeABContsA(items)
        elif action == selABContsActionB:
            self.quickMergeABContsB(items)
    def quickMergeA(self, items):
        '''Selects A version for all conflicts in items.'''
        for item in items:
            if item.object1.__class__.__name__ == 'Section':
                # Select section A's attributes/image
                item.resolution.attributes.pick1.click()
                item.resolution.images.pick1.click()
                # Contours
                # - Select & Move uniqueA contours to output
                item.resolution.contours.inUniqueA.selectAll()
                item.resolution.contours.moveSelectedA.click()
                # - Resolve conflicts (choose A)
                item.resolution.contours.inOvlp.selectAll()
                conflicts = item.resolution.contours.inOvlp.selectedItems()
                for conflict in conflicts:
                    conflict.forceResolution(1) # Choose contour A
                # - - Move to output
                item.resolution.contours.moveSelectedO.click()
                # Click merge button (conflicts resolved)
                item.resolution.contours.finish()
            elif item.object1.__class__.__name__ == 'Series':
                item.resolution.attributes.pick1.click()
                item.resolution.contours.pick1.click()
                # ZContours
                item.resolution.zcontours.output = item.resolution.zcontours.uniqueA+item.resolution.zcontours.merged
                # - update lab
                item.resolution.zcontours.lab.setText('Only section A\'s zcontours were kept, as per the quickmerge option.')
    def quickMergeB(self, items):
        '''Selects B version for all conflicts in items.'''
        for item in items:
            if item.object1.__class__.__name__ == 'Section':
                # Select section B's attributes/image
                item.resolution.attributes.pick2.click()
                item.resolution.images.pick2.click() 
                # Contours
                # - Select & Move uniqueB contours to output
                item.resolution.contours.inUniqueB.selectAll()
                item.resolution.contours.moveSelectedB.click()
                # - Resolve conflicts (choose B)
                item.resolution.contours.inOvlp.selectAll()
                conflicts = item.resolution.contours.inOvlp.selectedItems()
                for conflict in conflicts:
                    conflict.forceResolution(2) # Choose contour B
                # - - Move to output
                item.resolution.contours.moveSelectedO.click()
                # Click merge button (conflicts resolved)
                item.resolution.contours.finish()
            elif item.object1.__class__.__name__ == 'Series':
                item.resolution.attributes.pick2.click()
                item.resolution.contours.pick2.click()
                # ZContours... all but A
                item.resolution.zcontours.output = item.resolution.zcontours.uniqueA+item.resolution.zcontours.merged
                # - update lab
                item.resolution.zcontours.lab.setText('Only section B\'s zcontours were kept, as per the quickmerge option.')
    def quickMergeABContsA(self, items):
        '''This completes the merge resolution by selecting the A version of non-contour conflicts. For contour conflicts, this selects BOTH for overlaps and also includes uniques from A and B.'''
        for item in items:
            if item.object1.__class__.__name__ == 'Section':
                # Select section A's attributes/image
                item.resolution.attributes.pick1.click()
                item.resolution.images.pick1.click() 
                # Contours
                # - Select & Move uniqueA contours to output
                item.resolution.contours.inUniqueA.selectAll()
                item.resolution.contours.moveSelectedA.click()
                # - Select & Move uniqueB contours to output
                item.resolution.contours.inUniqueB.selectAll()
                item.resolution.contours.moveSelectedB.click()
                # - Resolve conflicts (choose BOTH)
                item.resolution.contours.inOvlp.selectAll()
                conflicts = item.resolution.contours.inOvlp.selectedItems()
                for conflict in conflicts:
                    conflict.forceResolution(3) # Choose BOTH contours
                # - - Move to output
                item.resolution.contours.moveSelectedO.click()
                # Click merge button (conflicts resolved)
                item.resolution.contours.finish()
            elif item.object1.__class__.__name__ == 'Series':
                item.resolution.attributes.pick1.click()
                item.resolution.contours.pick1.click()
                # ZContours are default
    def quickMergeABContsB(self, items):
        '''This completes the merge resolution by selection the B version of non-contour conflicts. For contour conflicts, this selects BOTH for overlaps and also includes uniques from A and B.'''
        for item in items:
            if item.object1.__class__.__name__ == 'Section':
                item.resolution.attributes.pick2.click()
                item.resolution.images.pick2.click() 
                # Contours
                # - Select & Move uniqueA contours to output
                item.resolution.contours.inUniqueA.selectAll()
                item.resolution.contours.moveSelectedA.click()
                # - Select & Move uniqueB contours to output
                item.resolution.contours.inUniqueB.selectAll()
                item.resolution.contours.moveSelectedB.click()
                # - Resolve conflicts (choose BOTH)
                item.resolution.contours.inOvlp.selectAll()
                conflicts = item.resolution.contours.inOvlp.selectedItems()
                for conflict in conflicts:
                    conflict.forceResolution(3) # Choose BOTH contours
                # - - Move to output
                item.resolution.contours.moveSelectedO.click()
                # Click merge button (conflicts resolved)
                item.resolution.contours.finish()
                # - - Move to output
            elif item.object1.__class__.__name__ == 'Series':
                item.resolution.attributes.pick2.click()
                item.resolution.contours.pick2.click()
                # ZContours are default
    def finishMerge(self):
        # Check if conflicts are resolved #=== make more comprehensive?
        ret = None
        for i in range(self.mergeSelect.count()):
            if self.mergeSelect.item(i).background() == QColor('red') or self.mergeSelect.item(i).background() == QColor('yellow'):
                msg = QMessageBox()
                msg.setText('Not all conflicts were resolved (red or yellow background).')
                msg.setInformativeText('Would you like to default unresolved conflicts to the first loaded series?')
                msg.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel)
                ret = msg.exec_()
                break
        if ret is None or ret == QMessageBox.Ok:
            dir = outdirBrowse()
            dir.exec_()
            path = dir.output
            for i in range(self.mergeSelect.count()):
                pyreconObject = self.mergeSelect.item(i).resolution.toObject()
                if pyreconObject.__class__.__name__ == 'Section':
                    xml.writeSection(pyreconObject, path)
                elif pyreconObject.__class__.__name__ == 'Series':
                    xml.writeSeries(pyreconObject, path)
        elif ret == QMessageBox.Cancel:
            return

class mergeItem(QListWidgetItem):
    '''This is a ListWidgetItem that contains two objects and their resolution handler.'''
    def __init__(self, object1, object2, name=None, colors=True):
        QListWidgetItem.__init__(self)
        self.setFont(QFont("Arial", 14))
        self.object1 = object1
        self.object2 = object2
        self.resolution = None # Holds the conflict resolution wrapper
        self.loadDetails(name,colors)
    def loadDetails(self, name, colors):
        # Load name to display in list
        if not name:
            try:
                if self.object1.__class__.__name__ == 'Series':
                    self.setText(self.object1.name+'.ser')
                else:
                    self.setText(self.object1.name)
            except:
                self.setText('Unknown name')
        # Determine color of background
        if colors == True and self.object1 != self.object2:
            self.setBackground(QColor('red'))
        elif colors == True and self.object1 == self.object2:
            self.setBackground(QColor('lightgreen'))
        # Load resolution wrapper
        if self.object1.__class__.__name__ == 'Section':
            self.resolution = sectionHandlers.sectionWrapper(self.object1, self.object2, parent=self)
        elif self.object1.__class__.__name__ == 'Series':
            self.resolution = seriesHandlers.seriesWrapper(self.object1,self.object2, parent=self)
    def isResolved(self):
        '''Returns True if all resolutions have output != None.'''
        return self.resolution.isResolved()
    def clicked(self, button=None):
        if not self.isResolved():
            self.setBackground(QColor('yellow'))

class outdirBrowse(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.path = browseWidget()
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
        self.close()
