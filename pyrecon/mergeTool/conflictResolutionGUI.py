'''Graphical handler functions for mergeTool conflicts'''
from PySide.QtCore import *
from PySide.QtGui import *
import sys

# SECTIONS
# - Image
class sectionImages(QWidget):
    def __init__(self, image1, image2):
        QWidget.__init__(self)
        self.loadObjects()
        self.loadFunctions(image1,image2)
        self.loadLayout()
        self.image = None
        self.show()
    def loadObjects(self):
        self.img1label = QLabel(self)
        self.img2label = QLabel(self)
        self.img1detail = QLabel(self)
        self.img2detail = QLabel(self)
        self.pick1 = QPushButton(self)
        self.pick2 = QPushButton(self)
    def loadFunctions(self, image1, image2):
        self.img1 = image1
        self.img2 = image2
        self.img1label.setText('Section A\'s Image\n'+'-'*17)
        self.img1label.setAlignment(Qt.AlignHCenter)
        self.img2label.setText('Section B\'s Image\n'+'-'*17)
        self.img2label.setAlignment(Qt.AlignHCenter)
        self.img1detail.setText('\n'.join([(str(item)+':\t'+str(image1.__dict__[item])) for item in image1.__dict__ if item != 'transform']))
        self.img2detail.setText('\n'.join([(str(item)+':\t'+str(image2.__dict__[item])) for item in image2.__dict__ if item != 'transform']))
        self.pick1.setText('Choose this image')
        self.pick2.setText('Choose this image')
        self.pick1.clicked.connect( self.ret1 ) #===
        self.pick2.clicked.connect( self.ret2 ) #===
    def loadLayout(self):
    	self.setWindowTitle('PyRECONSTRUCT Section Image Resolver')
        hbox = QHBoxLayout()
        # Left image
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.img1label)
        vbox1.addWidget(self.img1detail)
        vbox1.addWidget(self.pick1)
        # Right image
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.img2label)
        vbox2.addWidget(self.img2detail)
        vbox2.addWidget(self.pick2)
        hbox.addLayout(vbox1)
        hbox.addSpacing(50)
        hbox.addLayout(vbox2)
        self.setLayout(hbox)
    def ret1(self): #===
        self.image = self.img1

    def ret2(self): #===
        self.image = self.img2
# - Contours
class sectionContours(QWidget): #===
    def __init__(self, uniqueA, compOvlp, confOvlp, uniqueB):
        QWidget.__init__(self)
# - Attributes
class sectionAttributes(QWidget): #===
    def __init__(self, dictA, dictB):
        QWidget.__init__(self)

# SERIES #===
# - Contours
# - ZContours
# - Attributes