from PySide import QtCore, QtGui
from pyrecon.tools import classes, mergeTool
import sys

def main():
    app = QtGui.QApplication(sys.argv)
    a = mainContainer() # Doesn't work unless set to a variable for some reason
    sys.exit( app.exec_() )

class mainContainer(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,600,300)
        self.setWindowTitle('RECONSTRUCT MERGETOOL')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        self.series1 = None
        self.series2 = None
        
        self.loadFunctionalObjects()
        self.loadLayout()
        self.loadFunctionality()
        self.show()

    def loadFunctionalObjects(self):
        self.seriesPath1 = QtGui.QLineEdit()
        self.browseSeriesFile1 = QtGui.QPushButton()
        self.seriesPath2 = QtGui.QLineEdit()
        self.browseSeriesFile2 = QtGui.QPushButton()
        self.loadSeries = QtGui.QPushButton()
        self.seriesFileConflicts = QtGui.QPushButton()
        self.sectionFileConflicts = QtGui.QPushButton()
        self.infoLabel = QtGui.QLabel()                                         
        self.finishButton = QtGui.QPushButton()
        
    def loadFunctionality(self):
        self.seriesPath1.setText('Please enter or browse for path to primary series')
        self.seriesPath2.setText('Please enter or browse for path to secondary series')
        self.seriesPath1.setText('/home/michaelm/Documents/Test Series/BBCHZ/BBCHZ.ser') #===
        self.seriesPath2.setText('/home/michaelm/Documents/Test Series/BBCHZ2/BBCHZ.ser') #===
        
        self.seriesPath1.setAlignment(QtCore.Qt.AlignCenter)
        self.seriesPath2.setAlignment(QtCore.Qt.AlignCenter)
        self.browseSeriesFile1.setText('Browse')
        self.browseSeriesFile2.setText('Browse')
        self.browseSeriesFile1.clicked.connect( self.browseSeries )
        self.browseSeriesFile2.clicked.connect( self.browseSeries )
        self.loadSeries.setText('Load Series\nFiles')
        self.loadSeries.clicked.connect( self.loadSer )
        
        self.seriesFileConflicts.setText('Series File (.ser)\nConflicts')
        self.sectionFileConflicts.setText('Section File (.#)\nConflicts')
        self.seriesFileConflicts.setFlat(True)
        self.sectionFileConflicts.setFlat(True)
        
        self.finishButton.setText('COMPLETE MERGE\nAND\nOUTPUT NEW SERIES')
        self.finishButton.setFlat(True)
        
    def browseSeries(self):
        path = QtGui.QFileDialog.getOpenFileName(self,
                                                 'Load Series',
                                                 '/home/',
                                                 'Series File (*.ser)')
        path = str(path[0])
        if self.sender() == self.browseSeriesFile1: 
            self.seriesPath1.setText(path)
        elif self.sender() == self.browseSeriesFile2:
            self.seriesPath2.setText(path)
        
    def loadLayout(self):
        mainBox = QtGui.QVBoxLayout()
        
        # Series path bars / Browse / load button
        vbox1 = QtGui.QVBoxLayout()
        hboxA = QtGui.QHBoxLayout() # path/browse 1
        hboxA.addWidget( QtGui.QLabel('Primary Series: ') )
        hboxA.addWidget( self.seriesPath1 )
        hboxA.addWidget( self.browseSeriesFile1 )
        hboxA.insertSpacing(0, 25)
        hboxA.insertSpacing(-1, 25)
        hboxB = QtGui.QHBoxLayout() # path/browse 2
        hboxB.addWidget( QtGui.QLabel('Secondary Series: ') )
        hboxB.addWidget( self.seriesPath2 )
        hboxB.addWidget( self.browseSeriesFile2)
        hboxB.insertSpacing(0, 25)
        hboxB.insertSpacing(-1, 25)
        hboxC = QtGui.QHBoxLayout() # Load series button
        hboxC.addWidget( self.loadSeries )
        hboxC.insertSpacing(0, 250)
        hboxC.insertSpacing(-1, 250)
        vbox1.addLayout( hboxA )
        vbox1.addLayout( hboxB )
        vbox1.addLayout( hboxC )
        
        # Series/Section Conflict buttons
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget( self.seriesFileConflicts )
        hbox1.addWidget( self.sectionFileConflicts )
        hbox1.insertSpacing(-1,100)
        hbox1.insertSpacing(0,100)
        
        # Finish and merge button
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget( self.finishButton )
        hbox2.insertSpacing(-1,200)
        hbox2.insertSpacing(0,200)
        
        # Add to mainBox
        mainBox.addLayout(vbox1)
        mainBox.addLayout(hbox1)
        mainBox.addLayout(hbox2)
        self.setLayout( mainBox )
        
    def loadSer(self):
        path1 = str(self.seriesPath1.text())
        path2 = str(self.seriesPath2.text())
        msg = QtGui.QMessageBox(self)
        if '.ser' in path1 and '.ser' in path2:
            okBut = msg.addButton(QtGui.QMessageBox.Ok)
            msg.addButton(QtGui.QMessageBox.Cancel)
            msg.setText('This may take a few moments... please wait after clicking \'OK\'.')
            msg.exec_()
            if msg.clickedButton() == okBut:
                self.series1 = classes.loadSeries(path1)
                self.series2 = classes.loadSeries(path2)
                self.stepTwo()
        else:
            msg.setText('Please enter a correct path to both .ser files!')
            msg.show()
            
    def stepTwo(self):
        self.seriesFileConflicts.setFlat(False)
        self.sectionFileConflicts.setFlat(False)
        self.seriesFileConflicts.clicked.connect( self.seriesConflicts )
        self.sectionFileConflicts.clicked.connect( self.sectionConflicts )
        msg = QtGui.QMessageBox(self)
        msg.setText('Okay, done!\nClick one of the buttons below to resolve conflicts.\n\n**Non-resolved conflicts will default to the state of the primary series.    ')
        msg.show()
    
    def seriesConflicts(self):
        # Requires self. in variable name to be rendered correctly
        self.serWin = seriesConflictWindow(parent=None, pSeries=self.series1, sSeries=self.series2)
    
    def sectionConflicts(self):
        # Requires self. in variable name to be rendered correctly
        self.secWin = sectionConflictWindow(parent=None, pSeries=self.series1, sSeries=self.series2)

class seriesConflictWindow(QtGui.QFrame):
    def __init__(self, parent=None, pSeries=None, sSeries=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,325,300,150)
        self.setWindowTitle('Series File Conflicts')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        self.pSeries = pSeries
        self.sSeries = sSeries
        
        # Returned data when window is closed
        self.mergedAttributes = None
        self.mergedContours = None
        self.mergedZContours = None
        
        self.loadFunctionalObjects()
        self.loadLayout()
        self.loadFunctionality()
        
        
        self.show()
    
    def loadFunctionalObjects(self):
        self.attributesButton = QtGui.QPushButton(self)
        self.contoursButton = QtGui.QPushButton(self)
        self.zcontoursButton = QtGui.QPushButton(self)
        self.closeButton = QtGui.QPushButton(self)
    
    def loadLayout(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.attributesButton)
        vbox.addWidget(self.contoursButton)
        vbox.addWidget(self.zcontoursButton)
        vbox.addWidget(self.closeButton)
        self.setLayout(vbox)
        
    def loadFunctionality(self):
        # Attributes
        self.attributesButton.setText('Attribute\nConflicts')
        self.attributesButton.clicked.connect( self.resolveAttributes )
        # Contours
        self.contoursButton.setText('Contour\nConflicts')
        self.contoursButton.clicked.connect( self.resolveContours )
        # ZContours
        self.zcontoursButton.setText('ZContour\nConflicts')
        self.zcontoursButton.clicked.connect( self.resolveZContours )
        # Close
        self.closeButton.setText('Save and Close')
        self.closeButton.clicked.connect( self.closeWin )
    
    def closeWin(self): #===
        # Update instance data to match resolvers
        try:
            self.mergedAttributes = self.attRes.mergedAttributes
        except:
            print('Choose primary atts===')
            
        try:
            self.mergedContours = self.contRes.mergedContours
        except:
            print('Choose primary conts===')
            
        try:    
            self.mergedZContours = self.zContRes.mergedZContours
        except:
            print('Choose primary zconts===')

        self.close()
        
        #=== still need to update mainContainer
        print('Merged Attributes: '+str(self.mergedAttributes)) # Works
        print('Merged Contours: '+str(self.mergedContours))
        print('Merged ZContours: '+str(self.mergedZContours))
    
    def resolveAttributes(self):
        self.attRes = seriesAttributeResolver(pSeries=self.pSeries, sSeries=self.sSeries)
    
    def resolveContours(self): #===
        print('Contours pressed')
#         self.contRes = 
    
    def resolveZContours(self): #===
        print('ZContours pressed')
#         self.zContRes = 

class sectionConflictWindow(QtGui.QFrame):
    def __init__(self, parent=None, pSeries=None, sSeries=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(300,325,300,150)
        self.setWindowTitle('Section File Conflicts')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        self.pSeries = pSeries
        self.sSeries = sSeries
        
        # Returned objects when close button pressed
        self.mergedAttributes = None
        self.mergedImages = None
        self.mergedContours = None

        self.loadFunctionalObjects()
        self.loadLayout()
        self.loadFunctionality()
        
        
        self.show()
        
    def loadFunctionalObjects(self):
        self.attributesButton = QtGui.QPushButton(self)
        self.imagesButton = QtGui.QPushButton(self)
        self.contoursButton = QtGui.QPushButton(self)
        self.closeButton = QtGui.QPushButton(self)
        
    def loadLayout(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.attributesButton)
        vbox.addWidget(self.imagesButton)
        vbox.addWidget(self.contoursButton)
        vbox.addWidget(self.closeButton)
        self.setLayout(vbox)
        
    def loadFunctionality(self):
        # Attributes
        self.attributesButton.setText('Attribute\nConflicts')
#             self.attributesButton.clicked.connect( self.attributes )
        # ZContours
        self.imagesButton.setText('Image\nConflicts')
#             self.imagesButton.clicked.connect( self.zcontours )
        # Contours
        self.contoursButton.setText('Contour\nConflicts')
#             self.contoursButton.clicked.connect( self.contours )
        # Close
        self.closeButton.setText('Close')
        self.closeButton.clicked.connect( self.closeWin )
    def closeWin(self):
        self.close()
        return 

class seriesAttributeResolver(QtGui.QFrame):
    def __init__(self, parent=None, pSeries=None, sSeries=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,400)
        self.setWindowTitle('Series Attribute Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        mergeTool.mergeSeriesAttributes(pSeries, sSeries, handler=self.serAttHandler)
        self.mergedAttributes = None
        
        self.loadLayout()
        self.show()
        
    def serAttHandler(self, pSeriesAtts, sSeriesAtts, mergedAtts, conflicts):
        self.pSeriesAtts = pSeriesAtts
        self.sSeriesAtts = sSeriesAtts
        
        # Init table
        self.table = QtGui.QTableWidget(len(conflicts)+len(mergedAtts), 1, self)
        self.table.setHorizontalHeaderLabels(['Series Attributes'])
        self.table.setColumnWidth(0,330)
        self.table.itemPressed.connect( self.resolveDetail )
        # Load table items
        row = 0
        for att in conflicts:
            item = QtGui.QTableWidgetItem( str(att) )
            item.setBackground(QtGui.QBrush(QtGui.QColor('pink')))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(row,0,item)
            row+=1
        for att in mergedAtts:
            item = QtGui.QTableWidgetItem( str(att) )
            item.setBackground(QtGui.QBrush(QtGui.QColor('lightgreen')))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(row,0,item)
            row+=1
 
        self.table.show()
        
    def resolveDetail(self, item):
        pink = '#ffc0cb'
        yellow = '#ffff66'
        if item.background().color().name() in [pink, yellow]:
            self.res = textResolveDetail(parent=None, item=item,
                              pItem=self.pSeriesAtts[item.text().replace(' (Primary)', '').replace(' (Secondary)','')],
                              sItem=self.sSeriesAtts[item.text().replace(' (Primary)', '').replace(' (Secondary)','')])
    
    def loadLayout(self):
        self.closeButton = QtGui.QPushButton(self)
        self.closeButton.setText('Save and Close')
        self.closeButton.clicked.connect( self.updateAndClose )
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget( self.table )
        vbox.addWidget( self.closeButton )
        self.setLayout(vbox)
    
    def updateAndClose(self):
        self.mergedAttributes = {}
        for row in range( self.table.rowCount() ):
            itemLabel = self.table.item(row,0).text()
            if '(Secondary)' in itemLabel:
                itemLabel = str(itemLabel.replace(' (Secondary)',''))
                self.mergedAttributes[itemLabel] = self.sSeriesAtts[itemLabel]
            else:
                itemLabel = str(itemLabel.replace(' (Primary)',''))
                self.mergedAttributes[itemLabel] = self.pSeriesAtts[itemLabel]
        self.close()
    
class textResolveDetail(QtGui.QFrame):
    '''Detailed resolver for text-based item conflicts'''
    def __init__(self, parent=None, item=None, pItem=None, sItem=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,200)
        self.setWindowTitle('Text Item Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        self.tableItem = item
        self.pItem = pItem
        self.sItem = sItem
        
        self.loadObjects()
        self.loadLayout()
        self.show()
        
    def loadObjects(self):
        self.pItemLabel = QtGui.QLabel(self)
        self.pItemLabel.setText('Primary Item:\n'+str(self.pItem))
        self.pItemLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.sItemLabel = QtGui.QLabel(self)
        self.sItemLabel.setText('Secondary Item:\n'+str(self.sItem))
        self.sItemLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.choosePri = QtGui.QPushButton(self)
        self.choosePri.setText('Choose Primary Item\n(Default)')
        
        self.chooseSec = QtGui.QPushButton(self)
        self.chooseSec.setText('Choose Secondary Item\n')
        
        for choose in [self.choosePri, self.chooseSec]:
            choose.clicked.connect( self.choose )
    
    def choose(self):
        tableItemLabel = self.tableItem.text().replace(' (Primary)','').replace(' (Secondary)','')
        if self.sender() == self.choosePri:
            self.tableItem.setText(tableItemLabel+' (Primary)')
        else:
            self.tableItem.setText(tableItemLabel+' (Secondary)')
        self.tableItem.setBackground(QtGui.QBrush(QtGui.QColor('yellow')))
        self.close()
            
    def loadLayout(self):
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.pItemLabel)
        hbox1.addWidget(self.sItemLabel)
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.choosePri)
        hbox2.addWidget(self.chooseSec)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)
    
main()

