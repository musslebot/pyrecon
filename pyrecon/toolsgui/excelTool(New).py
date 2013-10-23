from PySide import QtCore, QtGui
import sys, os

class mainContainer(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setGeometry(0,0,1092,728)
        self.setWindowTitle('RECONSTRUCT Spreadsheet Tool')
        
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.frame.setGeometry(self.geometry())
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(3)
        
        menuBar = QtGui.QMenuBar(self.frame)
        menuBar.addMenu('&File')
        menuBar.addMenu('&Edit')
        
        self.sheetWindow = spreadsheetWindow(parent=self)
        
        self.show()

class spreadsheetWindow(QtGui.QWidget):
    '''Window containing the spreadsheet.'''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(0,25,1092,678)
        self.loadSpreadsheet()
        self.loadObjectList()
        self.loadLayout()
        self.show()
    
    def loadSpreadsheet(self):
        self.sheet = QtGui.QTableWidget(42, 42, self)

    def loadObjectList(self):
        self.objList = QtGui.QTableWidget(10, 1, self)
        self.objList.setFixedWidth(200)
        self.objList.setColumnWidth(0,200)
        self.objList.setHorizontalHeaderLabels(['RECONSTRUCT Objects'])
        self.objList.verticalHeader().setVisible(False)
        
    def loadLayout(self):
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.objList)
        hbox.addWidget(self.sheet)

        self.setLayout(hbox)
        
app = QtGui.QApplication(sys.argv)
t = mainContainer()
sys.exit( app.exec_() )