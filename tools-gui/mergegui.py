from PySide import QtGui, QtCore
import reconstructmergetool as rmt
import sys
from Series import *

'''TEST.PY functions as a test page for rmtgui.py. Changes are first made to test.py until a working
product is established and ready to be copied to rmtgui.py'''
# To Do:
#     Wait cursor after Series ZContours
#     Search for all of the '#===' to find problems/development areas
#     QPushButton.setAcceptDrops(True) for load series
#     Filters for contour name
#     Restore default for seccontwidg()
#     Repeat for other sections check box or button
#     Arrows/Scroll/Click in slider doesnt work

class widgetWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setGeometry(0,0,800,500)
        
class singleColumnTable(QtGui.QTableWidget):
    def __init__(self, length=None, noCol = 1, parent = None):
        QtGui.QTableWidget.__init__(self, length, noCol, parent)
        self.setSelectionMode( QtGui.QAbstractItemView.SelectionMode.MultiSelection )
        self.length = length
        self.currentRow = 0
        
    # Functions for loading
    def loadConts(self, contList): #===
        '''Loads objects from contList to table as tableItem'''
        row = 0
        for cont in contList:
            item = self.cont2item(cont)
            self.setItem(row, 0, item)
            row+=1
        self.currentRow = row
    
    def cont2item(self, cont, background='white'): #===
        '''Returns contour as a tableWidgetItem with specified background'''
        item = QtGui.QTableWidgetItem( cont.name )
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setBackground(QtGui.QBrush(QtGui.QColor(background)))
        return item
    
    def loadAtts(self, attList): #===
        '''Loads objects from attList to table as tableItem'''
        row = 0
        for att in attList:
            item = self.att2item(att)
            self.setItem(row, 0, item)
            row+=1
        self.currentRow = row
    
    def att2item(self, att, background='white'): #===
        item = QtGui.QTableWidgetItem( str(att) )
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setBackground(QtGui.QBrush(QtGui.QColor(background)))
        return item
    
    def loadLabels(self, labelList): #===
        return
       

    def selItems(self):
        '''Returns list of selected items'''
        return self.selectedItems()
    
    def allItems(self): #=== need to return actual items?
        '''Returns all items in the table'''
        items = []
        for row in range(self.length):
            items.append( self.item(0,row) )
        return items
    
    def item2cont(self, item, ref):
        '''Returns the contour object associated with item from ref'''
        return ref[ item.row() ]
    
    def item2att(self, item, ref):
        '''Returns a dictionary entry associated with item from ref'''
        return ref[ item.row() ]
       
    def itemsAsAttributes(self):
        '''Returns items as a dictionary of attributes'''
        return
    
    def itemsAsImages(self):
        '''Returns items as image objects'''
        return
    
    def showItemDetail(self, obj):
        '''Opens a display window with details for the object. __str__ must be defined in object'''
        detail = str(obj) # Str representation of object
        
        # Window
        win = QtGui.QWidget(self)
        win.setGeometry(250, 100, 300, 300)
        win.setAutoFillBackground(True)
        
        # Contour information
        label = QtGui.QLabel(self)
        label.setText(detail)
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
        
    def setHeader(self, header):
        self.setHorizontalHeaderLabels([header])
    def setWidth(self, width):
        self.setColumnWidth(0, width)
    def addItem(self, item):
        self.setItem(self.currentRow, 0, item)
        self.currentRow+=1
        
class mainFrame(QtGui.QFrame):
    '''The mainFrame() class holds all the contents of the reconstructmergetool (RMT) gui. It is the one
    RMTgui class that is open throughout the entire program.
    GUI-wise: the mainframe contains the widgets necessary for proper functioning of RMT. And a
        quit button.
    Data-wise: It contains all the important info regarding the series that are being merged.'''
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        # Window Dimensions and Attributes
        self.setGeometry(0,0,800,600)
        self.setWindowTitle('Reconstructmergetool v.DEV') #=== Change for deploy
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        # Widgets
        self.nextButton = QtGui.QPushButton(self)
        self.backButton = QtGui.QPushButton(self)
        self.slider = QtGui.QSlider(self)
        self.label = QtGui.QLabel(self)
        
        # Main Data
        self.ser1path = '/home/michaelm/Documents/Test Series/rmtgTest/ser1/BBCHZ.ser' #=== Remove for deploy
        self.ser2path = '/home/michaelm/Documents/Test Series/rmtgTest/ser2/BBCHZ.ser' #=== Remove for deploy
#         self.ser1path = 'Enter path or browse for Series 1'
#         self.ser2path = 'Enter path or browse for Series 2'

        self.serName = 'rmtg' #=== Remove for deploy
#        self.serName = 'Enter name of new series'
        self.ser1obj = None
        self.ser2obj = None

        # Reconstruct Object Data
        self.mergedAttributes = []
        self.mergedSerContours = [] #===
        self.mergedSerZContours = []
        
        self.mergedSecList = [] #===
        self.mergedSecAttributes = [] #===
        self.mergedSecImages = []
        self.mergedSecContours = [] #===
        self.contourWidgets = []
        self.currentWidget = None
        
        self.mergedSeries = None #=== First created (seriesAttributeWidget.next()) w/ no Contours/ZContours
        self.outputPath = 'Enter directory for output'
        
        # Load Functional Frame
        self.initUI()
        
    def initUI(self):
        self.prepNandBbuttons()
#         self.prepSlider() #=== moved to sectionAttributeWidget
        self.prepLayout()
        
        # shown when needed
        self.slider.hide()
        self.label.hide()

        self.show()
    
    def prepLayout(self):
        # Layout: Puts buttons in bottom-right corner
        hbox = QtGui.QHBoxLayout() # Horizontal
        hbox.addStretch(1) # Push down
        hbox.addWidget(self.backButton)
        hbox.addWidget(self.nextButton)
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(self.slider)
        vbox2.addWidget(self.label)
        
        vbox = QtGui.QVBoxLayout() # Vertical
        vbox.addStretch(1) # Push right
        vbox.addLayout(vbox2)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
    def prepNandBbuttons(self):
        # Next button
        self.nextButton.setText('Next')

        # Back button
        self.backButton.setText('Back')
          
    def prepSlider(self): #===
        #=== doesnt properly respond to clicking on ticks far from the "slider knob"
        # Slider
        if type(self.ser1obj) != None and type(self.ser2obj) != None:
            minTick = int(self.ser1obj.sections[0].name[-1]) # section no. of first section in section list
            if minTick == 0:
                maxTick = len(self.ser1obj.sections)-1 # number of sections in section list
            else:
                maxTick = len(self.ser1obj.sections)
            self.slider.setRange(minTick, maxTick)
        
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.slider.setTickInterval(1)
         
        # Label
        self.label.setText('Section '+str(self.slider.value()))
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        
        self.slider.sliderReleased.connect( self.changeSection )
        self.slider.sliderMoved.connect( self.changeSectionLabel )
        
    def changeSection(self):
        '''Loads appropriate section when the slider is released on a new position'''
        self.currentWidget.hide()
        
        # for already existing contourWidgets
        for sec in self.contourWidgets:
            if sec.section == self.slider.value():      
                self.currentWidget = sec
                self.currentWidget.show()
                self.sortContWidgList() #===
                return
        
        # for those that dont yet exist
        sec = mainFrame.sectionContourWidget( self, self.slider.value() )
        self.contourWidgets.append(sec)
        self.sortContWidgList() #===
        self.slider.show()
        self.label.show()
        self.currentWidget = sec
        self.currentWidget.show()
   
    def changeSectionLabel(self):
        '''Updates the section label while the slider is being moved'''
        print('Hovering: '+str(self.slider.sliderPosition())) #=== Remove for deploy
        print('Previously Hovered: '+str(self.slider.value())) #=== Remove for deploy
        newPos = self.slider.sliderPosition()
        self.label.setText('Section '+str(newPos)) #=== Remove for deploy

    def dispContourWidget(self):
        '''Shows the current secContWidget(), creates one if none exist'''
        if len(self.contourWidgets) == 0: # Make contour widget if doesnt exist
                self.contourWidgets.append( self.sectionContourWidget(self, 0 ))
                self.currentWidget = self.contourWidgets[0]
        else:
            self.slider.show()
            self.label.show()
        self.currentWidget.show()
    
    def sortContWidgList(self): #===
        self.contourWidgets = sorted(self.contourWidgets,
                                     key=lambda sectionContourWidget: sectionContourWidget.section)
            
    class serLoadWidget(widgetWindow):
        def __init__(self, parent=None):
            widgetWindow.__init__(self, parent)
            self.parent.backButton.setFlat(True)
            
            # Functional objects
            self.s1bar = None # Series 1 Path
            self.s1browse = None # Browse for ser 1 path
            self.s2bar = None
            self.s2browse = None
            self.sNameBar = None # Enter name for series
            
            self.prepFuncObjs()
            self.prepLayout()
            self.buttonFunctionality()
            
            self.show()
            
        def prepLayout(self):
            # Layout
            hbox1 = QtGui.QHBoxLayout()
            hbox1.addWidget(self.s1bar)
            hbox1.addWidget(self.s1browse)
            hbox1.insertSpacing(0,150)
            hbox1.insertSpacing(-1,150)
            
            hbox2 = QtGui.QHBoxLayout()
            hbox2.addWidget(self.s2bar)
            hbox2.addWidget(self.s2browse)
            hbox2.insertSpacing(0,150)
            hbox2.insertSpacing(-1,150)
            
            hbox3 = QtGui.QHBoxLayout()
            hbox3.addWidget(self.sNameBar)
            hbox3.insertSpacing(0,300)
            hbox3.insertSpacing(-1,300)
            
            vbox = QtGui.QVBoxLayout()
            vbox.insertSpacing(0,200)

            vbox.addLayout(hbox1)
            vbox.addLayout(hbox2)
            vbox.addLayout(hbox3)
            self.setLayout(vbox)
            
        def prepFuncObjs(self):
            '''Creates the objects that are functional in this class'''
            self.s1bar = QtGui.QLineEdit(self)
            self.s1bar.setText(self.parent.ser1path)
            self.s1browse = QtGui.QPushButton(self)
            self.s1browse.setIconSize(QtCore.QSize(25,25))
            self.s1browse.setText('Browse')
            
            self.s2bar = QtGui.QLineEdit(self)
            self.s2bar.setText(self.parent.ser2path)
            self.s2browse = QtGui.QPushButton(self)
            self.s2browse.setIconSize(QtCore.QSize(25,25))
            self.s2browse.setText('Browse')
            
            # Series name text bar
            self.sNameBar = QtGui.QLineEdit(self)
            self.sNameBar.setText(self.parent.serName)
            
        def buttonFunctionality(self):
            '''Adds functionality to the objects created in self.prepFuncObjs()'''
            self.parent.nextButton.clicked.connect( self.checkNextButton )
            self.s1bar.setAcceptDrops(True) #===
            self.s2bar.setAcceptDrops(True) #===
            self.s1browse.clicked.connect( self.browseSer )
            self.s2browse.clicked.connect( self.browseSer )
            
        def browseSer(self):
            '''Displays file browser and updates text in s1bar or s2bar.
            Parent data is not updated until next button function is executed
            successfully.'''
            path = QtGui.QFileDialog.getOpenFileName(self,
                                                     'Load Series',
                                                     '/home/',
                                                     'Series File (*.ser)')
            path = str(path[0])
            if self.sender() == self.s1browse: 
                self.s1bar.setText(path)
            elif self.sender() == self.s2browse:
                self.s2bar.setText(path)
        
        def next(self):
            # Update mainFrame() data
            self.parent.ser1path = self.s1bar.text()
            self.parent.ser2path = self.s2bar.text()
            self.parent.serName = self.sNameBar.text().replace('.ser','')
            self.parent.ser1obj = rmt.getSeriesXML(self.parent.ser1path) #===
            self.parent.ser2obj = rmt.getSeriesXML(self.parent.ser2path) #===
            
            # Merge series widget
            self.parent.nextButton.clicked.disconnect( self.checkNextButton )
            self.parent.seriesAttributeWidget(self.parent)
            self.close()

        def checkNextButton(self):
            if '.ser' not in self.s1bar.text() or '.ser' not in self.s2bar.text():
                msg = QtGui.QMessageBox(self)
                msg.setText('Please enter valid paths for both series')
                msg.show()
            elif self.sNameBar.text() == 'Enter name of new series' or self.sNameBar.text() == '':
                msg = QtGui.QMessageBox(self)
                msg.setText('Please enter a valid series name')
                msg.show()
            else:
                self.next()

    class seriesAttributeWidget(widgetWindow):
        def __init__(self, parent=None):
            widgetWindow.__init__(self, parent)
            self.table1 = None
            self.table2 = None
            self.table3 = None
            self.conflicts = None
            self.ser3atts = None
              
            # Update mainFrame data
            self.parent.setWindowTitle('Series Attributes') #===
            
            self.prepFuncObjs()
            rmt.mergeSeriesAttributes(self.parent.ser1obj, self.parent.ser2obj, handler=self.serAttHandler)
            self.prepLayout()
        
            self.show()
            
        def prepLayout(self):
            # Layout
            hbox = QtGui.QHBoxLayout()
            vbox1 = QtGui.QVBoxLayout()
            vbox1.addWidget(self.table1)
            vbox2 = QtGui.QVBoxLayout()
            vbox2.addWidget(self.table2)
            vbox3 = QtGui.QVBoxLayout()
            vbox3.addWidget(self.table3)
            hbox.addLayout(vbox1)
            hbox.addLayout(vbox3)
            hbox.addLayout(vbox2)
            self.setLayout(hbox)
            
        def prepFuncObjs(self):
            self.parent.backButton.setFlat(False)
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
        def next(self): #===
#             if len(self.table.selectedItems()) != len(self.conflicts):
#                 msg = QtGui.QMessageBox(self)
#                 msg.setText('Please select one item per row')
#                 msg.show()
#             else:
#                 # Create new dictionary of merged attributes
#                 newAtts = self.parent.ser1obj.output()[0]
#                 resolvedAtts = [ str(item.text()) for item in self.table.selectedItems() ]
#                 for row in range(len(self.conflicts)):
#                     att = self.table.verticalHeaderItem(row).text()
#                     newAtts[att] = resolvedAtts.pop(0)
#                 self.parent.mergedAttributes = newAtts
#                 self.parent.mergedSeries = Series(root=ET.Element('Series',newAtts),name=self.parent.serName)
#                 print('Series created') #===
                
                # Disconnect buttons and load next window
                self.parent.nextButton.clicked.disconnect( self.next )
                self.parent.backButton.clicked.disconnect( self.back )
                self.parent.seriesContourWidget(self.parent)
                self.close()
        
        def back(self):
            # Disconnect buttons and load prev window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.serLoadWidget( self.parent )
            self.close()
            
        def serAttHandler(self, ser1atts, ser2atts, ser3atts, conflicts): #=== put in actual data/details
            self.table1 = singleColumnTable(len(ser1atts), parent=self)
            self.table2 = singleColumnTable(len(ser2atts), parent=self)
            self.table3 = singleColumnTable(len(ser3atts), parent=self)
            self.conflicts = conflicts
            self.ser3atts = ser3atts

            attLabels = [ str(conflict) for conflict in conflicts ]

            self.table1.setHeader(self.parent.ser1obj.name)
            self.table2.setHeader(self.parent.ser2obj.name)
            self.table3.setHeader('Conflicts/Identical Attributes')
            
            for table in [self.table1, self.table2, self.table3]:
                table.setWidth(220)
            
            # Load items
            for conf in conflicts:
                self.table3.addItem( self.table3.att2item(conf, background='pink') )
            for ident in ser3atts:
                self.table3.addItem( self.table3.att2item(ident, background='lightGreen') )
            for attA in ser1atts:
                self.table1.addItem( self.table1.att2item(attA))
            for attB in ser2atts:
                self.table2.addItem( self.table2.att2item(attB))
  
    class seriesContourWidget(widgetWindow):
        def __init__(self, parent=None):
            widgetWindow.__init__(self, parent)
            self.table1 = None
            self.table2 = None
            self.s1c = None
            self.s2c = None
            self.mergedConts = None
             
            # update mainFrame stuff
            self.parent.setWindowTitle('Series Contours') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
             
            rmt.mergeSeriesContours(self.parent.ser1obj.contours, self.parent.ser2obj.contours, handler=self.serContHandler)
             
            self.prepLayout()
            self.show()

        def prepLayout(self):
            # Layout
            vbox = QtGui.QVBoxLayout() # Holds all the boxes below
            hbox1 = QtGui.QHBoxLayout() # For the 2 tables
            hbox1.addWidget(self.table1) # Series 1
            hbox1.addWidget(self.table3) # Merged series contours
            hbox1.addWidget(self.table2) # Series 2
            vbox.addLayout(hbox1)
            self.setLayout(vbox)
            
        def serContHandler(self, ser1conts, ser2conts, ser3conts):
            table1 = QtGui.QTableWidget(len(ser1conts), 1, parent=self)
            table2 = QtGui.QTableWidget(len(ser2conts), 1, parent=self)
            table3 = QtGui.QTableWidget(len(ser3conts), 1, parent = self)
            
            for table in [table1, table2, table3]:
                table.setColumnWidth(0, 240)
                table.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)
            table1.setHorizontalHeaderLabels( [self.parent.ser1obj.name] )
            table2.setHorizontalHeaderLabels( [self.parent.ser2obj.name] )
            table3.setHorizontalHeaderLabels( ['Identical Contours'] )
            
            for row in range( len(ser1conts) ):
                tableItem = QtGui.QTableWidgetItem( ser1conts[row].name )
#                 tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table1.setItem(row, 0, tableItem)
            for row in range( len(ser2conts) ):
                tableItem = QtGui.QTableWidgetItem( ser2conts[row].name )
#                 tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table2.setItem(row, 0, tableItem)
            for row in range( len(ser3conts) ):
                tableItem = QtGui.QTableWidgetItem( ser3conts[row].name )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightGreen')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table3.setItem(row, 0, tableItem)
                
            self.table1 = table1
            self.table2 = table2
            self.table3 = table3
            self.s1c = ser1conts
            self.s2c = ser2conts
            self.mergedConts = ser3conts
            
        def returnItems(self): #=== multiple tables added
            selItems = self.table1.selectedItems()
            selItems.extend(self.table2.selectedItems())
            selConts = []
            for item in selItems: # Convert tableItem objects to contour objects
                if item.column() == 0:
                    selConts.append( self.s1c[item.row()] )
                if item.column() == 1:
                    selConts.append( self.s2c[item.row()] )
            return selConts

        def next(self):
            if ( len(self.mergedConts) + len(self.table1.selectedItems()) + len(self.table2.selectedItems())) != 20:
                msg = QtGui.QMessageBox(self)
                msg.setText('Please select a total of 20 items')
                msg.show()
            else:
                # Add the selectedItems() to self.mergedAtts
                self.parent.mergedSerContours = self.mergedConts.extend( self.returnItems() )
                
                # Disconnect buttons and load next window
                self.parent.nextButton.clicked.disconnect( self.next )
                self.parent.backButton.clicked.disconnect( self.back )
                mainFrame.seriesZContourWidget( self.parent )
                self.close()
            
        def back(self):
            # Disconnect buttons and load prev window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.seriesAttributeWidget(self.parent)
            self.close()
    
    class seriesZContourWidget(widgetWindow):
        def __init__(self, parent=None):
            widgetWindow.__init__(self, parent)
            self.table = None
            self.s1zc = None
            self.s2zc = None
            self.mergedZConts = None

            # Update mainFrame data
            self.parent.setWindowTitle('Series ZContours') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            
            rmt.mergeSeriesZContours(self.parent.ser1obj.contours,
                                                    self.parent.ser2obj.contours,
                                                    handler=self.serZContHandler)
            
            self.show()
            
        def serZContHandler(self, ser1zconts, ser2zconts, ser3zconts):
            self.s1zc = ser1zconts
            self.s2zc = ser2zconts
            self.mergedZConts = ser3zconts
            
            self.prepTables(ser1zconts, ser2zconts, ser3zconts)  

        def prepTables(self, ser1zconts, ser2zconts, ser3zconts):
            table = QtGui.QTableWidget( max(len(ser1zconts),len(ser2zconts)), 2, parent=self )
            table.setGeometry(0,0,800,500)
            table.setColumnWidth(0, 300)
            table.setColumnWidth(1, 300)
            table.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)
            for row in range( max(len(ser1zconts),len(ser2zconts)) ):
                # Series 1
                if row < len(ser1zconts): # Prevent index out of range
                    tableItem = QtGui.QTableWidgetItem( ser1zconts[row].name )
                    tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                    table.setItem(row, 0, tableItem)
                # Series 2
                if row < len(ser2zconts):
                    tableItem = QtGui.QTableWidgetItem( ser2zconts[row].name )
                    tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                    table.setItem(row, 1, tableItem)
            self.table = table
            self.table.show()
        
        def returnItems(self):
            selItems = self.table.selectedItems()
            selzConts = []
            for item in selItems:
                if item.column() == 0:
                    selzConts.append( self.s1zc[item.row()] )
                if item.column() == 1:
                    selzConts.append( self.s2zc[item.row()] )
            return selzConts   
        
        def next(self):
            self.mergedZConts.extend( self.returnItems() )
            self.parent.mergedSerZContours = self.mergedZConts
            
            # Disconnect buttons and load next window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionAttributeWidget( self.parent )
            self.close()
            
        def back(self):
            # Disconnect buttons and load prev window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.seriesContourWidget( self.parent )
            self.close()

    class sectionAttributeWidget(widgetWindow):
        #=== should be basically the same as seriesAttributeWidget()
        def __init__(self, parent=None):
            widgetWindow.__init__(self, parent)
             
            # Update mainFrame data
            self.parent.setWindowTitle('Section Attributes') #===
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            self.parent.ser1obj.getSectionsXML( self.parent.ser1path ) #=== taking too long, need some sort of msg?
            self.parent.ser2obj.getSectionsXML( self.parent.ser2path )
            self.parent.prepSlider() #===
            self.show()

        def next(self):
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionImageWidget( self.parent )
            self.close()
            
        def back(self):
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.seriesZContourWidget( self.parent )
            self.close()
                   
    class sectionImageWidget(widgetWindow):
        def __init__(self, parent=None):
            widgetWindow.__init__(self, parent)

            self.series1 = self.parent.ser1obj
            self.series2 = self.parent.ser2obj
            self.table = None
            self.imgConflicts = [] # list of lists of images for sections. len(inner-list) >1 if there's a conflict
             
            # Update mainFrame data
            self.parent.setWindowTitle('Section Images') #===
            self.parent.nextButton.clicked.connect( self.next ) #===
            self.parent.backButton.clicked.connect( self.back )
             
            # Find conflicting images
            for i in range(len(self.series1.sections)):
                self.imgConflicts.append( rmt.mergeSectionImgs(self.series1.sections[i],
                                     self.series2.sections[i],
                                     handler=self.secImgHandler) )
            self.prepTable()
            self.show()
          
        def secImgHandler(self, s1, s2):
            return [s1.imgs[0], s2.imgs[0]]
        
        def prepTable(self):
            table = QtGui.QTableWidget( len([conf for conf in self.imgConflicts if len(conf)>1]), 2, parent=self )
            table.setGeometry(0,0,800,500)
            table.setColumnWidth(0, 300)
            table.setColumnWidth(1, 300)
            
            sectionNames = []
            count = -1
            for i in range(len(self.imgConflicts)):
                if len(self.imgConflicts[i]) > 1:
                    count += 1
                    sectionNames.append( str(self.parent.serName)+'.'+str(i))
                    tableItem = QtGui.QTableWidgetItem( str(self.imgConflicts[i][0]) )
                    tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                    table.setItem(count, 0, tableItem)
                    tableItem = QtGui.QTableWidgetItem( str(self.imgConflicts[i][1]) )
                    tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                    table.setItem(count, 1, tableItem)
            table.setVerticalHeaderLabels(sectionNames)
            table.resizeRowsToContents()
            table.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)
            self.table = table
            self.table.show()
        
        def returnItems(self):
            selItems = self.table.selectedItems()
            for item in selItems:
                sectionNum = int(self.table.verticalHeaderItem(item.row()).text().rsplit('.')[1])
                if item.column() == 0:
                    self.imgConflicts[sectionNum] = self.series1.sections[sectionNum].imgs
                elif item.column() == 1:
                    self.imgConflicts[sectionNum] = self.series2.sections[sectionNum].imgs
            
        def next(self):
            self.returnItems()
            self.parent.mergedSecImages = self.imgConflicts
             
            # Check for no multiple images
            for item in self.parent.mergedSecImages:
                if len(item) != 1:
                    msg = QtGui.QMessageBox(self)
                    msg.setText('Please select one image per row')
                    msg.show()
                    return
            # Disconnect buttons and open next window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )

            self.parent.dispContourWidget()
            self.close()
           
        def back(self):
            # Disconnect buttons and open previous window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionAttributeWidget( self.parent )
            self.close()
            
    class sectionContourConflictResolver(widgetWindow):
        def __init__(self, parent=None, contA=None, contB=None):
            widgetWindow.__init__(self, parent)
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
            
            image = QtGui.QPixmap(parent=self.contAInfo) #=== TESTING IMAGES
            image.load('/home/michaelm/Documents/Test Series/rmtgTest/ser1/001____z0.0.tif')
            image = image.copy(QtCore.QRect(500,500,100,30))
            
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
            
            # Repetition checkboxes
            self.thisTraceAllSections = QtGui.QCheckBox()
            self.thisTraceAllSections.setText('Choose THIS particular trace in THIS series for ALL sections')
            self.thisTraceAllSections.stateChanged.connect(self.checkedBox)
            self.allTracesThisSection = QtGui.QCheckBox()
            self.allTracesThisSection.setText('Choose ALL of this series\' traces for THIS section')
            self.allTracesThisSection.stateChanged.connect(self.checkedBox)
            self.allTracesAllSections = QtGui.QCheckBox()
            self.allTracesAllSections.setText('Choose ALL of this series\' traces for ALL sections')
            self.allTracesAllSections.stateChanged.connect(self.checkedBox)
            
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
        
        def checkedBox(self):
            '''Maintains an exclusive implementation of checkboxes (i.e. unchecks others when one is checked)'''
            if self.sender() == self.thisTraceAllSections and self.thisTraceAllSections.checkState() == QtCore.Qt.Checked:
                self.allTracesThisSection.setCheckState(QtCore.Qt.Unchecked)
                self.allTracesAllSections.setCheckState(QtCore.Qt.Unchecked)
            elif self.sender() == self.allTracesThisSection and self.allTracesThisSection.checkState() == QtCore.Qt.Checked:
                self.thisTraceAllSections.setCheckState(QtCore.Qt.Unchecked)
                self.allTracesAllSections.setCheckState(QtCore.Qt.Unchecked)
            elif self.sender() == self.allTracesAllSections and self.allTracesAllSections.checkState() == QtCore.Qt.Checked:
                self.thisTraceAllSections.setCheckState(QtCore.Qt.Unchecked)
                self.allTracesThisSection.setCheckState(QtCore.Qt.Unchecked)

        def buttonClicked(self): #===
            for button in [self.contAButton, self.contBButton, self.bothButton]:
                if button == self.sender():
                    button.setFlat(True) #=== change color
                    button.setAutoFillBackground(True)
                else:
                    button.setFlat(False)
                    button.setAutoFillBackground(False)

    class sectionContourWidget(widgetWindow):
        def __init__(self, parent=None, section=None):
            widgetWindow.__init__(self, parent)
            self.table1 = None # Series 1 table
            self.table2 = None # Merge table
            self.table3 = None # Series 2 table
            self.section = section
            
            # Original contours, DO NOT CHANGE IN FUNCTIONS 
            self.uniqueA = None
            self.compOvlp = None
            self.confOvlp = None
            self.uniqueB = None
            
            # Contours to be output into the merged series, CHANGE THESE WITH FUNCTIONS
            self.confOvlpout = [] # for resolved conflicts
            self.allOutContours = None
            
            # Update mainFrame data
            self.parent.setWindowTitle('Section Contours') #===
            
            # Load widget for each section into self.parent.tempContours
            self.prepTables(*rmt.mergeSectionContours(self.parent.ser1obj.sections[self.section],
                                                     self.parent.ser2obj.sections[self.section],
                                                     handler=self.secContHandler))
            self.prepButtonFunctionality()
            self.prepLayout()
        
        def secContHandler(self, uniqueA, compOvlp, confOvlp, uniqueB):
            '''rmtgui version of section contour handler'''
            self.uniqueA = uniqueA
            self.compOvlp = compOvlp
            self.confOvlp = confOvlp
            self.uniqueB = uniqueB
            return uniqueA, compOvlp, confOvlp, uniqueB

        def prepButtonFunctionality(self):
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.backButton.clicked.connect( self.back )
            # What happens when you double click a table item?
            self.table1.itemDoubleClicked.connect( self.showDetail )
            self.table2.itemDoubleClicked.connect( self.resolveConflict )
            self.table3.itemDoubleClicked.connect( self.showDetail )
            
        def prepLayout(self):
            self.parent.slider.show()
            self.parent.label.show()
            
            # Layout
            vbox = QtGui.QVBoxLayout() # Holds all the boxes below
            hbox1 = QtGui.QHBoxLayout() # For the 3 tables
            hbox1.addWidget(self.table1) # Series 1
            hbox1.addWidget(self.table2) # Conflicts/merges
            hbox1.addWidget(self.table3) # Series 2
            vbox.addLayout(hbox1)
            self.setLayout(vbox)
            
        def prepTables(self, s1unique, ovlps, confs, s2unique):
            table1 = QtGui.QTableWidget(len(s1unique), 1, parent=self)
            table2 = QtGui.QTableWidget(len(confs)+len(ovlps), 1, parent=self)
            table3 = QtGui.QTableWidget(len(s2unique), 1, parent=self)
            
            # Load labels/items into tables
            table1.setHorizontalHeaderLabels(['Unique 1'])
            for row in range(len(s1unique)):
                tableItem = QtGui.QTableWidgetItem( s1unique[row].name )
#                 tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table1.setItem(row, 0, tableItem)
                
            table2.setHorizontalHeaderLabels(['Conflicts/Overlaps'])
            row = 0
            for elem in confs:
                tableItem = QtGui.QTableWidgetItem( elem[0].name )
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('pink')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table2.setItem(row, 0, tableItem)
                row+=1
            for elem in ovlps:
                tableItem = QtGui.QTableWidgetItem( elem[0].name)
                tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightGreen')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table2.setItem(row, 0, tableItem)
                row+=1
                    
            table3.setHorizontalHeaderLabels(['Unique 2'])
            for row in range(len(s2unique)):
                tableItem = QtGui.QTableWidgetItem( s2unique[row].name )
#                 tableItem.setBackground(QtGui.QBrush(QtGui.QColor('lightCyan')))
                tableItem.setTextAlignment(QtCore.Qt.AlignCenter)
                table3.setItem(row, 0, tableItem)
            
            # Apply changes to tables
            for table in [table1,table2,table3]:
                table.setSelectionMode(QtGui.QAbstractItemView.SelectionMode.MultiSelection)
                table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
                table.setColumnWidth(0,240)
            
            # Assign tables to self
            self.table1 = table1
            self.table2 = table2
            self.table3 = table3
            return self
            
        def resolveConflict(self, item):
            row = item.row()
            pink = '#ffc0cb'
            yellow = '#ffff66'
            if item.background().color().name() in [pink, yellow]: # If background color = pink (i.e. is a conflict)
                self.showConfDetails( *self.returnConfConts(row) )
#                 self.itemToYellow(item) #=== changed to update only when conflict resolved
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
            if table == self.table1: cont = self.uniqueA[row]
            elif table == self.table2: cont = self.compOvlp[row][0]
            elif table == self.table3: cont = self.uniqueB[row]
            
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
        
        def showConfDetails(self, confA, confB, row):
            '''Gives more detail of the contours in conflict'''
            item = self.table2.item(row, 0)
            def pickConfA():
                '''Adds contour A to the output contour list'''
                if confA not in self.confOvlpout: self.confOvlpout.append(confA)
                if confB in self.confOvlpout: self.confOvlpout.remove(confB)
                item.setText(confA.name)
                item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.itemToYellow(item) #===
                res.close()
                
            def pickConfB():
                '''Adds contour B to the output contour list'''
                if confB not in self.confOvlpout: self.confOvlpout.append(confB)
                if confA in self.confOvlpout: self.confOvlpout.remove(confA)
                item.setText(confB.name)
                item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
                self.itemToYellow(item) #===
                res.close()
                
            def pickBoth():
                if confA not in self.confOvlpout: self.confOvlpout.append(confA)
                if confB not in self.confOvlpout: self.confOvlpout.append(confB)
                item.setText('-------------> '+confA.name+' <-------------') #=== confA.name?
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.itemToYellow(item) #===
                res.close()#=== Remove for deploy
                
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
        
        def loadOutList(self): #===
            self.allOutContours = []
            t1items = self.table1.selectedItems()
            t2items = self.table2.selectedItems()
            t3items = self.table3.selectedItems()
            
            # Unique A
            for item in t1items:
                row = item.row()
                cont = self.uniqueA[row]
                self.allOutContours.append(cont)
                
            # Comp ovlp
            for item in t2items:
                green = '#90ee90'
                if item.background().color().name() == green: # Added when confl is resolved
                    row = item.row()-len(self.confOvlp)
                    cont = self.compOvlp[row][0]
                    self.allOutContours.append(cont)
            
            # Conflict ovlp; only adds selected AND resolved conflicts
            for item in t2items:
                row = item.row()
                if row < len(self.confOvlp):
                    for resConf in self.confOvlpout:
                        if resConf == self.confOvlp[row][0]:
                            self.allOutContours.append(resConf)
                        if resConf == self.confOvlp[row][1]:#=== Remove for deploy
                            self.allOutContours.append(resConf)
                        
            # Unique B
            for item in t3items:
                row = item.row()
                cont = self.uniqueB[row]
                self.allOutContours.append(cont)

            print('Section '+str(self.section)+' output: '+str([cont.name for cont in self.allOutContours])) #===
        
        def itemToYellow(self, item):
            item.setBackground(QtGui.QBrush(QtGui.QColor('#ffff66')))

        def next(self): #=== add a double-check message to make sure all sections are complete
            self.loadOutList()
            self.parent.mergedSecContours.append(self.allOutContours)
            # Hide section slider
            self.parent.slider.hide()
            self.parent.label.hide()
            # Disconnect buttons and load next window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.outputWidget( self.parent )
            self.close()
  
        def back(self):
            # Hide slider/label
            self.parent.slider.hide()
            self.parent.label.hide()
            # Disconnect buttons and load previous window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.backButton.clicked.disconnect( self.back )
            mainFrame.sectionImageWidget( self.parent )

            self.close()
           
    class outputWidget(widgetWindow):
        def __init__(self, parent=None):
            widgetWindow.__init__(self, parent)
            
            # Update mainFrame data
            self.parent.setWindowTitle('Merged Series Output') #===
            
            self.outBar = None
            self.nameBar = None
            self.outBarBrowse = None
            
            self.prepFuncObjs()
            self.prepLayout()
            self.show()
            
        def prepFuncObjs(self):
            self.parent.nextButton.clicked.connect( self.next )
            self.parent.nextButton.setText('Finish and close') #===
            self.parent.backButton.clicked.connect( self.back )
            
            # Output path edit bar
            self.outBar = QtGui.QLineEdit(self)
            self.outBar.setText(self.parent.outputPath)
            
            # Series name bar
            self.nameBar = QtGui.QLineEdit(self)
            self.nameBar.setText( self.parent.serName )
            
            # Output path browse button
            self.outBarBrowse = QtGui.QPushButton(self)
            self.outBarBrowse.setIconSize(QtCore.QSize(25,25))
            self.outBarBrowse.setText('Browse')
            self.outBarBrowse.clicked.connect( self.browseOutPath )
            
        def prepLayout(self):
            # Layout
            hbox = QtGui.QHBoxLayout()
            hbox.addWidget(self.outBar)
            hbox.addWidget(self.outBarBrowse)
            hbox.insertSpacing(0,150)
            hbox.insertSpacing(-1,150)
            
            hbox2 = QtGui.QHBoxLayout()
            hbox2.addWidget(self.nameBar)
            hbox2.insertSpacing(0,300)
            hbox2.insertSpacing(-1,300)
            
            vbox = QtGui.QVBoxLayout()
            vbox.insertSpacing(0,200)

            vbox.addLayout(hbox)
            vbox.addLayout(hbox2)

            self.setLayout(vbox)
            
        def browseOutPath(self):
            path = QtGui.QFileDialog.getExistingDirectory(self,
                                                     'Select Output Directory',
                                                     '/home/')
            path = str(path)+'/' # extract path and turn unicode -> regstr
            self.parent.outputPath = path
            self.outBar.setText(path)
            
        def combineMergedStuff(self): #=== Test for completion
            '''Combines all the merged stuff for output'''
            print('1: '+str(self.parent.mergedSeries))
            print('2: '+str(self.parent.mergedAttributes))
            print('3: '+str(self.parent.mergedSerContours))
            print('4: '+str(self.parent.mergedSerZContours))
            print('5: '+str(self.parent.mergedSecList))
            print('6: '+str(self.parent.mergedSecAttributes))
            print('7: '+str(self.parent.mergedSecImages))
            print('8: '+str(self.parent.mergedSecContours))
            
        def outputName(self):
            if str( self.nameBar.text() ) != str( self.parent.serName ):
                self.parent.serName = str( self.nameBar.text() )
                self.parent.mergedSeries.name = str( self.nameBar.text() )
                    
                count=-1
                for section in self.parent.mergedSeries.sections:
                    count+=1
                    section.name = str( self.nameBar.text() )+'.'+str( count )
                    print(section.name)
                    
        def next(self):
            # Output merged series, close program (restart program?)
            if '/' in self.parent.outputPath:
                if self.parent.outputPath[-1] != '/':
                    self.parent.outputPath+='/'
                
                self.outputName()
                self.combineMergedStuff()
                
                self.parent.mergedSeries.writeseries( self.parent.outputPath )
                self.parent.mergedSeries.writesections( self.parent.outputPath )
                self.close()
                quit() 
            else:
                msg = QtGui.QMessageBox(self)
                msg.setText('Invalid directory, please fix')
                msg.show()
            
        def back(self): #===
            # Reload contourWidget and slider
            self.parent.slider.show()
            self.parent.label.show()
            self.parent.currentWidget.show()
            
            #=== Disconnect buttons, reconnect prev buttons, and load previous window
            self.parent.nextButton.clicked.disconnect( self.next )
            self.parent.nextButton.setText('Next')
            self.parent.backButton.clicked.disconnect( self.back )
            self.close()
            
def main():
    app = QtGui.QApplication(sys.argv)
    rmtFrame = mainFrame()
#     mainFrame.serLoadWidget(rmtFrame)
    mainFrame.sectionContourConflictResolver(rmtFrame)
    sys.exit( app.exec_() )
main()


