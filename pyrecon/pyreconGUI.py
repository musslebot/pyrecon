'''Contains graphical components of PyRECONSTRUCT that are used accross multple tools.'''
from PySide.QtCore import *
from PySide.QtGui import *
import pyrecon

class pyreconMainWindow(QMainWindow):
    '''Main PyRECONSTRUCT window.'''
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setWindowTitle('PyRECONSTRUCT')
        self.loadMenus()
        self.show()
        self.resize(QDesktopWidget().availableGeometry().size())
        self.statusBar().showMessage('Ready! Welcome to PyRECONSTRUCT')
    def loadMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.loadFileMenu()
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.loadToolsMenu()
        self.helpMenu = self.menuBar().addMenu("&Help")
    def loadFileMenu(self):
        saveAction = QAction( QIcon(), 'Save', self)
        saveAction.triggered.connect( self.save )
        saveAction.setStatusTip( 'Save current series' )
        self.fileMenu.addAction( saveAction )
    def loadToolsMenu(self):
        # 1) Create Actions
        
        #===
        # - TEST
        testAction = QAction( QIcon(), 'TEST', self )
        testAction.triggered.connect( self.test )
        testAction.setStatusTip('TEST HERE')
        self.toolsMenu.addAction( testAction )
        #===

        # - mergeTool
        mergeAction = QAction( QIcon(), 'mergeTool', self ) #QIcon() is null, but necessary for Action creation
        mergeAction.triggered.connect( self.loadMergeTool )
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
    def loadMergeTool(self): #===
        from pyrecon.mergeTool.gui.main import mergeSelection
        self.lDock = QDockWidget() # Left dockWidget
        mergeSel = mergeSelection() #=== parent stuff? Whats the deal? i.e. print statements not working in mergeSelection
        self.lDock.setWidget( mergeSel )
        self.addDockWidget( Qt.LeftDockWidgetArea, self.lDock )
        # PlaceHolder for resoution widgets
        self.placeHolder = QLabel()
        self.placeHolder.setPixmap( QPixmap(750,750) )
        self.placeHolder.setAlignment( Qt.AlignCenter )
        self.setCentralWidget( self.placeHolder )
    #===
    def test(self):
        from pyrecon.mergeTool.gui.mergeGUI import testWidget2
        print('Begin Test')
        lDock = QDockWidget() # Widget on same page as mainWindow
        rDock = QDockWidget() # Widget in mergeTool/gui/mergeGUI
        lDock.setWidget( testWidget() )
        rDock.setWidget( testWidget2() )
        self.addDockWidget( Qt.LeftDockWidgetArea, lDock)
        self.addDockWidget( Qt.RightDockWidgetArea, rDock)
    #===
    def loadCalib(self): #===
        print('Load calibration widget')
    def loadExcel(self): #===
        print('Load excel widget')
    def loadCurate(self): #===
        print('Load curation widget')
    def save(self): #===
        print('THIS WILL SAVE YOUR SERIES (in the future :D)')

#===
class testWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.b1 = QPushButton()
        self.b2 = QPushButton()
        self.b3 = QPushButton()
    def loadFunctions(self):
        self.b1.setText('One')
        self.b2.setText('Two')
        self.b3.setText('Three')
        for but in [self.b1, self.b2, self.b3]:
            but.clicked.connect( self.butClick )
    def loadLayout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.b1)
        vbox.addWidget(self.b2)
        vbox.addWidget(self.b3)
        self.setLayout(vbox)
    def butClick(self):
        if self.sender() == self.b1:
            print('BUTTON 1')
        elif self.sender() == self.b2:
            print('BUTTON 2')
        elif self.sender() == self.b3:
            print('BUTTON 3')
#===

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

if __name__ == '__main__':
    app = QApplication.instance()
    if app == None:
        app = QApplication([])
    a = pyreconMainWindow()
    app.exec_()