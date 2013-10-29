from PySide import QtCore, QtGui
from pyrecon.tools import classes
import sys, os, re
# THIS IS A DEVELOPMENT FILE AND SHOULD NOT BE EXPECTED TO WORK
# Current issues:
# * Can't load multiple series into QListWidget simultaneously
# * Needs to filter multiple things

class ObjectListWidget(QtGui.QWidget):
    def __init__(self, parent=None, width=None, height=None):
        QtGui.QWidget.__init__(self, parent)
        # Size (1/3 of total width?) #=== how to make scalable?
        self.setGeometry(0,0,width,height)
        
        self.initObjects()
        self.initLayout()
        
        self.show()
        
    def initObjects(self):
        self.filter = QtGui.QLineEdit()
        self.filter.setText('Enter filters, sep. by commas')
        
        self.refBut = QtGui.QPushButton()
        self.refBut.setText('Refresh')
        self.refBut.clicked.connect( self.ref )
        
        self.objList = QtGui.QListWidget()
        
        self.addSerBut = QtGui.QPushButton()
        self.addSerBut.setText('Add Series')
        self.addSerBut.clicked.connect( self.addSer )
        
        self.delSerBut = QtGui.QPushButton()
        self.delSerBut.setText('Remove Series')
        self.delSerBut.clicked.connect( self.delSer )
        
        self.objects = None
        
    def initLayout(self):
        widgetLayout = QtGui.QVBoxLayout()
        
        filterBox = QtGui.QHBoxLayout()
        filterBox.addWidget( self.filter )
        filterBox.addWidget( self.refBut )
        widgetLayout.addLayout(filterBox)
        
        listBox = QtGui.QHBoxLayout()
        listBox.addWidget( self.objList )
        widgetLayout.addLayout(listBox)
        
        modListBox = QtGui.QHBoxLayout()
        modListBox.addWidget( self.addSerBut )
        modListBox.addWidget( self.delSerBut )
        widgetLayout.addLayout(modListBox)
        
        self.setLayout(widgetLayout)
    
    def ref(self): #===
        self.objList.clear()
        filters = self.filter.text()
        if self.objects is not None:
            allObjects = sorted([object.name for object in self.objects])
            filteredObjects = [name for name in allObjects if str(filters) not in name] #=== filtering line
            
            if filters != 'Enter filters, sep. by commas' and filters != '':
                print 'Filter the list'
                self.objList.addItems(filteredObjects)
            else:
                print 'invalid filter'
                self.objList.addItems(allObjects)
        print filters
    
    def addSer(self):
        def getObjects():
            path = QtGui.QFileDialog.getOpenFileName(self, 'Series File', '/home/', 'Series Files (*.ser)')
            path = str(path[0])
            ser = classes.loadSeries(path)
            self.objects = classes.rObjectsFromSeries(ser)
            self.ref()
        msg = QtGui.QMessageBox(self)
        msg.setText('This process may take a moment, please be patient.')
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        ret = msg.exec_()
        if ret == QtGui.QMessageBox.Ok:
            getObjects()

    def delSer(self):
        print('del ser')

    
        
        
        
        
#===== Below is pre-ListWidget        
#     def initFilterLine(self):
#         '''Loads filter input line and refresh button'''
#         self.filterLine = QtGui.QLineEdit(self)
#         self.filterLine.setText('Enter filters, separated by commas')
#         self.refreshButton = QtGui.QPushButton('Refresh')
#         self.refreshButton.clicked.connect( self.refresh )
#         self.addSeriesButton = QtGui.QPushButton('Add Series')
#         self.addSeriesButton.clicked.connect( self.addSeries )
#         self.removeSeriesButton = QtGui.QPushButton('Remove Series')
#         self.removeSeriesButton.clicked.connect( self.remSeries )
#     
#     def loadList(self, rows, cols):
#         '''Creates a QListWidget with specified parameters'''
#         self.oList = QtGui.QListWidget(len(self.objects), cols, parent=self)
#         
#         for object in range(len(self.objects)):
#             item = QtGui.QListWidgetItem(str(self.objects[object]))
#             print(object)
#             self.oList.setItem(object,0,item)
#         
#         self.oList.verticalHeader().setVisible(False) # No row numbers
#         self.oList.setHorizontalHeaderLabels(['Objects'])
#         self.oList.resizeRowsToContents() # Reduces item row height to minimum         
#         self.oList.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch) # Keeps columns at width of window
#         
#     def initLayout(self):
#         filterLineBox = QtGui.QHBoxLayout()
#         filterLineBox.addWidget(self.filterLine)
#         filterLineBox.addWidget(self.refreshButton)
#         
#         bottomButBox = QtGui.QHBoxLayout()
#         bottomButBox.addWidget(self.addSeriesButton)
#         bottomButBox.addWidget(self.removeSeriesButton)
#         
#         vbox = QtGui.QVBoxLayout()
#         vbox.addLayout(filterLineBox)
#         vbox.addWidget(self.oList)
#         vbox.addLayout(bottomButBox)
#         
#         self.setLayout(vbox)
#     
#     def addSeries(self): #===
#         print 'add series'
#     def remSeries(self): #===
#         print 'rem series'
#     def refresh(self):
#         # Reload list with new specs
#         try:
#             self.oList.clearContents()
#             self.initUI()
#             print('refreshing list') #===
#         except:
#             print ('No series file loaded')
        
app = QtGui.QApplication(sys.argv)
objL = ObjectListWidget(width=300, height=800)
sys.exit( app.exec_() )