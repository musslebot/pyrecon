'''Graphical handler functions for mergeTool conflicts'''
from PySide import QtCore, QtGui
import sys

# SECTIONS
# - Image
def sectionImages(imageA, imageB):
	# app = QtGui.QApplication(sys.argv)
	a = sectionImageResolver(imageA, imageB)
	# sys.exit( app.exec_() ) 
# - Contours
def sectionContours(uniqueA, compOvlp, confOvlp, uniqueB):
	return

class sectionImageResolver(QtGui.QFrame):
	def __init__(self, image1, image2):
		QtGui.QFrame.__init__(self)
		self.loadObjects()
		self.loadFunctions(image1, image2)
		self.loadLayout()
		self.show()

	def loadObjects(self):
		self.image1src = QtGui.QLabel(self) # Image src label
		self.image2src = QtGui.QLabel(self) # "
		self.image1det = QtGui.QLabel(self) # Image details
		self.image2det = QtGui.QLabel(self) # "
		self.pickButton1 = QtGui.QPushButton(self)
		self.pickButton2 = QtGui.QPushButton(self)
	
	def loadFunctions(self, image1, image2):
		self.image1src.setText( image1.src )
		self.image2src.setText( image2.src )
		pic1 = QtGui.QPixmap()
		pic1.load("/home/michaelm/Documents/Test Series/BBCHZ/"+str(image1.src))
		pic2 = QtGui.QPixmap()
		pic2.load("/home/michaelm/Documents/Test Series/BBCHZ/"+str(image2.src))
		self.image1det.setPixmap( pic1 )
		self.image2det.setPixmap( pic2 )
		self.pickButton1.setText( 'Pick 1' )
		self.pickButton2.setText( 'Pick 2' )
	
	def loadLayout(self):
		self.setGeometry(0,0,600,600)
		self.setWindowTitle('Section Image Resolver')
		self.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Plain)
		self.setLineWidth(2)
		self.setMidLineWidth(3)
		# Image 1
		vbox1 = QtGui.QVBoxLayout()
		vbox1.addWidget(self.image1src)
		vbox1.addWidget(self.image1det)
		vbox1.addWidget(self.pickButton1)
		# Image 2
		vbox2 = QtGui.QVBoxLayout()
		vbox2.addWidget(self.image2src)
		vbox2.addWidget(self.image2det)
		vbox2.addWidget(self.pickButton2)
		# Combine
		hbox = QtGui.QHBoxLayout()
		hbox.addLayout(vbox1)
		hbox.addLayout(vbox2)
		self.setLayout(hbox)

