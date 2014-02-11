import sys
from PySide.QtGui import *
from PySide.QtCore import *
import pyrecon
from pyrecon.mergeTool import handlersGUI as gui

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		self.toWrite = None

		self.handleBut = QPushButton('Handle Conflicts', self)
		self.handleBut.clicked.connect(self.handle)
		self.writeBut = QPushButton('Close (& Write)', self)
		self.writeBut.clicked.connect(self.write)

		self.centralWidget = QWidget(self)
		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.handleBut)
		self.vbox.addWidget(self.writeBut)
		self.setCentralWidget( self.centralWidget )
		self.centralWidget.setLayout(self.vbox)

	def handle(self):
		self.thread = myThread()
	def write(self):
		print('Writing: '+str(self.toWrite))

class myThread(QThread):
	def __init__(self):
		s1 = pyrecon.openSeries('/home/michaelm/Documents/Test Series/Tool Tests/merge/ser1')
		s2 = pyrecon.openSeries('/home/michaelm/Documents/Test Series/Tool Tests/merge/ser2')
		i1 = s1.sections[5].image
		i2 = s2.sections[5].image
		self.handler = gui.imageFrame(i1,i2)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())