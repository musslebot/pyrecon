#!/usr/bin/env python
import sys
from pyrecon.excelTool import excelTool
from PySide.QtGui import *
from PySide.QtCore import *

class excelToolWindow(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
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
        self.seriesPathLine = QLineEdit(self)
        self.seriesPathLine.setText( self.seriesPath )
        self.seriesPathLine.setAlignment( Qt.AlignCenter )
        
        self.seriesPathBrowse = QPushButton(self)
        self.seriesPathBrowse.clicked.connect( self.browse )
        self.seriesPathBrowse.setIconSize(QSize(25,25))
        self.seriesPathBrowse.setText('Browse')
        
        self.savePathLine = QLineEdit(self)
        self.savePathLine.setText( self.savePath )
        self.savePathLine.setAlignment( Qt.AlignCenter ) #===
        
        self.savePathBrowse = QPushButton(self)
        self.savePathBrowse.clicked.connect( self.browse )
        self.savePathBrowse.setIconSize(QSize(25,25))
        self.savePathBrowse.setText('Browse')
        
        self.goButton = QPushButton(self)
        self.goButton.setText('Create Excel Workbook (.xlsx)')
        self.goButton.clicked.connect( self.checkAndFinish )
        self.goButton.setMinimumHeight(50)
        self.goButton.setFlat(True)

    def layout(self):
        vbox = QVBoxLayout()
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget( self.seriesPathLine )
        hbox1.addWidget( self.seriesPathBrowse )
        hbox1.insertSpacing(0,25)
        hbox1.insertSpacing(-1,25)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget( self.savePathLine )
        hbox2.addWidget( self.savePathBrowse )
        hbox2.insertSpacing(0,25)
        hbox2.insertSpacing(-1,25)
        
        hbox3 = QHBoxLayout()
        hbox3.insertSpacing(0,225)
        hbox3.addWidget( self.goButton )
        hbox3.insertSpacing(-1,225)
        
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        self.setLayout(vbox)

    def browse(self):
            if self.sender() == self.seriesPathBrowse:
                path = QFileDialog.getOpenFileName(self,
                                                     'Load Series',
                                                     '/home/',
                                                     'Series File (*.ser)')
                path = str(path[0])
                if path != '':
                    self.seriesPathLine.setText(path)
                
            elif self.sender() == self.savePathBrowse:
                path = str( QFileDialog.getExistingDirectory(self) )
                if path != '':
                    self.savePathLine.setText(path)
                self.goButton.setFlat(False)
    def checkAndFinish(self):
        self.seriesPath = self.seriesPathLine.text()
        self.savePath = self.savePathLine.text()
        if '.ser' not in self.seriesPath:
            msg = QMessageBox(self)
            msg.setText('Invalid series file -- Please try again.')
            msg.show()
        if self.savePath == 'Enter or browse path to save excel workbook' or '/' not in self.savePath:
            msg = QMessageBox(self)
            msg.setText('Invalid save path!')
            msg.show()
        else:
            excelTool.main(str(self.seriesPath), str(self.savePath))
            self.close()
    