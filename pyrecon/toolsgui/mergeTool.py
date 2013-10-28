from PySide import QtCore, QtGui
from pyrecon.tools import classes, mergeTool
from lxml import etree as ET
import sys

class mainContainer(QtGui.QFrame):
    '''Holds all the resolved data and objects required for loading series.'''
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
    
    def browseOutpath(self):
        path = QtGui.QFileDialog.getExistingDirectory(self)
        self.outpathLine.setText(path)
            
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
        msg.setText('Okay, done loading the series!\nClick one of the two conflict buttons below to resolve conflicts.\n\n**Non-resolved conflicts (pink) will default to the state of the primary series.    ')
        msg.show()
    
    def seriesConflicts(self):
        # Requires self. in variable name to be rendered correctly
        self.serWin = seriesConflictWindow(parent=None, pSeries=self.series1, sSeries=self.series2, window=self)
        
    def sectionConflicts(self):
        # Requires self. in variable name to be rendered correctly
        self.secWin = sectionConflictWindow(parent=None, pSeries=self.series1, sSeries=self.series2, window=self)
    
    def checkConfButs(self):
        if self.check1 and self.check2:
            self.finishButton.setFlat(False)
            self.finishButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        
    def getOutpathAndName(self):
        # box with directory input line and optional new name
        box = QtGui.QWidget(self)
        box.setGeometry(0,0,600,300)
        box.setAutoFillBackground(True)
        vbox = QtGui.QVBoxLayout() # Holds all stuff in the box
        
        hbox = QtGui.QHBoxLayout() # Holds output directory line/browse
        self.outpathLine = QtGui.QLineEdit(self)
        self.outpathLine.setText('Enter directory to save merged series')
        self.outpathLine.setAlignment(QtCore.Qt.AlignCenter)
        hbox.addWidget(self.outpathLine)
        outpathBrowse = QtGui.QPushButton(self)
        outpathBrowse.setText('Browse')
        outpathBrowse.clicked.connect( self.browseOutpath )
        hbox.addWidget(outpathBrowse)
        
        hbox2 = QtGui.QHBoxLayout()
        self.newNameLine = QtGui.QLineEdit(self)
        self.newNameLine.setText('(Optional) Enter a new name for the series')
        self.newNameLine.setAlignment(QtCore.Qt.AlignCenter)
        hbox2.addWidget(self.newNameLine)
        
        vbox2 = QtGui.QVBoxLayout()
        doneButton = QtGui.QPushButton(self)
        doneButton.setText('Finish!')
        doneButton.clicked.connect( self.mergeEverything )
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(doneButton)
        hbox3.insertSpacing(0,200)
        hbox3.insertSpacing(-1,200)
        cancelButton = QtGui.QPushButton(self)
        cancelButton.setText('Cancel')
        cancelButton.clicked.connect( box.close )
        hbox4 = QtGui.QHBoxLayout()
        hbox4.addWidget(cancelButton)
        hbox4.insertSpacing(0,200)
        hbox4.insertSpacing(-1,200)
        vbox2.addLayout(hbox3)
        vbox2.addLayout(hbox4)
        
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addLayout(vbox2)
        box.setLayout(vbox)
        box.show()
    
    def mergeEverything(self):
        if '\\' in self.outpathLine.text(): # Windows compatability
            self.outpathLine.setText( self.outpathLine.text().replace('\\','/') )
            print( 'Converted backslashes in output directory path')
        if '/' not in self.outpathLine.text() or self.outpathLine.text() == '':
            msg = QtGui.QMessageBox(self)
            msg.setText('Invalid outpath, please re-enter')
            msg.show()
            return
        
        # Renaming series
        if '(Optional)' not in self.newNameLine.text() and self.newNameLine.text() != '':
            name = self.newNameLine.text()
        else:
            name = self.series1.name
         
        #===== SERIES FILE MERGE =====
        # Create new .ser file w/ attributes
        try: mergedSeries = classes.Series( root=ET.Element('Series',self.serWin.mergedAttributes), name=name )
        except: mergedSeries = classes.Series( root=ET.Element('Series',self.series1.output()[0]), name=name)
            
        # Append contours
        try: mergedSeries.contours = list(self.serWin.mergedContours)
        except: mergedSeries.contours = [cont for cont in self.series1.contours if cont.tag == 'Contour']
        
        # Append zcontours
        try: mergedSeries.contours.extend(list(self.serWin.mergedZContours))
        except: mergedSeries.contours.extend([cont for cont in self.series1.contours if cont.tag == 'ZContour'])
        
        #===== SECTION FILES MERGE =====
        # For each section, make a section object
        for secNum in range(max(len(self.series1.sections),len(self.series2.sections))):

            # Attributes
            try:
                elem = ET.Element('Section')
                for att in self.secWin.mergedAttributes[secNum]:
                    elem.set(str(att), self.secWin.mergedAttributes[secNum][att])
                sec = classes.Section(elem, name+'.'+self.secWin.mergedAttributes[secNum]['index'])
            except:
                sec = self.series1.sections[secNum]
                sec.name = str(name+'.'+str(sec.index))
            
            # Images
            try: sec.imgs = [self.secWin.mergedImages[secNum]]
            except: sec.imgs = self.series1.sections[secNum].imgs
            
            # Contours
            try: sec.contours = self.secWin.mergedContours[str(secNum)]
            except: sec.contours = self.series1.sections[secNum].contours
                
            mergedSeries.sections.append(sec)
        
        mergedSeries.writeseries( self.outpathLine.text() )
        mergedSeries.writesections( self.outpathLine.text() )
        
        compMsg = QtGui.QMessageBox(self)
        compMsg.setText('ALL DONE! Everything output to:\n'+str(self.outpathLine.text()))
        ret = compMsg.exec_()
        if ret == QtGui.QMessageBox.Ok:
            self.close()
    
    def finish(self):
        if self.check1 != True or self.check2 != True:
            return
        # Let user know what things were defaulted, choose to continue
        defaultedThings = []
        if self.serWin.mergedAttributes == None:
            defaultedThings.append('Series Attributes')
        if self.serWin.mergedContours == None:
            defaultedThings.append('Series Contours')
        if self.serWin.mergedZContours == None:
            defaultedThings.append('Series ZContours')
        if self.secWin.mergedAttributes == None:
            defaultedThings.append('Section Attributes')
        if self.secWin.mergedImages == None:
            defaultedThings.append('Section Images')
        if self.secWin.mergedContours == None:
            defaultedThings.append('Section Contours')
        
        if len(defaultedThings) > 0:
            defMsg = QtGui.QMessageBox(self)
            msgTxt = 'The following items have been defaulted to the primary series due to lack of resolution:\n'
            for item in defaultedThings:
                msgTxt+='\t'+item+'\n'
            defMsg.setText(msgTxt)
            defMsg.addButton(QtGui.QMessageBox.Ok)
            defMsg.addButton(QtGui.QMessageBox.Cancel)
            ret = defMsg.exec_()
            if ret != QtGui.QMessageBox.Ok:
                defMsg.close()
                return
            defMsg.close()
            
        # Display new message saying that it may take a few moments to merge everything
        msg = QtGui.QMessageBox(self)
        msgTxt = 'This process may take time depending on the size of the series... please be patient!'
        msg.setText(msgTxt)
        msg.addButton(QtGui.QMessageBox.Ok)
        msg.addButton(QtGui.QMessageBox.Cancel)
        ret = msg.exec_()
        if ret == QtGui.QMessageBox.Ok:
            self.getOutpathAndName()
        else:
            return
        
class seriesConflictWindow(QtGui.QFrame):
    '''Window for selecting conflicts to be resolved in .ser files'''
    def __init__(self, parent=None, pSeries=None, sSeries=None, window=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,325,300,150)
        self.setWindowTitle('Series File Conflicts')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        self.parent = window
        
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
    
    def closeWin(self):
        # Update instance data to match resolvers
        try: self.mergedAttributes = self.attRes.mergedAttributes
        except: print('Primary Series Attributes chosen by default')
            
        try: self.mergedContours = self.contRes.mergedContours
        except: print('Primary Series Contours chosen by default')
            
        try: self.mergedZContours = self.zContRes.mergedZContours
        except: print('Primary Series ZContours chosen by default')
        
        self.parent.check1 = True
        self.parent.seriesFileConflicts.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.parent.checkConfButs()
        self.close()
    
    def resolveAttributes(self):
        self.attRes = seriesAttributeResolver(pSeries=self.pSeries,
                                              sSeries=self.sSeries,
                                              window=self)
        
    def resolveContours(self):
        self.contRes = seriesContourResolver(pSeries=self.pSeries,
                                             sSeries=self.sSeries,
                                             window=self)
    
    def resolveZContours(self):
        self.zContRes = seriesZContourResolver(pSeries=self.pSeries,
                                               sSeries=self.sSeries,
                                               window=self)

class sectionConflictWindow(QtGui.QFrame):
    '''Window for selecting what kind of conflicts two resolve between section
    files in a series'''
    def __init__(self, parent=None, pSeries=None, sSeries=None, window=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(300,325,300,150)
        self.setWindowTitle('Section File Conflicts')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        self.parent=window
        
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
        self.attRes = sectionAttributeResolver(pSeries=self.pSeries,
                                               sSeries=self.sSeries,
                                               window=self)
        
    def resolveImages(self):
        self.imgRes = sectionImageResolver(pSeries=self.pSeries,
                                           sSeries=self.sSeries,
                                           window=self)
     
    def resolveContours(self):
        self.contRes = sectionContourResolver(pSeries=self.pSeries,
                                              sSeries=self.sSeries,
                                              window=self)
    
    def closeWin(self):
        # Update instance data to match resolvers
        try: self.mergedAttributes = self.attRes.mergedAttributes
        except: print('Primary Series Section Attributes chosen by default')
            
        try: self.mergedImages = self.imgRes.mergedImages
        except: print('Primary Series Section Images chosen by default')
            
        try: self.mergedContours = self.contRes.allMergedContours
        except: print('Primary Series Section Contours chosen by default')
        
        self.parent.check2 = True
        self.parent.sectionFileConflicts.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.parent.checkConfButs()
        self.close()

class seriesAttributeResolver(QtGui.QFrame):
    '''Window for resolving attribute differences between two .ser files'''
    def __init__(self, parent=None, pSeries=None, sSeries=None, window=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,400)
        self.setWindowTitle('Series Attribute Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        self.parent = window
        
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
        self.parent.attributesButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.close()
    
class seriesContourResolver(QtGui.QFrame):
    '''Window for resolving contour differences between two .ser files'''
    def __init__(self, parent=None, pSeries=None, sSeries=None, window=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,100)
        self.setWindowTitle('Series Contour Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        self.parent=window
        
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
        self.parent.contoursButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.close()

class seriesZContourResolver(QtGui.QFrame):
    '''Window for resolving ZContour differences between two .ser files'''
    def __init__(self, parent=None, pSeries=None, sSeries=None, window=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,200)
        self.setWindowTitle('Series ZContour Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        self.parent=window

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
        self.parent.zcontoursButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.close()

class sectionAttributeResolver(QtGui.QFrame):
    '''Window for resolving attribute differences in section pairs of the 
    two series'.'''
    def __init__(self, parent=None, pSeries=None, sSeries=None, window=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,400)
        self.setWindowTitle('Section Attribute Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        self.parent=window
        
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
        self.parent.attributesButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.close()
        
class sectionImageResolver(QtGui.QFrame):
    '''Window for resolving src image differences between sections.'''
    def __init__(self, parent=None, pSeries=None, sSeries=None, window=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,400)
        self.setWindowTitle('Section Image Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        self.parent=window
        
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
        self.table.itemPressed.connect( self.resolveDetail )
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
        self.parent.imagesButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.close()
        
class sectionContourResolver(QtGui.QFrame):
    '''Window for resolving conflicts between section contours in two series.
    A single table with an item for each section pair (pink if differences exist)'''
    def __init__(self, parent=None, pSeries=None, sSeries=None, window=None):
        QtGui.QFrame.__init__(self, parent)
        self.setGeometry(0,0,400,400)
        self.setWindowTitle('Section Contour Conflict Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        self.parent=window
        
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
        self.table.itemPressed.connect( self.resolveDetail )
        # Load table items
        for i in range(max(len(self.pSecConts),len(self.sSecConts))):
            pSec = self.pSecConts[i]
            sSec = self.sSecConts[i]
            
            item = QtGui.QTableWidgetItem( 'Section '+str(self.pSections[i].index) )
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if pSec == sSec: #=== Too Exclusive?
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
        yellow = '#ffff00'
        row=item.row()
        if item.background().color().name() in [pink, yellow]:
            self.res = sectionContourResolver.sectionContoursWidget(parent=None, window=self,
                                                                   pSection=self.pSections[row],
                                                                   sSection=self.sSections[row])
        item.setBackground(QtGui.QBrush(QtGui.QColor('yellow')))

    def updateAndClose(self):
        self.parent.contoursButton.setPalette(QtGui.QPalette(QtGui.QColor('lightgreen')))
        self.close()
    
    class sectionContoursWidget(QtGui.QWidget):
        '''Displays all the contours in two sections, with the primary section in the left table,
        secondary in the right, and conflicting/merged in the middle'''
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
#             self.pSecTable = QtGui.QTableWidget() # Moved to loadTables()
#             self.midTable = QtGui.QTableWidget() # "
#             self.sSecTable = QtGui.QTableWidget() # "
            self.saveCloseButton = QtGui.QPushButton(self)
            self.ignorePTable = QtGui.QCheckBox(self)
            self.ignoreMTable = QtGui.QCheckBox(self)
            self.ignoreSTable = QtGui.QCheckBox(self)
            
        def loadFunctionality(self):
            self.loadTables()
            self.pSecTable.itemPressed.connect( self.resolveConflict )
            self.midTable.itemPressed.connect( self.resolveConflict )
            self.sSecTable.itemPressed.connect( self.resolveConflict )
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
            pTableConts = []
            if not self.ignorePTable.isChecked():
                for row in range(self.pSecTable.rowCount()):
                    pTableConts.append(self.uniqueA[row])
            
            # midTable
            mTableConts = []
            if not self.ignoreMTable.isChecked():
                for row in range(len(self.confOvlp)):
                    if ' (Secondary)' in self.midTable.item(row,0).text():
                        mTableConts.append( self.confOvlp[row][1] )
                    elif ' (Both)' in self.midTable.item(row,0).text():
                        mTableConts.append( self.confOvlp[row][0])
                        self.confOvlp[row][1].name += '-sec'
                        mTableConts.append( self.confOvlp[row][1])
                    else:
                        mTableConts.append( self.confOvlp[row][0])
                mTableConts.extend( [cont[0] for cont in self.compOvlp] )
            
            # sTable
            sTableConts = []
            if not self.ignoreSTable.isChecked():
                for row in range(self.sSecTable.rowCount()):
                    sTableConts.append(self.uniqueB[row])
        
            self.secMergedContours.extend(pTableConts+mTableConts+sTableConts)
            
        def resolveConflict(self, item):
            row = item.row()
            pink = '#ffc0cb'
            yellow = '#ffff00'
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
            itemName = item.text().replace(' (Primary)','').replace(' (Secondary)','').replace(' (Both)', '')
            def pickConfA():
                item.setText(itemName+' (Primary)')
                self.itemToYellow(item)
                res.close()
                 
            def pickConfB():
                item.setText(itemName+' (Secondary)')
                self.itemToYellow(item)
                res.close()
                 
            def pickBoth():
                item.setText(itemName+' (Both)')
                self.itemToYellow(item)
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

        def saveAndClose(self):
            if self.parent.allMergedContours == None:
                self.parent.allMergedContours = {}
            self.updateSecMergedConts()
            print([cont.name for cont in self.secMergedContours])
            # Add contours for this section to the dictionary
            self.parent.allMergedContours[ str(self.pSection.index) ] = self.secMergedContours
            self.close()
            
    class sectionContourConflictResolver(QtGui.QWidget):
        '''Window for resolving conflicts between two contours'''
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
            self.contAInfo.setAutoFillBackground(True)
             
            self.contBInfo = QtGui.QWidget(self)
            self.contBInfo.setAutoFillBackground(True)
             
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
    
app = QtGui.QApplication(sys.argv)
a = mainContainer() # Doesn't work unless set to a variable for some reason
sys.exit( app.exec_() )