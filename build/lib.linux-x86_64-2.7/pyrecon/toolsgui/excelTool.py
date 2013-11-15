#!/usr/bin/env python
import sys
from pyrecon.tools import excelTool
from PySide import QtGui, QtCore

class excelToolWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.setGeometry(0,0,500,200)
        
        self.seriesPathLine = None
        self.seriesPathBrowse = None
        self.seriesPath = 'Enter or browse path to series'
        
        self.savePathLine = None
        self.savePathBrowse = None
        self.savePath = 'Enter or browse path to save excel workbook'
        
        self.goButton = None
        
        # GUI Start Functions
        self.functionalItems()
        self.layout()
        self.show()
        
    def functionalItems(self):
        self.seriesPathLine = QtGui.QLineEdit(self)
        self.seriesPathLine.setText( self.seriesPath )
        self.seriesPathLine.setAlignment( QtCore.Qt.AlignCenter )
        
        self.seriesPathBrowse = QtGui.QPushButton(self)
        self.seriesPathBrowse.clicked.connect( self.browse )
        self.seriesPathBrowse.setIconSize(QtCore.QSize(25,25))
        self.seriesPathBrowse.setText('Browse')
        
        self.savePathLine = QtGui.QLineEdit(self)
        self.savePathLine.setText( self.savePath )
        self.savePathLine.setAlignment( QtCore.Qt.AlignCenter ) #===
        
        self.savePathBrowse = QtGui.QPushButton(self)
        self.savePathBrowse.clicked.connect( self.browse )
        self.savePathBrowse.setIconSize(QtCore.QSize(25,25))
        self.savePathBrowse.setText('Browse')
        
        self.goButton = QtGui.QPushButton(self)
        self.goButton.setText('Create Excel Workbook (.xlsx)')
        self.goButton.clicked.connect( self.checkAndFinish )

    def layout(self):
        vbox = QtGui.QVBoxLayout()
        
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget( self.seriesPathLine )
        hbox1.addWidget( self.seriesPathBrowse )
        hbox1.insertSpacing(0,25)
        hbox1.insertSpacing(-1,25)
        
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget( self.savePathLine )
        hbox2.addWidget( self.savePathBrowse )
        hbox2.insertSpacing(0,25)
        hbox2.insertSpacing(-1,25)
        
        hbox3 = QtGui.QHBoxLayout()
        hbox3.insertSpacing(0,225)
        hbox3.addWidget( self.goButton )
        hbox3.insertSpacing(-1,225)
        
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        self.setLayout(vbox)

    def browse(self):
            if self.sender() == self.seriesPathBrowse:
                path = QtGui.QFileDialog.getOpenFileName(self,
                                                     'Load Series',
                                                     '/home/',
                                                     'Series File (*.ser)')
                path = str(path[0])
                if path != '':
                    self.seriesPathLine.setText(path)
                
            elif self.sender() == self.savePathBrowse:
                path = str( QtGui.QFileDialog.getExistingDirectory(self) )
                if path != '':
                    self.savePathLine.setText(path)
                      
    def checkAndFinish(self):
        self.seriesPath = self.seriesPathLine.text()
        self.savePath = self.savePathLine.text()
        if '.ser' not in self.seriesPath:
            msg = QtGui.QMessageBox(self)
            msg.setText('Invalid series file -- Please try again.')
            msg.show()
        if self.savePath == 'Enter or browse path to save excel workbook' or '/' not in self.savePath:
            msg = QtGui.QMessageBox(self)
            msg.setText('Invalid save path!')
            msg.show()
        else:
            print('Continuing...')
            print(self.seriesPath)
            print(self.savePath)
            excelTool.main(self.seriesPath, self.savePath)
            self.close()
            
def main():
    app = QtGui.QApplication(sys.argv)
    t = excelToolWindow()
    sys.exit( app.exec_() )
main()
    