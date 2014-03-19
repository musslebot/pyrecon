'''Contains graphical components of PyRECONSTRUCT that are used accross multple tools.'''
from PySide.QtCore import *
from PySide.QtGui import *

class pyreconMainWindow(QMainWindow):
    '''Main PyRECONSTRUCT window.'''
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setWindowTitle('PyRECONSTRUCT')
        self.loadMenus()
        self.show()
        self.statusBar().showMessage('Ready')
    def loadMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.loadToolsMenu()
        self.helpMenu = self.menuBar().addMenu("&Help")
        
    def loadToolsMenu(self):
        # 1) Create Actions
        # - mergeTool
        mergeAction = QAction( QIcon(), 'mergeTool', self ) #QIcon() is null, but necessary for Action creation
        mergeAction.triggered.connect( self.loadMerge )
        mergeAction.setStatusTip( 'Open merge widget' )
        # - calibrationTool
        calibAction = QAction( QIcon(), 'calibrationTool', self )
        calibAction.triggered.connect( self.loadCalib )
        calibAction.setStatusTip( 'Open calibration widget' )
        # - excelTool
        excelAction = QAction( QIcon(), 'excelTool', self )
        excelAction.triggered.connect( self.loadExcel )
        excelAction.setStatusTip( 'Open excel widget' )
        # - curationTool
        curateAction = QAction( QIcon(), 'curationTool', self )
        curateAction.triggered.connect( self.loadCurate )
        curateAction.setStatusTip( 'Open curation widget' )
        
        # 2) Add actions to toolbars
        self.toolsMenu.addAction( mergeAction )
        self.toolsMenu.addAction( calibAction )
        self.toolsMenu.addAction( excelAction )
        self.toolsMenu.addAction( curateAction )
        
    def loadMerge(self):
        from pyrecon.mergeTool.mergeToolGUI import mergeSelection, saveComplete
        lDock = QDockWidget() # Left dockWidget
        m = mergeSelection()
        lDock.setWidget(m)
        rDock = QDockWidget() # Right dockWidget
        s = saveComplete()
        rDock.setWidget(s)
        self.addDockWidget( Qt.LeftDockWidgetArea, lDock )
        self.addDockWidget( Qt.BottomDockWidgetArea, rDock )
        self.setCentralWidget( )
    def loadCalib(self): #===
        print('Load calibration widget')
    def loadExcel(self): #===
        print('Load excel widget')
    def loadCurate(self): #===
        print('Load curation widget')

class directoryBrowse(QWidget):
    '''Provides a QLineEdit and button for browsing for directory paths'''
    def __init__(self, title='Enter directory or browse'):
        QWidget.__init__(self)
        self.loadObjects(title)
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self, title):
        self.path = QLineEdit()
        self.path.setText(title)
        self.browseButton = QPushButton()
        self.browseButton.setText('Browse')
    def loadFunctions(self):
        self.browseButton.clicked.connect( self.browseDir )
    def loadLayout(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.path)
        hbox.addWidget(self.browseButton)
        self.setLayout(hbox)
    def browseDir(self):
        dirName = QFileDialog.getExistingDirectory(self)
        self.path.setText( str(dirName) )


if __name__ == '__main__':
    app = QApplication.instance()
    if app == None:
        app = QApplication([])
    a = pyreconMainWindow()
    app.exec_()