from PySide.QtCore import *
from PySide.QtGui import *

import pyrecon.handleXML as xml
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
        self.mergeSelect.itemClicked.connect( self.itemClicked )
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
        seriesDialog = seriesLoad()
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
        self.parentWidget().parentWidget().resolutionStack.setCurrentWidget(item.resolution)
    def finishMerge(self): #===
        # Check if conflicts are resolved
        for i in range(self.mergeSelect.count()): #=== yellow?
            if self.mergeSelect.item(i).background() == QColor('red') or self.mergeSelect.item(i).background() == QColor('yellow'):
                msg = QMessageBox()
                msg.setText('Not all conflicts were resolved (red or yellow background).')
                msg.setInformativeText('Would you like to default unresolved conflicts to the first loaded series?')
                msg.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel)
                ret = msg.exec_()
                break
        if ret == QMessageBox.Ok:
            dir = outdirBrowse()
            dir.exec_()
            path = dir.output
            print('Output merged series to:',path)
            for i in range(self.mergeSelect.count()):
                pyreconObject = self.mergeSelect.item(i).resolution.toObject()
                print 'pObject:',pyreconObject.__dict__
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
        # Load resolution wrapper
        if self.object1.__class__.__name__ == 'Section':
            self.resolution = sectionHandlers.sectionWrapper(self.object1, self.object2)
        elif self.object1.__class__.__name__ == 'Series':
            self.resolution = seriesHandlers.seriesWrapper(self.object1,self.object2)

class seriesLoad(QDialog):
    '''Dialog for loading series files into memory as pyrecon.classes.Series objects'''
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.series1 = browseWidget(browseType='series')
        self.series2 = browseWidget(browseType='series')
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
        self.output = ( str(self.series1.path.text()), str(self.series2.path.text()) )
        self.close()

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

