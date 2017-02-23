# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'seriesLoadWidget.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

import sys, os, csv, json, numpy
from skimage import transform as tf
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_loadDialog(object):

    def setupUi(self, loadDialog):
        loadDialog.setObjectName("loadDialog")
        loadDialog.resize(400, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(loadDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.welcomeLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.welcomeLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.welcomeLabel.setObjectName("welcomeLabel")
        self.verticalLayout_3.addWidget(self.welcomeLabel)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.loadLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.loadLineEdit.setObjectName("loadLineEdit")
        self.horizontalLayout_3.addWidget(self.loadLineEdit)
        self.loadSeriesButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.loadSeriesButton.setObjectName("loadSeriesButton")
        self.horizontalLayout_3.addWidget(self.loadSeriesButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cancelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_4.addWidget(self.cancelButton)
        self.selectButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.selectButton.setObjectName("selectButton")
        self.horizontalLayout_4.addWidget(self.selectButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(loadDialog)
        self.loadSeriesButton.clicked.connect(loadDialog.loadSeries)
        self.cancelButton.clicked.connect(loadDialog.reject)
        self.selectButton.clicked.connect(loadDialog.startMainWindow)
        QtCore.QMetaObject.connectSlotsByName(loadDialog)


    def retranslateUi(self, loadDialog):
        _translate = QtCore.QCoreApplication.translate
        loadDialog.setWindowTitle(_translate("loadDialog", "Dialog"))
        self.welcomeLabel.setText(_translate("loadDialog", "Welcome to pyRECONSTRUCT! Please select a series."))
        self.loadSeriesButton.setText(_translate("loadDialog", "Load Series..."))
        self.cancelButton.setText(_translate("loadDialog", "Cancel"))
        self.selectButton.setText(_translate("loadDialog", "Select"))

class loadDialog(QtWidgets.QDialog):
    def __init__(self):
        super(loadDialog, self).__init__()

        self.ui = Ui_loadDialog()
        self.ui.setupUi(self)
        self.exec_()

    def loadSeries(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Series", "/home/", "Series File (*.ser)")
        if fileName != None:
            self.ui.loadLineEdit.setText(str(fileName[0]))
            self.output = str(fileName[0])


    def startMainWindow(self):
        #series = openSeries(self.fileName)
        self.close()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(761, 551)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 371, 501))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.changeSeriesButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.changeSeriesButton.setObjectName("changeSeriesButton")
        self.verticalLayout_2.addWidget(self.changeSeriesButton)
        self.unresolvedLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.unresolvedLabel.setFont(font)
        self.unresolvedLabel.setObjectName("unresolvedLabel")
        self.verticalLayout_2.addWidget(self.unresolvedLabel)

        self.unresolvedView = QtWidgets.QListView(self.gridLayoutWidget)
        self.unresolvedModel = QtGui.QStandardItemModel(self.unresolvedView)
        self.unresolvedView.setModel(self.unresolvedModel)
        self.unresolvedView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.unresolvedView.setObjectName("unresolvedView")
        self.verticalLayout_2.addWidget(self.unresolvedView)
        self.transferLeftButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.transferLeftButton.setObjectName("transferLeftButton")
        self.verticalLayout_2.addWidget(self.transferLeftButton)
        self.viewAllButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.viewAllButton.setObjectName("viewAllButton")
        self.verticalLayout_2.addWidget(self.viewAllButton)
        self.transferAllButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.transferAllButton.setObjectName("transferAllButton")
        self.verticalLayout_2.addWidget(self.transferAllButton)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(390, 0, 371, 501))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.resolvedLabel = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        self.resolvedLabel.setFont(font)
        self.resolvedLabel.setObjectName("resolvedLabel")
        self.verticalLayout.addWidget(self.resolvedLabel)

        self.resolvedView = QtWidgets.QListView(self.gridLayoutWidget_2)
        self.resolvedModel = QtGui.QStandardItemModel(self.resolvedView)
        self.resolvedView.setModel(self.resolvedModel)        
        self.resolvedView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.resolvedView.setObjectName("resolvedView")
        self.verticalLayout.addWidget(self.resolvedView)
        self.transferRightButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.transferRightButton.setObjectName("transferRightButton")
        self.verticalLayout.addWidget(self.transferRightButton)
        self.completeButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.completeButton.setObjectName("completeButton")
        self.verticalLayout.addWidget(self.completeButton)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setNativeMenuBar(False)

        self.menubar.setGeometry(QtCore.QRect(0, 0, 761, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionChange_Series = QtWidgets.QAction(MainWindow)
        self.actionChange_Series.setObjectName("actionChange_Series")
        self.actionSave_Resolutions = QtWidgets.QAction(MainWindow)
        self.actionSave_Resolutions.setObjectName("actionSave_Resolutions")
        self.actionResolve_all_Left = QtWidgets.QAction(MainWindow)
        self.actionResolve_all_Left.setObjectName("actionResolve_all_Left")
        self.actionResolve_all_Right = QtWidgets.QAction(MainWindow)
        self.actionResolve_all_Right.setObjectName("actionResolve_all_Right")
        self.actionTransfer_all = QtWidgets.QAction(MainWindow)
        self.actionTransfer_all.setObjectName("actionTransfer_all")
        self.actionView_All = QtWidgets.QAction(MainWindow)
        self.actionView_All.setObjectName("actionView_All")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionChange_Series)
        self.menuFile.addAction(self.actionSave_Resolutions)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionView_All)
        self.menuEdit.addAction(self.actionTransfer_all)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        self.changeSeriesButton.clicked.connect(MainWindow.loadSeries)
        self.actionChange_Series.triggered.connect(MainWindow.loadSeries)
        self.transferAllButton.clicked.connect(MainWindow.transferAllRight)
        self.transferLeftButton.clicked.connect(MainWindow.transferFromLeft)
        self.transferRightButton.clicked.connect(MainWindow.transferFromRight)
        self.viewAllButton.clicked.connect(MainWindow.viewAll)
        self.completeButton.clicked.connect(MainWindow.saveSeries)
        self.actionSave_Resolutions.triggered.connect(MainWindow.saveSeries)
        self.actionExit.triggered.connect(MainWindow.close)
        self.actionTransfer_all.triggered.connect(MainWindow.transferAllRight)
        self.actionView_All.triggered.connect(MainWindow.viewAll)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.changeSeriesButton.setText(_translate("MainWindow", "Change Series..."))
        self.unresolvedLabel.setText(_translate("MainWindow", "Unresolved Potential Duplicates"))
        self.transferLeftButton.setText(_translate("MainWindow", "Transfer >>"))
        self.viewAllButton.setText(_translate("MainWindow", "View All"))
        self.transferAllButton.setText(_translate("MainWindow", "Transfer All (Ignore)"))
        self.resolvedLabel.setText(_translate("MainWindow", "Resolved Duplicates, Exact Duplicates, and Unique Traces"))
        self.transferRightButton.setText(_translate("MainWindow", "Transfer <<"))
        self.completeButton.setText(_translate("MainWindow", "Resolve Complete"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionChange_Series.setText(_translate("MainWindow", "Change Series..."))
        self.actionSave_Resolutions.setText(_translate("MainWindow", "Save Resolutions"))
        self.actionResolve_all_Left.setText(_translate("MainWindow", "Resolve All (Left)"))
        self.actionResolve_all_Right.setText(_translate("MainWindow", "Resolve All (Right)"))
        self.actionTransfer_all.setText(_translate("MainWindow", "Transfer All"))
        self.actionView_All.setText(_translate("MainWindow", "View All"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data):
        super(MainWindow, self).__init__()

        self.data = data
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initializeDataset()

    def initializeDataset(self):
        for i in range (len(self.data)):
            if len(self.data[i]["potential"]) > 0:
                for j in range (len(self.data[i]["potential"])):
                    unresolvedItem = QtGui.QStandardItem(self.data[i]["potential"][j][0]["name"])
                    data = self.data[i]["potential"][j]
                    unresolvedItem.setData(data)
                    unresolvedItem.setText(str(self.data[i]["section"])+"."+str(self.data[i]["potential"][j][0]["name"]))
                    self.ui.unresolvedModel.appendRow(unresolvedItem)
                    unresolvedItem.setBackground(QtGui.QColor('red'))


            if len(self.data[i]["exact"]) > 0:
                for j in range (len(self.data[i]["exact"])):
                    resolvedItem = QtGui.QStandardItem(self.data[i]["exact"][j][0]["name"])
                    data = self.data[i]["exact"][j]
                    resolvedItem.setData(data)
                    resolvedItem.setText(str(self.data[i]["section"])+"."+str(self.data[i]["exact"][j][0]["name"]))
                    self.ui.resolvedModel.appendRow(resolvedItem)
                    resolvedItem.setBackground(QtGui.QColor('yellow'))

            if len(self.data[i]["unique"]) > 0:        
                for j in range (len(self.data[i]["unique"])):
                    resolvedItem = QtGui.QStandardItem(self.data[i]["unique"][j]["name"])
                    data = self.data[i]["unique"][j]
                    resolvedItem.setData(data)
                    resolvedItem.setText(str(self.data[i]["section"])+"."+str(self.data[i]["unique"][j]["name"]))
                    self.ui.resolvedModel.appendRow(resolvedItem)
                    resolvedItem.setBackground(QtGui.QColor('green'))

        self.ui.unresolvedView.doubleClicked.connect(self.loadResolveUnchanged)
        self.ui.resolvedView.doubleClicked.connect(self.loadResolveChanged)
     
        print ("initalizes dataset")

    def loadSeries(self):
        print("load series")

    def transferAllRight(self):
        initialRowCount = self.ui.unresolvedModel.rowCount()
        for idx in range (0, initialRowCount):
            i = 0
            indexObj = self.ui.unresolvedModel.index(i, 0)
            selectedItem = self.ui.unresolvedModel.itemFromIndex(indexObj)
            self.ui.unresolvedModel.takeRow(i)
            self.ui.resolvedModel.appendRow(selectedItem)

        self.ui.resolvedView.update()
        self.ui.unresolvedView.update()


    def transferFromLeft(self):
        selected = self.ui.unresolvedView.selectedIndexes()
        for idx in selected:
            selectedItem = self.ui.unresolvedModel.itemFromIndex(idx)
            self.ui.unresolvedModel.takeRow(idx.row())
            self.ui.resolvedModel.appendRow(selectedItem)

        self.ui.resolvedView.update()
        self.ui.unresolvedView.update()

    def transferFromRight(self):
        selected = self.ui.resolvedView.selectedIndexes()
        for idx in selected:
            selectedItem = self.ui.resolvedModel.itemFromIndex(idx)
            self.ui.resolvedModel.takeRow(idx.row())
            self.ui.unresolvedModel.appendRow(selectedItem)

        self.ui.resolvedView.update()
        self.ui.unresolvedView.update()


    def viewAll(self):
        print ("view all")

    def saveSeries(self):
        print ("save series")

    def loadResolveUnchanged(self, item):
        selected = self.ui.unresolvedView.selectedIndexes()
        for idx in selected:
            selectedItem = self.ui.unresolvedModel.itemFromIndex(idx)        
        resolveDialog(selectedItem)
        print ("load resolve unchanged")


    def loadResolveChanged(self, item):
        selected = self.ui.resolvedView.selectedIndexes()   
        for idx in selected:
            selectedItem = self.ui.resolvedModel.itemFromIndex(idx)           
        resolution = resolveDialog(selectedItem)        
        print ("load resolve changed")


class resolveDialog(QtWidgets.QDialog):
    def __init__(self, item):
        super(resolveDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.pixmap1 = QtGui.QPixmap()
        self.pixmap2 = QtGui.QPixmap()
        self.item = item

#        for len(item):

        global itemData
        itemData = item.data()
        self.initializeData()
        self.exec_()

    def initializeData(self):
        name1 = itemData[0]["name"]
        name2 = itemData[1]["name"]
        self.ui.nameEdit1.setText(name1)
        self.ui.nameEdit2.setText(name2)
        myBool = QtCore.QFileInfo(itemData[0]["image"]).exists()

        if not myBool:
            minx, miny, maxx, maxy = itemData[0]['nullpoints']
            self.pixmap1 = QtGui.QPixMap(maxx-minx+100, maxy-miny+100)
            self.pixmap1.fill(fillColor=Qt.black)     
        
        else:       
            self.pixmap1 = (QtGui.QPixmap(itemData[0]["image"]))
            self.pixmap2 = (QtGui.QPixmap(itemData[1]["image"]))

        self.pixmap1 = self.pixmap1.copy(*(itemData[0]['rect']))
        self.pixmap2 = self.pixmap2.copy(*(itemData[1]['rect']))

        preCropSize1 = self.pixmap1.size()
        preCropSize2 = self.pixmap2.size()

        self.pixmap1 = self.pixmap1.copy().scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.pixmap2 = self.pixmap2.copy().scaled(300, 300, QtCore.Qt.KeepAspectRatio)

        preWidth = float(preCropSize1.width())
        preHeight = float(preCropSize1.height())

        if preWidth == 0.0 or preHeight == 0.0:
            preWidth = 1.0
            preHeight = 1.0

        wScale = self.pixmap1.size().width()/preWidth
        hScale = self.pixmap1.size().height()/preHeight

        scale = numpy.array([wScale, hScale])

        scaledPoints = list(map(tuple, numpy.array(itemData[0]['croppedPoints'])*scale))
        points = scaledPoints

        polygon = QtGui.QPolygon()
        for point in points:
            polygon.append(QtCore.QPoint(*point))

        painter = QtGui.QPainter()
        painter.begin(self.pixmap1)
        painter.setPen(QtGui.QColor('red'))
        painter.drawConvexPolygon(polygon)   
        self.ui.pix1.setPixmap(self.pixmap1)

    def changeName(self):
        print ("change name")

    def saveResolutions(self):
        print ("save resolutions")

    def updateContour(self):
        print ("update contour")

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(736, 649)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 9, 696, 616))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.resolveLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.resolveLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.resolveLabel.setAutoFillBackground(False)
        self.resolveLabel.setWordWrap(False)
        self.resolveLabel.setObjectName("resolveLabel")
        self.verticalLayout.addWidget(self.resolveLabel)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pix1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.pix1.setMaximumSize(QtCore.QSize(300, 300))
        self.pix1.setText("")
#        self.pix1.setPixmap(QtGui.QPixmap("brain4.png"))
        self.pix1.setScaledContents(True)
        self.pix1.setWordWrap(False)
        self.pix1.setObjectName("pix1")
        self.horizontalLayout_3.addWidget(self.pix1)
        self.pix2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.pix2.setMaximumSize(QtCore.QSize(300, 300))
        self.pix2.setText("")
#        self.pix2.setPixmap(QtGui.QPixmap("brain4.png"))
        self.pix2.setScaledContents(True)
        self.pix2.setWordWrap(False)
        self.pix2.setObjectName("pix2")
        self.horizontalLayout_3.addWidget(self.pix2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.nameLabel1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.nameLabel1.setMaximumSize(QtCore.QSize(50, 16777215))
        self.nameLabel1.setObjectName("nameLabel1")
        self.horizontalLayout.addWidget(self.nameLabel1)
        self.nameEdit1 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameEdit1.sizePolicy().hasHeightForWidth())
        self.nameEdit1.setSizePolicy(sizePolicy)
        self.nameEdit1.setMaximumSize(QtCore.QSize(200, 16777215))
        self.nameEdit1.setObjectName("nameEdit1")
        self.horizontalLayout.addWidget(self.nameEdit1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.checkBox1 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox1.setMaximumSize(QtCore.QSize(16777215, 20))
        self.checkBox1.setObjectName("checkBox1")
        self.verticalLayout_2.addWidget(self.checkBox1)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.nameLabel2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.nameLabel2.setMaximumSize(QtCore.QSize(50, 16777215))
        self.nameLabel2.setObjectName("nameLabel2")
        self.horizontalLayout_2.addWidget(self.nameLabel2)
        self.nameEdit2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameEdit2.sizePolicy().hasHeightForWidth())
        self.nameEdit2.setSizePolicy(sizePolicy)
        self.nameEdit2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.nameEdit2.setObjectName("nameEdit2")
        self.horizontalLayout_2.addWidget(self.nameEdit2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.checkBox2 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.checkBox2.setObjectName("checkBox2")
        self.verticalLayout_4.addWidget(self.checkBox2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.saveChangesButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.saveChangesButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.saveChangesButton.setObjectName("saveChangesButton")
        self.verticalLayout_3.addWidget(self.saveChangesButton)
        self.cancelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancelButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cancelButton.setObjectName("cancelButton")
        self.verticalLayout_3.addWidget(self.cancelButton)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Dialog)
        self.nameEdit1.textChanged['QString'].connect(Dialog.changeName)
        self.nameEdit2.textChanged['QString'].connect(Dialog.changeName)
        self.saveChangesButton.clicked.connect(Dialog.saveResolutions)
        self.cancelButton.clicked.connect(Dialog.reject)
        self.saveChangesButton.clicked.connect(Dialog.accept)
        self.checkBox1.stateChanged['int'].connect(Dialog.updateContour)
        self.checkBox2.stateChanged['int'].connect(Dialog.updateContour)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.resolveLabel.setText(_translate("Dialog", "Resolve Duplicate Contours"))
        self.nameLabel1.setText(_translate("Dialog", "Name:"))
        self.checkBox1.setText(_translate("Dialog", "Contour 1"))
        self.nameLabel2.setText(_translate("Dialog", "Name:"))
        self.checkBox2.setText(_translate("Dialog", "Contour 2"))
        self.saveChangesButton.setText(_translate("Dialog", "Save"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))


def main():

    app = QtWidgets.QApplication(sys.argv)
    mockData = json.load(open('mockdata5.json'))
    initialWindow = loadDialog()
    series = initialWindow.output
    print (series)
    mainWindow = MainWindow(mockData)
    mainWindow.show()
    app.exec_()

main()
