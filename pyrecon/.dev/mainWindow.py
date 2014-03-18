from PySide.QtGui import *
from PySide.QtCore import *

class pyreconMain(QMainWindow):
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
        self.toolsMenu.addAction('curationTool')
        curateAction = QAction( QIcon(), 'curationTool', self )
        curateAction.triggered.connect( self.loadCurate )
        curateAction.setStatusTip( 'Open curation widget' )
        
        # 2) Add actions to toolbars
        self.toolsMenu.addAction( mergeAction )
        self.toolsMenu.addAction( calibAction )
        self.toolsMenu.addAction( excelAction )
        self.toolsMenu.addAction( curateAction )
        
    def loadMerge(self): #=== Why isn't this showing? QLabel is...
        print('Load merge widget')
        m = mergeWidget()
        self.setCentralWidget(m)
    def loadCalib(self): #===
        print('Load calibration widget')
    def loadExcel(self): #===
        print('Load excel widget')
    def loadCurate(self): #===
        print('Load curation widget')
    
class testLabel(QLabel):
    def __init__(self):
        QLabel.__init__(self)
        self.setText('TESTING CENTRAL WIDGET')

class mergeWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Merge Widget')

class sectionScroll(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        return
    def loadFunctions(self):
        return
    def loadLayout(self):
        return

class sectionPropChooser(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)