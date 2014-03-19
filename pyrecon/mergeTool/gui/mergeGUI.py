from PySide.QtCore import *
from PySide.QtGui import *

from pyrecon.pyreconGUI import *
from pyrecon.main import openSeries
#===
class testWidget2(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.b1 = QPushButton()
        self.b2 = QPushButton()
        self.b3 = QPushButton()
    def loadFunctions(self):
        self.b1.setText('One')
        self.b2.setText('Two')
        self.b3.setText('Three')
        for but in [self.b1, self.b2, self.b3]:
            but.clicked.connect( self.butClick )
    def loadLayout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.b1)
        vbox.addWidget(self.b2)
        vbox.addWidget(self.b3)
        self.setLayout(vbox)
    def butClick(self):
        if self.sender() == self.b1:
            print('BUTTON 1')
        elif self.sender() == self.b2:
            print('BUTTON 2')
        elif self.sender() == self.b3:
            print('BUTTON 3')
#===
class mergeSelection(QWidget):
    '''Select what section/attributes to look at.'''
    def __init__(self, parent=None):
        print('Loading merge selection widget') #=== NOT SHOWING
        QWidget.__init__(parent=parent)
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
        print('LOADED FUNCTIONS FOR MERGE SELECTION') #===
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
    def loadSeries(self):
        seriesDialog = seriesLoad()
        seriesDialog.exec_()
        self.series1 = openSeries(seriesDialog.output[0])
        self.series2 = openSeries(seriesDialog.output[1])
        self.loadSections(self.series1, self.series2)
    def loadSections(self): #===
        print('Loading sections into table...') #===
        for i in range( len(series1.sections) ):
            sectionItem = doubleSectionListItem( series1.sections[i],series2.sections[i] )
            self.sectionSelect.addItem( sectionItem )
            print 'added:',sectionItem.section1 #===
    def viewAttributes(self): #===
        print('VIEW ATTRIBUTES')
    def viewImages(self): #===
        print('VIEW IMAGES')
    def viewContours(self): #===
        print('VIEW CONTOURS')

class doubleSectionListItem(QListWidgetItem):
    def __init__(self, section1, section2):
        QListWidgetItem.__init__(self)
        self.section1 = section1
        self.section2 = section2
        self.setText(self.section1.name)
        if self.section1 != self.section2:
            self.setBackground(QColor('red'))
    def clicked(self): #===
        print('SectionListItem clicked!')

class seriesLoad(QDialog):
    '''Dialog for loading series files into memory as pyrecon.classes.Series objects'''
    def __init__(self):
        print('seriesLoad Dialog init') #===
        QDialog.__init__(self)
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