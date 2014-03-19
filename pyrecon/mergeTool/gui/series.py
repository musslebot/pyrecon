from PySide.QtCore import *
from PySide.QtGui import *

# - Attributes #=== low priority, return A's for now
class seriesAttributes(QDialog):
	def __init__(self, dictA, dictB):
		QDialog.__init__(self)
		self.setWindowTitle('Series Attributes')
		box = QVBoxLayout()
		self.lab = QLabel('This is a placeholder until complete. Attributes from series1 are kept for now. x out of window') #===
		self.closeBut = QPushButton(self)
		self.closeBut.setText('Close and continue')
		self.closeBut.clicked.connect( self.close )
		box.addWidget(self.lab)
		box.addWidget(self.closeBut)
		self.setLayout(box)
		self.output = {}
		for key in dictA:
			if key not in ['zcontours','contours', 'sections']: # ignore zcontours, contours, sections -- they have their own merge functions
				self.output[key] = dictA[key]
		self.exec_()
# - Contours #=== low priority, return A's for now
class seriesContours(QDialog):
	def __init__(self, contsA, contsB):
		QDialog.__init__(self)
		self.setWindowTitle('Series Contours')
		box = QVBoxLayout()
		self.lab = QLabel('This is a placeholder until complete. Contours from series1 are kept for now. x out of window') #===
		self.closeBut = QPushButton(self)
		self.closeBut.setText('Close and continue')
		self.closeBut.clicked.connect( self.close )
		box.addWidget(self.lab)
		box.addWidget(self.closeBut)
		self.setLayout(box)
		self.output = contsA #===
		self.exec_()
# - ZContours #=== HIGH PRIORITY, add uniques from zConts1,zConts2 to merged
class seriesZContours(QDialog):
	def __init__(self, zConts1, zConts2, mergedZConts):
		QDialog.__init__(self)
		self.setWindowTitle('Series ZContours')
		box = QVBoxLayout()
		self.lab = QLabel('This is a placeholder until complete. ZContours from both series are kept for now. x out of window') #===
		self.closeBut = QPushButton(self )
		self.closeBut.setText('Close and continue')
		self.closeBut.clicked.connect( self.close )
		box.addWidget(self.lab)
		box.addWidget(self.closeBut)
		self.setLayout(box)
		# add leftover, unique zcontours to ser3zconts
		mergedZConts.extend(zConts1)
		mergedZConts.extend(zConts2)
		self.output = mergedZConts
		self.exec_()