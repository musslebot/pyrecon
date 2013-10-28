from PySide import QtCore, QtGui
from pyrecon.tools import classes
import sys, os

# Current issues:
# - Refresh button should be square with arrow-circle in it

class objectListWidget(QtGui.QWidget):
    def __init__(self, parent=None, width=None, height=None):
        QtGui.QWidget.__init__(self, parent)
        # Size (1/3 of total width?) #=== how to make scalable?
        self.setGeometry(0,0,width,height)
        
        #===
        self.series = classes.loadSeries('/home/michaelm/Documents/Test Series/test/ser1/BBCHZ.ser')
        self.objects = classes.rObjectsFromSeries(self.series)
        
        self.initFilterLine()
        self.initTable(rows=40,cols=1) # set initial table size, changed with refreshTable(self)
        self.initLayout()
        self.show()
    
    def refreshTable(self):
        # Reload table with new specs
        self.objects = classes.rObjectsFromSeries(self.series)
        self.initTable(rows=len(self.objects), cols=1)
        
    def initFilterLine(self):
        self.filterLine = QtGui.QLineEdit(self)
        self.filterLine.setText('Enter filters, separated by commas')
        self.refreshButton = QtGui.QPushButton('Refresh')
        self.refreshButton.clicked.connect( self.refreshTable )
    
    def initTable(self, rows, cols):
        self.table = QtGui.QTableWidget(rows,cols,self)
        self.table.verticalHeader().setVisible(False) # No row numbers
        self.table.setHorizontalHeaderLabels(['Objects'])
        self.table.resizeRowsToContents() # Reduces item row height to minimum 
        
        row = 0 #=== space before loading correct object 
        for obj in self.objects:
            print(row)
            item = QtGui.QTableWidgetItem(obj.name)
            self.table.setItem(row, cols, item)
            row+=1
        
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch) # Keeps columns at width of window
        
    def initLayout(self):
        filterLineBox = QtGui.QHBoxLayout()
        filterLineBox.addWidget(self.filterLine)
        filterLineBox.addWidget(self.refreshButton)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(filterLineBox)
        vbox.addWidget(self.table)
        
        self.setLayout(vbox)
         
app = QtGui.QApplication(sys.argv)
objL = objectListWidget(width=300, height=800)
sys.exit( app.exec_() )