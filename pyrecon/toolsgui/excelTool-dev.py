from PySide import QtCore, QtGui
import sys, os

class objectListWidget(QtGui.QWidget):
    def __init__(self, parent=None, width=None, height=None):
        QtGui.QWidget.__init__(self, parent)
        # Size (1/3 of total width?) #=== how to make scalable?
        self.setGeometry(0,0,width,height)
        self.initFilterLine()
        self.initTable()
        self.initLayout()
        self.show()
    
    def initFilterLine(self):
        self.filterLine = QtGui.QLineEdit(self)
        self.filterLine.setText('Enter object list filters, separated by commas')
        self.refreshButton = QtGui.QPushButton(self)
        # Refresh arrows in button, resize to square #===
#         self.refreshButton.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
#         self.refreshButton.setText('Refresh')
    
    def initTable(self):
        self.table = QtGui.QTableWidget(40,1,self)
        self.table.verticalHeader().setVisible(False) # No row numbers
        self.table.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored) # Scales with anysize window, necessary? #===
        self.table.setHorizontalHeaderLabels(['Objects'])
        self.table.resizeRowsToContents()
        self.table.setColumnWidth(0, 240) #=== Replace 240 with scalable width

        #=== Test Items
        for i in range(40):
            item = QtGui.QTableWidgetItem('Item '+str(i+1))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(i,0,item)
        
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