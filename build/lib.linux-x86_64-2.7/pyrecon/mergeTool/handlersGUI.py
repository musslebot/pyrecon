'''Graphical handler functions for mergeTool conflicts'''
from PySide import QtCore, QtGui
import sys

# SECTIONS
# - Image

class contourThread(QtCore.QThread):
	def __init__(self, section1, section2):
		QtCore.QThread.__init__(self)
		self.contResolution = contourFrame(section1, section2)

class imageThread(QtCore.QThread):
	def __init__(self, image1, image2):
		QtCore.QThread.__init__(self)
		self.imgResolution = imageFrame(image1, image2)
		self.image = self.imgResolution.image
		
class imageFrame(QtGui.QFrame):
    def __init__(self, image1, image2):
        QtGui.QFrame.__init__(self)
        self.loadObjects()
        self.loadFunctions(image1,image2)
        self.loadLayout()
        self.image = None
        self.show()
    def loadObjects(self):
        self.img1label = QtGui.QLabel(self)
        self.img2label = QtGui.QLabel(self)
        self.img1detail = QtGui.QLabel(self)
        self.img2detail = QtGui.QLabel(self)
        self.pick1 = QtGui.QPushButton(self)
        self.pick2 = QtGui.QPushButton(self)
    def loadFunctions(self, image1, image2):
        self.img1 = image1
        self.img2 = image2
        self.img1label.setText('Section A\'s Image\n'+'-'*17)
        self.img1label.setAlignment(QtCore.Qt.AlignHCenter)
        self.img2label.setText('Section B\'s Image\n'+'-'*17)
        self.img2label.setAlignment(QtCore.Qt.AlignHCenter)
        self.img1detail.setText('\n'.join([(str(item)+':\t'+str(image1.__dict__[item])) for item in image1.__dict__ if item != 'transform']))
        self.img2detail.setText('\n'.join([(str(item)+':\t'+str(image2.__dict__[item])) for item in image2.__dict__ if item != 'transform']))
        self.pick1.setText('Choose this image')
        self.pick2.setText('Choose this image')
        self.pick1.clicked.connect( self.ret1 ) #===
        self.pick2.clicked.connect( self.ret2 ) #===
    def loadLayout(self):
    	self.setWindowTitle('PyRECONSTRUCT Section Image Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        hbox = QtGui.QHBoxLayout()
        # Left image
        vbox1 = QtGui.QVBoxLayout()
        vbox1.addWidget(self.img1label)
        vbox1.addWidget(self.img1detail)
        vbox1.addWidget(self.pick1)
        # Right image
        vbox2 = QtGui.QVBoxLayout()
        vbox2.addWidget(self.img2label)
        vbox2.addWidget(self.img2detail)
        vbox2.addWidget(self.pick2)
        hbox.addLayout(vbox1)
        hbox.addSpacing(50)
        hbox.addLayout(vbox2)
        self.setLayout(hbox)
    def ret1(self): #===
        self.image = self.img1
        print 'image1: '+str(self.image)
        self.close()
        return self.image #===
    def ret2(self): #===
        self.image = self.img2
        print 'image2: '+str(self.image) #===
        self.close()
        return self.image