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
        self.check1 = False # True when serConflict button has been clicked
        self.check2 = False # True when secConflict button has been clicked
        
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
        self.seriesPath1.setText('/home/michaelm/Documents/Test Series/rmtgTest/ser1/BBCHZ.ser') #===
        self.seriesPath2.setText('/home/michaelm/Documents/Test Series/rmtgTest/ser2/BBCHZ.ser') #===
        
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
        self.finishButton.clicked.connect( self.finish )
        
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
        self.seriesFileConflicts.setPalette(QtGui.QPalette(QtGui.QColor('pink')))
        self.sectionFileConflicts.setPalette(QtGui.QPalette(QtGui.QColor('pink')))
        self.seriesFileConflicts.clicked.connect( self.seriesConflicts )
        self.sectionFileConflicts.clicked.connect( self.sectionConflicts )
        msg = QtGui.QMessageBox(self)
        msg.setText('Okay, done!\nClick one of the buttons below to resolve conflicts.\n\n**Non-resolved conflicts will default to the state of the primary series.    ')
        msg.show()
    
    def seriesConflicts(self):
        # Requires self. in variable name to be rendered correctly
        self.serWin = seriesConflictWindow(parent=None, pSeries=self.series1, sSeries=self.series2)
        self.seriesFileConflicts.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.check1 = True
        self.checkConfButs()
        
    def sectionConflicts(self):
        # Requires self. in variable name to be rendered correctly
        self.secWin = sectionConflictWindow(parent=None, pSeries=self.series1, sSeries=self.series2)
        self.sectionFileConflicts.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.check2 = True
        self.checkConfButs()
    
    def checkConfButs(self):
        if self.check1 and self.check2:
            self.finishButton.setFlat(False)
            self.finishButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        
    def finish(self): #===
        # update merged stuff
        # Popup showing which areas are going to be defaulted due to no human resolution
        # ask for output path
        # create new series object
        # push out
        return

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
        self.attributesButton.setPalette(QtGui.QPalette(QtGui.QColor('pink')))
        self.attributesButton.clicked.connect( self.resolveAttributes )
        # Contours
        self.contoursButton.setText('Contour\nConflicts')
        self.contoursButton.setPalette(QtGui.QPalette(QtGui.QColor('pink')))
        self.contoursButton.clicked.connect( self.resolveContours )
        # ZContours
        self.zcontoursButton.setText('ZContour\nConflicts')
        self.zcontoursButton.clicked.connect( self.resolveZContours )
        self.zcontoursButton.setPalette(QtGui.QPalette(QtGui.QColor('pink')))
        # Close
        self.closeButton.setText('Save and Close')
        self.closeButton.clicked.connect( self.closeWin )
    
    def closeWin(self): #===
        # Update instance data to match resolvers
        try:
            self.mergedAttributes = self.attRes.mergedAttributes
        except:
            print('Primary Series Attributes chosen by default')
            
        try:
            self.mergedContours = self.contRes.mergedContours
        except:
            print('Primary Series Contours chosen by default')
            
        try:    
            self.mergedZContours = self.zContRes.mergedZContours
        except:
            print('Primary Series ZContours chosen by default')
            
        self.close()
        
        #=== still need to update mainContainer
        print('Merged Attributes: '+str(self.mergedAttributes)) # Works
        print('Merged Contours: '+str(self.mergedContours))
        print('Merged ZContours: '+str(self.mergedZContours))
    
    def resolveAttributes(self):
        self.attRes = seriesAttributeResolver(pSeries=self.pSeries, sSeries=self.sSeries)
        self.attributesButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        
    def resolveContours(self):
        self.contRes = seriesContourResolver(pSeries=self.pSeries, sSeries=self.sSeries)
        self.contoursButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
    
    def resolveZContours(self):
        self.zContRes = seriesZContourResolver(pSeries=self.pSeries, sSeries=self.sSeries)
        self.zcontoursButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))

class sectionConflictWindow(QtGui.QFrame): #===
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

        self.loadObjects()
        self.loadLayout()
        self.loadFunctionality()
        
        
        self.show()
        
    def loadObjects(self):
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
        self.attributesButton.setPalette(QtGui.QPalette(QtGui.QColor('pink')))
        self.attributesButton.clicked.connect( self.resolveAttributes )
        # ZContours
        self.imagesButton.setText('Image\nConflicts')
        self.imagesButton.clicked.connect( self.resolveImages )
        self.imagesButton.setPalette(QtGui.QPalette(QtGui.QColor('pink')))
        # Contours
        self.contoursButton.setText('Contour\nConflicts')
        self.contoursButton.clicked.connect( self.resolveContours )
        self.contoursButton.setPalette(QtGui.QPalette(QtGui.QColor('pink')))
        # Close
        self.closeButton.setText('Save and Close')
        self.closeButton.clicked.connect( self.closeWin )
    
    def resolveAttributes(self):
        self.attRes = sectionAttributeResolver(parent=None,
                                               pSeries=self.pSeries,
                                               sSeries=self.sSeries)
        self.attributesButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        
    def resolveImages(self):
        self.imgRes = sectionImageResolver(parent=None,
                                           pSeries=self.pSeries,
                                           sSeries=self.sSeries)
        self.imagesButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
    
    def resolveContours(self): #===
        print('sec conts pressed')
        self.contRes = sectionContourResolver(parent=None,
                                              pSeries=self.pSeries,
                                              sSeries=self.sSeries)
        self.contoursButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
    
    def closeWin(self):
        # Update instance data to match resolvers
        try:
            self.mergedAttributes = self.attRes.mergedAttributes
        except:
            print('Default section attributes chosen')
            
        try:
            self.mergedImages = self.imgRes.mergedImages
        except:
            print('Default section images chosen')
            
        try:    
            self.mergedContours = self.contRes.mergedContours
        except:
            print('Default section contours chosen')

        self.close()
        
        #=== still need to update mainContainer
        print('Merged Sec Attributes: '+str(self.mergedAttributes)) # Works
        print('Merged Sec Images: '+str(self.mergedImages))
        print('Merged Sec Contours: '+str(self.mergedContours))

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
        self.numConflicts = 0
        # Init table
        self.table = QtGui.QTableWidget(len(conflicts)+len(mergedAtts), 1, self)
        self.table.setColumnWidth(0,330)
        self.table.itemPressed.connect( self.resolveDetail )
        # Load table items
        row = 0
        for att in conflicts:
            item = QtGui.QTableWidgetItem( str(att) )
            item.setBackground(QtGui.QBrush(QtGui.QColor('pink')))
            self.numConflicts += 1
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(row,0,item)
            row+=1
        for att in mergedAtts:
            item = QtGui.QTableWidgetItem( str(att) )
            item.setBackground(QtGui.QBrush(QtGui.QColor('lightgreen')))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(row,0,item)
            row+=1
        self.table.setHorizontalHeaderLabels(['Series Attributes\n'+str(self.numConflicts)+' Conflicts'])
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
    
class seriesContourResolver(QtGui.QFrame):
    def __init__(self, parent=None, pSeries=None, sSeries=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,100)
        self.setWindowTitle('Series Contour Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        self.pSeriesConts = [cont for cont in pSeries.contours if cont.tag == 'Contour']
        self.sSeriesConts = [cont for cont in sSeries.contours if cont.tag == 'Contour']
        
        self.mergedContours = None
        
        self.loadObjects()
        self.loadLayout()
        self.show()

    def loadObjects(self):
        self.pSeriesContButton = QtGui.QPushButton(self)
        self.pSeriesContButton.setText('Choose Primary\nSeries Contours (Default)')
        self.pSeriesContButton.clicked.connect( self.choose )
        self.sSeriesContButton = QtGui.QPushButton(self)
        self.sSeriesContButton.setText('Choose Secondary\nSeries Contours')
        self.sSeriesContButton.clicked.connect( self.choose )
    
    def loadLayout(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget( self.pSeriesContButton )
        vbox.addWidget( self.sSeriesContButton )
        self.setLayout( vbox )
        
    def choose(self):
        if self.sender() == self.pSeriesContButton:
            self.mergedContours = self.pSeriesConts
        else:
            self.mergedContours = self.sSeriesConts
        self.close()

class seriesZContourResolver(QtGui.QFrame):
    def __init__(self, parent=None, pSeries=None, sSeries=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,200)
        self.setWindowTitle('Series ZContour Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)

        self.pSeriesZConts = [cont for cont in pSeries.contours if cont.tag == 'ZContour']
        self.sSeriesZConts = [cont for cont in sSeries.contours if cont.tag == 'ZContour']
        
        self.mergedZContours = None
        
        self.loadObjects()
        self.loadLayout()
        self.show()
    
    def loadObjects(self):
        self.pSerZContsButton = QtGui.QPushButton(self)
        self.pSerZContsButton.setText('Choose Primary Series\'\nZContours (Default)')
        self.pSerZContsButton.clicked.connect( self.choose )
        self.sSerZContsButton = QtGui.QPushButton(self)
        self.sSerZContsButton.setText('Choose Secondary Series\'\nZContours')
        self.sSerZContsButton.clicked.connect( self.choose )
        self.bothSerZContsButton = QtGui.QPushButton(self)
        self.bothSerZContsButton.setText('Choose both Series\'\nZContours')
        self.bothSerZContsButton.clicked.connect( self.choose )
    
    def loadLayout(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget( self.pSerZContsButton )
        vbox.addWidget( self.sSerZContsButton )
        vbox.addWidget( self.bothSerZContsButton)
        self.setLayout( vbox )
        
    def choose(self):
        if self.sender() == self.pSerZContsButton:
            self.mergedZContours = self.pSeriesZConts
        elif self.sender() == self.sSerZContsButton:
            self.mergedZContours = self.sSeriesZConts
        else:
            self.mergedZContours = mergeTool.mergeSeriesZContours(self.pSeriesZConts,
                                                                  self.sSeriesZConts,
                                                                  handler=mergeTool.serZContHandler)
        self.close()

class sectionAttributeResolver(QtGui.QFrame):
    def __init__(self, parent=None, pSeries=None, sSeries=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,400)
        self.setWindowTitle('Section Attribute Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        self.pSecAttributes = [section.output() for section in pSeries.sections]
        self.sSecAttributes = [section.output() for section in sSeries.sections]
        
        self.mergedAttributes = None
        
        self.loadObjects()
        self.loadLayout()
        self.show()
        
    def loadObjects(self):
        self.closeSaveButton = QtGui.QPushButton(self)
        self.closeSaveButton.setText('Save and Close')
        self.closeSaveButton.clicked.connect( self.updateAndClose )
        
        self.numConflicts = 0
        self.table = QtGui.QTableWidget( max(len(self.pSecAttributes),len(self.sSecAttributes)),
                                        1, 
                                        self)
        self.table.setColumnWidth(0,330)
        self.table.itemPressed.connect( self.resolveDetail )
        # Load table items
        for i in range(max(len(self.pSecAttributes),len(self.sSecAttributes))):
            pSec = self.pSecAttributes[i]
            sSec = self.sSecAttributes[i]
            
            item = QtGui.QTableWidgetItem( 'Section '+pSec['index'] )
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if pSec == sSec:
                item.setBackground(QtGui.QBrush(QtGui.QColor('lightgreen')))
            else:
                item.setBackground(QtGui.QBrush(QtGui.QColor('pink')))
                self.numConflicts += 1
            self.table.setItem(i,0,item)
        self.table.setHorizontalHeaderLabels(['Section Attributes\n'+str(self.numConflicts)+' Conflicts'])
        self.table.show()
        
    def loadLayout(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.table)
        vbox.addWidget(self.closeSaveButton)
        self.setLayout(vbox)
        
    def resolveDetail(self, item):
        pink = '#ffc0cb'
        yellow = '#ffff66'
        if item.background().color().name() in [pink, yellow]:
            self.res = textResolveDetail(parent=None, item=item,
                              pItem=self.pSecAttributes[item.row()],
                              sItem=self.sSecAttributes[item.row()])
   
    def updateAndClose(self):
        self.mergedAttributes = []
        for row in range( self.table.rowCount() ):
            itemLabel = self.table.item(row,0).text()
            if '(Secondary)' in itemLabel:
                itemLabel = str(itemLabel.replace(' (Secondary)',''))
                self.mergedAttributes.append(self.sSecAttributes[row])
            else:
                itemLabel = str(itemLabel.replace(' (Primary)',''))
                self.mergedAttributes.append(self.pSecAttributes[row])
        self.close()
        
class sectionImageResolver(QtGui.QFrame):
    def __init__(self, parent=None, pSeries=None, sSeries=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,400)
        self.setWindowTitle('Section Image Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        self.sections = [sec for sec in pSeries.sections]
        self.pSecImages = [sec.imgs[0] for sec in pSeries.sections]
        self.sSecImages = [sec.imgs[0] for sec in sSeries.sections]
        
        self.mergedImages = None
        
        self.loadObjects()
        self.loadLayout()
        self.show()
        
    def loadObjects(self):
        self.numConflicts = 0
        self.saveCloseButton = QtGui.QPushButton(self)
        self.saveCloseButton.setText('Save and Close')
        self.saveCloseButton.clicked.connect( self.updateAndClose )
        
        self.table = QtGui.QTableWidget(max(len(self.pSecImages),len(self.sSecImages)),
                                        1,
                                        self)
        self.table.setColumnWidth(0,330)
        self.table.itemPressed.connect( self.resolveDetail ) #===
        # Load table items
        for i in range(max(len(self.pSecImages),len(self.sSecImages))):
            pSec = self.pSecImages[i].output()
            sSec = self.sSecImages[i].output()
            
            item = QtGui.QTableWidgetItem( 'Section '+str(self.sections[i].index) )
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if pSec == sSec:
                item.setBackground(QtGui.QBrush(QtGui.QColor('lightgreen')))
            else:
                item.setBackground(QtGui.QBrush(QtGui.QColor('pink')))
                self.numConflicts += 1
            self.table.setItem(i,0,item)
        self.table.setHorizontalHeaderLabels(['Section Images\n'+str(self.numConflicts)+' Conflicts'])
        self.table.show()
    
    def loadLayout(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.table)
        vbox.addWidget(self.saveCloseButton)
        self.setLayout(vbox)
    
    def resolveDetail(self, item):
        pink = '#ffc0cb'
        yellow = '#ffff66'
        if item.background().color().name() in [pink, yellow]:
            self.res = textResolveDetail(parent=None, item=item,
                              pItem=self.pSecImages[item.row()].output(),
                              sItem=self.sSecImages[item.row()].output())    
    
    def updateAndClose(self):
        self.mergedImages = []
        for row in range( self.table.rowCount() ):
            itemLabel = self.table.item(row,0).text()
            if '(Secondary)' in itemLabel:
                itemLabel = str(itemLabel.replace(' (Secondary)',''))
                self.mergedImages.append(self.sSecImages[row])
            else:
                itemLabel = str(itemLabel.replace(' (Primary)',''))
                self.mergedImages.append(self.pSecImages[row])
        self.close()
        
class sectionContourResolver(QtGui.QFrame):
    def __init__(self, parent=None, pSeries=None, sSeries=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,400)
        self.setWindowTitle('Section Contour Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        self.pSections = [sec for sec in pSeries.sections]
        self.sSections = [sec for sec in sSeries.sections]
        self.pSecConts = [sec.contours for sec in pSeries.sections]
        self.sSecConts = [sec.contours for sec in sSeries.sections]
        
        self.allMergedContours = None # All of the contours that were selected via resolution
         
        self.loadObjects()
        self.loadFunctionality()
        self.loadLayout()
        self.show()
        
    def loadObjects(self):
        self.saveCloseButton = QtGui.QPushButton(self)
        self.table = QtGui.QTableWidget(max(len(self.pSecConts),len(self.sSecConts)),
                                        1,
                                        self)
        
    def loadFunctionality(self):
        self.saveCloseButton.setText('Save and Close')
        self.saveCloseButton.clicked.connect( self.updateAndClose )
        
        # Table stuff
        self.numConflicts = 0
        self.table.setColumnWidth(0,330)
        self.table.itemPressed.connect( self.resolveDetail ) #===
        # Load table items
        for i in range(max(len(self.pSecConts),len(self.sSecConts))):
            pSec = self.pSecConts[i]
            sSec = self.sSecConts[i]
            
            item = QtGui.QTableWidgetItem( 'Section '+str(self.pSections[i].index) )
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if pSec == sSec: #=== Too exclusive?
                item.setBackground(QtGui.QBrush(QtGui.QColor('lightgreen')))
            else:
                item.setBackground(QtGui.QBrush(QtGui.QColor('pink')))
                self.numConflicts += 1
            self.table.setItem(i,0,item)
        self.table.setHorizontalHeaderLabels(['Section Contours\n'+str(self.numConflicts)+' Conflicts'])
        self.table.show()
        
    def loadLayout(self):
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.table)
        vbox.addWidget(self.saveCloseButton)
        self.setLayout(vbox)

    def resolveDetail(self, item):
        pink = '#ffc0cb'
        yellow = '#ffff66'
        row=item.row()
        if item.background().color().name() in [pink, yellow]:
            self.res = sectionContourResolver.sectionContoursWidget(parent=None, window=self,
                                                                   pSection=self.pSections[row],
                                                                   sSection=self.sSections[row])
        item.setBackground(QtGui.QBrush(QtGui.QColor('yellow')))

    def updateAndClose(self): #===
        print('updateandclose')
        print('AllMergedContours: '+str(self.allMergedContours))
        self.close()
    
    class sectionContoursWidget(QtGui.QWidget):
        def __init__(self, parent=None, window=None, pSection=None, sSection=None):
            QtGui.QWidget.__init__(self, parent)
            self.setGeometry(0,0,800,500)
            self.parent = window # To update the allMergedContours dict
            self.pSection = pSection
            self.sSection = sSection
            
            self.secMergedContours = None
            
            self.loadObjects()
            self.loadFunctionality()
            self.loadLayout()
            
            self.show()
        
        def loadObjects(self):
#             self.pSerTable = QtGui.QTableWidget() # Moved to loadTables()
#             self.midTable = QtGui.QTableWidget() # "
#             self.sSerTable = QtGui.QTableWidget() # "
            self.saveCloseButton = QtGui.QPushButton(self)
            self.ignorePTable = QtGui.QCheckBox(self)
            self.ignoreMTable = QtGui.QCheckBox(self)
            self.ignoreSTable = QtGui.QCheckBox(self)
            
        def loadFunctionality(self):
            self.loadTables()
            self.midTable.itemPressed.connect( self.resolveConflict )
            self.saveCloseButton.setText('Save and Close')
            self.saveCloseButton.clicked.connect( self.saveAndClose )
            self.ignorePTable.setText('Ignore items in this table')
            self.ignoreMTable.setText('Ignore items in this table')
            self.ignoreSTable.setText('Ignore items in this table')
        
        def loadLayout(self):
            hbox1 = QtGui.QHBoxLayout() # Holds all of the table widgets
            hbox1.addWidget(self.pSecTable)
            hbox1.addWidget(self.midTable)
            hbox1.addWidget(self.sSecTable)
            
            hbox2 = QtGui.QHBoxLayout()
            hbox2.addWidget(self.ignorePTable)
            hbox2.addWidget(self.ignoreMTable)
            hbox2.addWidget(self.ignoreSTable)
            
            hbox3 = QtGui.QHBoxLayout()
            hbox3.addWidget(self.saveCloseButton)
            
            vbox = QtGui.QVBoxLayout()
            vbox.addLayout(hbox1)
            vbox.addLayout(hbox2)
            vbox.addLayout(hbox3)
            self.setLayout(vbox)
            
        def loadTables(self):
            mergeTool.mergeSectionContours(self.pSection, self.sSection, handler=self.secContHandler)
            
            self.pSecTable = QtGui.QTableWidget(len(self.uniqueA),
                                                1,
                                                parent=self)
            self.midTable = QtGui.QTableWidget(len(self.confOvlp)+len(self.compOvlp),
                                               1,
                                               parent=self)
            self.sSecTable = QtGui.QTableWidget(len(self.uniqueB),
                                                1,
                                                parent=self)
            
            # pSerTable
            self.pSecTable.setHorizontalHeaderLabels(['Primary Series\nUnique Contours'])
            for row in range(len(self.uniqueA)):
                tableItem = QtGui.QTableWidgetItem( self.uniqueA[row].name )
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                self.pSecTable.setItem(row, 0, tableItem)
                
            # midTable
            self.midTable.setHorizontalHeaderLabels(['Conflicting and Completely\nOverlapping Contours'])
            row = 0
            for item in self.confOvlp:
                tableItem = QtGui.QTableWidgetItem( item[0].name )
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('pink')))
                self.midTable.setItem(row, 0, tableItem)
                row+=1
            for item in self.compOvlp:
                tableItem = QtGui.QTableWidgetItem( item[0].name )
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightgreen')))
                self.midTable.setItem(row, 0, tableItem)
                row+=1
            
            # sSerTable
            self.sSecTable.setHorizontalHeaderLabels(['Secondary Series\nUnique Contours'])
            for row in range(len(self.uniqueB)):
                tableItem = QtGui.QTableWidgetItem( self.uniqueB[row].name )
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                self.sSecTable.setItem(row, 0, tableItem)
                
            self.pSecTable.setColumnWidth(0,235)
            self.midTable.setColumnWidth(0,235)
            self.sSecTable.setColumnWidth(0,235)
            
        def secContHandler(self, uniqueA, compOvlp, confOvlp, uniqueB):
            '''rmtgui version of section contour handler'''
            self.uniqueA = uniqueA
            self.compOvlp = compOvlp
            self.confOvlp = confOvlp
            self.uniqueB = uniqueB
            return uniqueA, compOvlp, confOvlp, uniqueB
        
        def updateSecMergedConts(self):
            self.secMergedContours = []
            
            # pTable
            if not self.ignorePTable.isChecked():
                pTableConts = []
                for row in range(self.pSecTable.rowCount()):
                    pTableConts.append(self.uniqueA[row])

            
            # midTable
            if not self.ignoreMTable.isChecked():
                mTableConts = []
                for row in range(len(self.confOvlp)):
                    print(str(row))
                    if ' (Secondary)' in self.midTable.item(row,0).text(): #===
                        mTableConts.append( self.confOvlp[row][1] )
                    elif ' (Both)' in self.midTable.item(row,0).text():
                        mTableConts.append( self.confOvlp[row][0])
                        self.confOvlp[row][1].name += '-dup'
                        mTableConts.append( self.confOvlp[row][1])
                    else:
                        mTableConts.append( self.confOvlp[row][0])
                mTableConts.extend( [cont[0] for cont in self.compOvlp] )
            
            # sTable
            if not self.ignoreSTable.isChecked():
                sTableConts = []
                for row in range(self.sSecTable.rowCount()):
                    sTableConts.append(self.uniqueB[row])
        
            self.secMergedContours.extend(pTableConts+mTableConts+sTableConts)
        
        def saveAndClose(self):
            if self.parent.allMergedContours == None:
                self.parent.allMergedContours = {}
            self.updateSecMergedConts()
            self.parent.allMergedContours[ str(self.pSection.index) ] = self.secMergedContours
            self.close()

        def resolveConflict(self, item): #===
            row = item.row()
            pink = '#ffc0cb'
            yellow = '#ffff66'
            if item.background().color().name() in [pink, yellow]: # If background color = pink (i.e. is a conflict)
                self.showConfDetails( *self.returnConfConts(row) )
            else:
                self.showDetail(item)
             
        def returnConfConts(self, row):
            '''Returns a Contour object that is represented in row of the table'''
            return self.confOvlp[row][0], self.confOvlp[row][1], row
 
        def showDetail(self, item):
            '''Provides a small window to display more details about a table item'''
            row = item.row()-len(self.confOvlp)
            table = item.tableWidget()
            # Get contour object
            if table == self.pSecTable: cont = self.uniqueA[row]
            elif table == self.midTable: cont = self.compOvlp[row][0]
            elif table == self.sSecTable: cont = self.uniqueB[row]
             
            # Window
            win = QtGui.QWidget(self)
            win.setGeometry(250, 100, 300, 300)
            win.setAutoFillBackground(True)
             
            # Contour information
            label = QtGui.QLabel(self)
            label.setText(str(cont))
            label.setAlignment(QtCore.Qt.AlignCenter)
             
            # Close button
            closeBut = QtGui.QPushButton(self)
            closeBut.setText('Close')
            closeBut.clicked.connect( win.close )
             
            # Layout
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(label)
            vbox.addWidget(closeBut)
            win.setLayout(vbox)
            win.show()
        
        def itemToYellow(self, item):
            item.setBackground(QtGui.QBrush(QtGui.QColor('yellow')))
            
        def showConfDetails(self, confA, confB, row):
            '''Gives more detail of the contours in conflict'''
            item = self.midTable.item(row, 0)
            itemName = item.text().replace(' (Primary)','').replace(' (Secondary)','')
            def pickConfA():
                item.setText(itemName+' (Primary)')
                self.itemToYellow(item) #===
                res.close()
                 
            def pickConfB():
                item.setText(itemName+' (Secondary)')
                self.itemToYellow(item) #===
                res.close()
                 
            def pickBoth():
                item.setText(itemName+' (Both)')
                self.itemToYellow(item) #===
                res.close()
                 
            # Conflict Resolution window
            res = QtGui.QWidget(self)
            res.setGeometry(0,0,800,500)
            res.setAutoFillBackground(True)
 
            # Conflict Label (Name of conflicting contours)
            labelBox = QtGui.QHBoxLayout()
            label = QtGui.QLabel(self) # Label
            label.setText('Conflict: '+str(confA.name))
            labelBox.addWidget(label)
            labelBox.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            labelBox.setSizeConstraint(QtGui.QLayout.SetFixedSize)
             
            # Sections box
            sectionBox = QtGui.QHBoxLayout()
            #--- Section A
            secAbox = QtGui.QVBoxLayout() # For sectionA detail & button
            tBoxA = QtGui.QLabel(self) # Text box
            tBoxA.setText(str(confA))
            tBoxA.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            confAbut = QtGui.QPushButton(self) # Contour A button
            confAbut.setText('Keep A')
            confAbut.clicked.connect( pickConfA )
            secAbox.addWidget(tBoxA)
            secAbox.addWidget(confAbut)
            sectionBox.addLayout(secAbox)
            #--- Section B
            secBbox = QtGui.QVBoxLayout() # For sectionB detail & button
            tBoxB = QtGui.QLabel(self) # Text box
            tBoxB.setText(str(confB))
            tBoxB.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
            confBbut = QtGui.QPushButton(self) # Contour B button
            confBbut.setText('Keep B')
            confBbut.clicked.connect( pickConfB )
            secBbox.addWidget(tBoxB)
            secBbox.addWidget(confBbut)
            sectionBox.addLayout(secBbox)
             
            # 'Cancel' & 'Keep Both' buttons
            archButtonBox = QtGui.QVBoxLayout()
            bothButBox = QtGui.QHBoxLayout()
            bothBut = QtGui.QPushButton(self)
            bothBut.setText('Keep Both Contours')
            bothBut.clicked.connect( pickBoth )
            bothButBox.addSpacing(250)
            bothButBox.addWidget(bothBut)
            bothButBox.addSpacing(250)
            cancelButBox = QtGui.QHBoxLayout()
            cancelBut = QtGui.QPushButton(self)
            cancelBut.setText('Cancel')
            cancelBut.clicked.connect( res.close )
            cancelButBox.addSpacing(250)
            cancelButBox.addWidget(cancelBut)
            cancelButBox.addSpacing(250)
            archButtonBox.addSpacing(50)
            archButtonBox.addLayout(bothButBox)
            archButtonBox.addLayout(cancelButBox)
            archButtonBox.insertSpacing(-1,100) # prevents the huge space between label and contour info
             
            # Combine layouts
            vbox = QtGui.QVBoxLayout() # For entire detail window
            vbox.addLayout(labelBox)
            vbox.addLayout(sectionBox)
            vbox.addLayout(archButtonBox)
             
            res.setLayout(vbox)
            res.show()    

    class sectionContourConflictResolver(QtGui.QWidget):
        def __init__(self, parent=None, contA=None, contB=None):
            QtGui.QWidget.__init__(self, parent)
            self.parent = parent
            self.setGeometry(0,0,800,500)
            self.contA = contA
            self.contB = contB
             
            self.buttons()
            self.layout()
            self.show()
             
        def buttons(self):
            #=== Contour info windows (eventually pictures; skimage)
            # skimage.
            # skimage.draw.polygon for traces
            self.contAInfo = QtGui.QWidget(self)
            self.contAInfo.setAutoFillBackground(True) #===
             
            self.contBInfo = QtGui.QWidget(self)
            self.contBInfo.setAutoFillBackground(True) #===
             
            # A button
            self.contAButton = QtGui.QPushButton()
            self.contAButton.setText('Choose Series A\nTrace')
            self.contAButton.clicked.connect( self.buttonClicked )
             
            # B button
            self.contBButton = QtGui.QPushButton()
            self.contBButton.setText('Choose Series B\nTrace')
            self.contBButton.clicked.connect( self.buttonClicked )
             
            # Both button
            self.bothButton = QtGui.QPushButton()
            self.bothButton.setText('Choose traces\nfor both series')
            self.bothButton.clicked.connect( self.buttonClicked )
             
            for button in [self.contAButton, self.contBButton, self.bothButton]: #Must be consistent with buttonClicked()
                button.setPalette(QtGui.QPalette('lightgray'))
                          
        def layout(self):
            # Trace info
            hbox1 = QtGui.QHBoxLayout()
            hbox1.addWidget(self.contAInfo)
            hbox1.addWidget(self.contBInfo)
             
            # Trace selection buttons
            hbox2 = QtGui.QHBoxLayout()
            hbox2.insertSpacing(0,50)
            hbox2.addWidget(self.contAButton)
            hbox2.insertSpacing(2,100)
            hbox2.addWidget(self.contBButton)
            hbox2.insertSpacing(4,50)
            hbox3 = QtGui.QHBoxLayout()
            hbox3.insertSpacing(0,250)
            hbox3.addWidget(self.bothButton)
            hbox3.insertSpacing(2,250)
             
            # Action-repetition options
            hbox4 = QtGui.QHBoxLayout()
            hbox4.addWidget(self.thisTraceAllSections, alignment = QtCore.Qt.AlignHCenter)
            hbox5 = QtGui.QHBoxLayout()
            hbox5.addWidget(self.allTracesThisSection, alignment = QtCore.Qt.AlignHCenter)
            hbox6 = QtGui.QHBoxLayout()
            hbox6.addWidget(self.allTracesAllSections, alignment = QtCore.Qt.AlignHCenter)
             
            # Main Layout
            vbox = QtGui.QVBoxLayout()
            vbox.addLayout(hbox1)
            vbox.addLayout(hbox2)
            vbox.addLayout(hbox3)
            vbox.addLayout(hbox4)
            vbox.addLayout(hbox5)
            vbox.addLayout(hbox6)
            self.setLayout(vbox)
         
        def buttonClicked(self):
            for button in [self.contAButton, self.contBButton, self.bothButton]:
                if button == self.sender():
                    button.setPalette(QtGui.QPalette('lightblue'))
                else:
                    button.setPalette(QtGui.QPalette('lightgray'))
        
class textResolveDetail(QtGui.QFrame):
    '''Detailed resolver for text-based item conflicts'''
    def __init__(self, parent=None, item=None, pItem=None, sItem=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,400)
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
        # Need to auto-wrap qlabels
        self.pItemLabel = QtGui.QLabel(self)
        self.pItemLabel.setWordWrap(True)
        self.pItemLabel.setText('Primary Item:\n'+str(self.pItem))
        self.pItemLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.sItemLabel = QtGui.QLabel(self)
        self.sItemLabel.setWordWrap(True)
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

