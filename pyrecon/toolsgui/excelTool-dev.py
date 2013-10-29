from PySide import QtCore, QtGui
from pyrecon.tools import classes
import sys, os

# Current issues:
# - Refresh button should be square with arrow-circle in it

class ObjectListWidget(QtGui.QWidget):
    def __init__(self, parent=None, width=None, height=None):
        QtGui.QWidget.__init__(self, parent)
        # Size (1/3 of total width?) #=== how to make scalable?
        self.setGeometry(0,0,width,height)
        self.initUI()
        
    def initUI(self):
        '''Initial load of layout/objects'''
        self.series = classes.loadSeries('/home/michaelm/Documents/Test Series/test/ser1/BBCHZ.ser')
        self.objects = classes.rObjectsFromSeries(self.series)

        self.initFilterLine()
        self.loadTable(rows=len(self.objects),cols=1)
        self.initLayout()
        self.show()
        
    def initFilterLine(self):
        '''Loads filter input line and refresh button'''
        self.filterLine = QtGui.QLineEdit(self)
        self.filterLine.setText('Enter filters, separated by commas')
        self.refreshButton = QtGui.QPushButton('Refresh')
        self.refreshButton.clicked.connect( self.refresh )
    
    def loadTable(self, rows, cols):
        '''Creates a QTableWidget with specified parameters'''
        self.table = QtGui.QTableWidget(len(self.objects), cols, self)
        
        for object in range(len(self.objects)):
            item = QtGui.QTableWidgetItem(str(self.objects[object]))
            self.table.setItem(1,0,item)
        
        self.table.verticalHeader().setVisible(False) # No row numbers
        self.table.setHorizontalHeaderLabels(['Objects'])
        self.table.resizeRowsToContents() # Reduces item row height to minimum         
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch) # Keeps columns at width of window
        
    def initLayout(self):
        filterLineBox = QtGui.QHBoxLayout()
        filterLineBox.addWidget(self.filterLine)
        filterLineBox.addWidget(self.refreshButton)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(filterLineBox)
        vbox.addWidget(self.table)
        
        self.setLayout(vbox)
            
    def refresh(self):
        # Reload table with new specs
        try:
            self.objects = classes.rObjectsFromSeries(self.series)
            self.loadTable(rows=len(self.objects), cols=1)
            self.initUI()
            print( 'refreshing table') #===
        except:
            print ('No series file loaded')
        
app = QtGui.QApplication(sys.argv)
objL = ObjectListWidget(width=300, height=800)
sys.exit( app.exec_() )