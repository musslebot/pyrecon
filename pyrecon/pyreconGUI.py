'''Contains graphical components of PyRECONSTRUCT that are used accross multple tools.'''
from PySide.QtCore import *
from PySide.QtGui import *
import pyrecon
# Pyrecon tool modules imported when called by their functions below

class pyreconMainWindow(QMainWindow):
    '''Main PyRECONSTRUCT window.'''
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setWindowTitle('PyRECONSTRUCT')
        self.loadMenus()
        self.show()
        newSize = QDesktopWidget().availableGeometry().size() / 4
        self.resize( newSize )
        self.statusBar().showMessage('Ready! Welcome to PyRECONSTRUCT')
    def loadMenus(self):
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.loadToolsMenu()
        self.helpMenu = self.menuBar().addMenu("&Help")
    def loadToolsMenu(self):
        # 1) Create Actions
        # - mergeTool
        mergeAction = QAction( QIcon(), 'mergeTool', self ) #QIcon() is null, but necessary for Action creation
        mergeAction.triggered.connect( self.loadMergeTool )
        mergeAction.setStatusTip( 'Open merge widget' )
        # - calibrationTool
        calibAction = QAction( QIcon(), 'calibrationTool', self )
        calibAction.triggered.connect( self.loadCalibrationTool )
        calibAction.setStatusTip( 'Open calibration widget' )
        # - excelTool
        excelAction = QAction( QIcon(), 'excelTool', self )
        excelAction.triggered.connect( self.loadExcelTool )
        excelAction.setStatusTip( 'Open excel widget' )
        # - curationTool
        curateAction = QAction( QIcon(), 'curationTool', self )
        curateAction.triggered.connect( self.loadCurationTool )
        curateAction.setStatusTip( 'Open curation widget' )
        # 2) Add actions to toolbars
        self.toolsMenu.addAction( mergeAction )
        self.toolsMenu.addAction( calibAction )
        self.toolsMenu.addAction( excelAction )
        self.toolsMenu.addAction( curateAction )
    def loadMergeTool(self):
        from pyrecon.mergeTool.gui.mergeGUI import mergeSelection
        self.mergeSelector = QDockWidget() # Left dockWidget
        mergeSel = mergeSelection(self)
        self.mergeSelector.setWidget( mergeSel )
        self.addDockWidget( Qt.LeftDockWidgetArea, self.mergeSelector )
        # stackedWidget contains each mergeItem's resolution wrapper
        self.resolutionStack = QStackedWidget()
        self.setCentralWidget( self.resolutionStack )
    def loadCurationTool(self): #===
        from pyrecon.curationTool.gui.curationGUI import curationToolStuff
        # Left dockWidget: load series/options
        self.curateSelector = QDockWidget()
        self.curationTool = curationToolStuff(self)
        self.curateSelector.setWidget( self.curationTool )
        self.addDockWidget( Qt.LeftDockWidgetArea, self.curateSelector )
        self.setCentralWidget(self.curationTool.output)

    def loadCalibrationTool(self): #===
        print('Load calibration widget')
    def loadExcelTool(self): #===
        print('Load excel widget')
    

class browseWidget(QWidget):
    '''Provides a QLineEdit and button for browsing through a file system. browseType can be directory, file or series but defaults to directory.'''
    def __init__(self, browseType='directory'):
        QWidget.__init__(self)
        self.loadObjects(browseType)
        self.loadFunctions(browseType)
        self.loadLayout()
    def loadObjects(self, browseType):
        # Path entry area
        self.path = QLineEdit()
        if browseType == 'directory':
            title = 'Enter or browse path to directory'
        elif browseType == 'file':
            title = 'Enter or browse path to file'
        else:
            title = 'Enter or browse path'
        self.path.setText(title)
        # Browse button
        self.browseButton = QPushButton()
        self.browseButton.setText('Browse')
    def loadFunctions(self, browseType):
        if browseType == 'directory':
            self.browseButton.clicked.connect( self.browseDir )
        elif browseType == 'file':
            self.browseButton.clicked.connect( self.browseFile )
        elif browseType == 'series':
            self.browseButton.clicked.connect( self.browseSeries )
    def loadLayout(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.path)
        hbox.addWidget(self.browseButton)
        self.setLayout(hbox)
    def browseDir(self):
        dirName = QFileDialog.getExistingDirectory(self)
        self.path.setText( str(dirName) )
    def browseFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "/home/")
        self.path.setText( str(fileName[0]))
    def browseSeries(self):
        fileName = QFileDialog.getOpenFileName(self, "Open Series", "/home/", "Series File (*.ser)")
        self.path.setText( str(fileName[0]))

class singleSeriesLoad(QDialog):
    '''Dialog for loading series files into memory as pyrecon.classes.Series objects'''
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.series = browseWidget(browseType='series')
        self.closeButton = QPushButton()
        self.closeButton.setText('Load Series')
    def loadFunctions(self):
        self.closeButton.clicked.connect( self.loadClose )
    def loadLayout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.series)
        vbox.addWidget(self.closeButton)
        self.setLayout(vbox)
    def loadClose(self):
        # Add paths to self.output
        self.output = str(self.series.path.text())
        self.close()

class doubleSeriesLoad(QDialog):
    '''Dialog for loading series files into memory as pyrecon.classes.Series objects'''
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.series1 = browseWidget(browseType='series')
        self.series2 = browseWidget(browseType='series')
        self.closeButton = QPushButton()
        self.closeButton.setText('Load Series')
    def loadFunctions(self):
        self.closeButton.clicked.connect( self.loadClose )
    def loadLayout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.series1)
        vbox.addWidget(self.series2)
        vbox.addWidget(self.closeButton)
        self.setLayout(vbox)
    def loadClose(self):
        # Add paths to self.output
        self.output = ( str(self.series1.path.text()), str(self.series2.path.text()) )
        self.close()

if __name__ == '__main__':
    app = QApplication.instance()
    if app == None:
        app = QApplication([])
    a = pyreconMainWindow()
    app.exec_()