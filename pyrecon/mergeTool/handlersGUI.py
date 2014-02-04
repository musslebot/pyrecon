'''Graphical handler functions for mergeTool conflicts'''
from PySide import QtCore, QtGui
import sys

app = QtGui.QApplication(sys.argv)
sys.exit( app.exec_() ) 

# SECTIONS
# - Image
def sectionImages(imageA, imageB):
	a = sectionImageResolver(imageA, imageB)
	return
# - Contours
def sectionContours(uniqueA, compOvlp, confOvlp, uniqueB):
	return

class sectionImageResolver(QtGui.QFrame):
    def __init__(self, image1, image2):
        QtGui.QFrame.__init__(self)
        self.setWindowTitle('PyRECONSTRUCT Section Image Resolver')
        self.setFrameStyle(QtGui.QFrame.Box|QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        self.loadObjects()
        self.loadFunctions(image1,image2)
        self.loadLayout()
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
#         self.img1detail.setText('\n'.join([(str(item)+':\t'+str(image1.__dict__[item])) for item in image1.__dict__ if item != 'transform']))
#         self.img2detail.setText('\n'.join([(str(item)+':\t'+str(image2.__dict__[item])) for item in image2.__dict__ if item != 'transform']))
        self.img1detail.setText('placeholder') #===
        self.img2detail.settext('placeholder') #===
        self.pick1.setText('Choose this image')
        self.pick2.setText('Choose this image')
    def loadLayout(self):
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