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
        self.unresolvedView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.unresolvedView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.unresolvedView.customContextMenuRequested.connect(MainWindow.unresolvedMenu)

        self.unresolvedView.setObjectName("unresolvedView")
        self.verticalLayout_2.addWidget(self.unresolvedView)
        self.resolveButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.resolveButton.setObjectName("resolveButton")
        self.verticalLayout_2.addWidget(self.resolveButton)        
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
        self.resolvedView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

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
        self.resolveButton.setText(_translate("MainWindow", "Resolve Selected")) 
        self.transferLeftButton.setText(_translate("MainWindow", "Transfer >>"))
        self.viewAllButton.setText(_translate("MainWindow", "Resolve All"))
        self.transferAllButton.setText(_translate("MainWindow", "Transfer All"))
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

            if len(self.data[i]["potential_realigned"]) > 0:
                for j in range (len(self.data[i]["potential_realigned"])):
                    unresolvedItem = QtGui.QStandardItem(self.data[i]["potential"][j][0]["name"])
                    data = self.data[i]["potential"][j]
                    unresolvedItem.setData(data)
                    unresolvedItem.setText(str(self.data[i]["section"])+"."+str(self.data[i]["potential"][j][0]["name"]))
                    self.ui.unresolvedModel.appendRow(unresolvedItem)
                    unresolvedItem.setBackground(QtGui.QColor('orange'))


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
                    resolvedItem = QtGui.QStandardItem(self.data[i]["unique"][j][0]["name"])
                    data = self.data[i]["unique"][j]
                    resolvedItem.setData(data)
                    resolvedItem.setText(str(self.data[i]["section"])+"."+str(self.data[i]["unique"][j][0]["name"]))
                    self.ui.resolvedModel.appendRow(resolvedItem)
                    resolvedItem.setBackground(QtGui.QColor('green'))

        self.ui.unresolvedView.doubleClicked.connect(self.loadResolveUnchanged)
        self.ui.resolvedView.doubleClicked.connect(self.loadResolveChanged)
     
        print ("initalizes dataset")

    def loadSeries(self):
        print("load series")

    def transferAllRight(self):
        rowCount = self.ui.unresolvedModel.rowCount()
        for idx in range (0, rowCount):
            indexObj = self.ui.unresolvedModel.index(0, 0)
            selectedItem = self.ui.unresolvedModel.itemFromIndex(indexObj)
            self.ui.unresolvedModel.takeRow(0)
            self.ui.resolvedModel.appendRow(selectedItem)

        self.ui.resolvedView.update()
        self.ui.unresolvedView.update()


    def transferFromLeft(self):
        selected = self.ui.unresolvedView.selectedIndexes()
        rowNumbers = []
        for idx in selected:
            rowNumbers.append(idx.row())

        oldIndex = 0

        rowNumbers = sorted(rowNumbers)

        for i in range (len(rowNumbers)):
            indexObj = self.ui.unresolvedModel.index(rowNumbers[i] - oldIndex, 0)
            selectedItem = self.ui.unresolvedModel.itemFromIndex(indexObj)
            self.ui.unresolvedModel.takeRow(rowNumbers[i] - oldIndex)
            self.ui.resolvedModel.appendRow(selectedItem)
            oldIndex +=1

        self.ui.resolvedView.update()
        self.ui.unresolvedView.update()


    def transferFromRight(self):
        selected = self.ui.resolvedView.selectedIndexes()
        rowNumbers = []
        for idx in selected:
            rowNumbers.append(idx.row())

        oldIndex = 0
        rowNumbers = sorted(rowNumbers)

        for i in range (len(rowNumbers)):
            indexObj = self.ui.resolvedModel.index(rowNumbers[i] - oldIndex, 0)
            selectedItem = self.ui.resolvedModel.itemFromIndex(indexObj)
            self.ui.resolvedModel.takeRow(rowNumbers[i] - oldIndex)
            self.ui.unresolvedModel.appendRow(selectedItem)
            oldIndex +=1

        self.ui.resolvedView.update()
        self.ui.unresolvedView.update()


    def viewAll(self):
        for idx in range (0, self.ui.unresolvedModel.rowCount()):
            nextItemIndex = self.ui.unresolvedModel.index(0, 0)
            nextItem = self.ui.unresolvedModel.itemFromIndex(nextItemIndex)
            resolution = resolveDialog(nextItem)
            resoMarker = resolution.saveState
            
            if resoMarker:
                self.ui.unresolvedModel.takeRow(0)
                self.ui.resolvedModel.appendRow(nextItem)        

        self.ui.resolvedView.update()
        self.ui.unresolvedView.update()            

    def saveSeries(self):
        print ("save series")

    def loadResolveUnchanged(self):
        selected = self.ui.unresolvedView.selectedIndexes()
        for idx in selected:
            selectedItem = self.ui.unresolvedModel.itemFromIndex(idx)        
            resolution = resolveDialog(selectedItem)
            resoMarker = resolution.saveState
        
            if resoMarker:
                self.ui.unresolvedModel.takeRow(idx.row())
                self.ui.resolvedModel.appendRow(selectedItem)        

                self.ui.resolvedView.update()
                self.ui.unresolvedView.update()

    def loadResolveChanged(self):
        selected = self.ui.resolvedView.selectedIndexes()   
        for idx in selected:
            selectedItem = self.ui.resolvedModel.itemFromIndex(idx)           
        resolveDialog(selectedItem)    

    def selectAllLeft(self):
        selected = self.ui.unresolvedView.selectedIndexes()   
        for idx in selected:
            selectedItem = self.ui.unresolvedModel.itemFromIndex(idx)           
            selectedData = selectedItem.data()

            for i in range (0, len(selectedData)):
                if i == 0:
                    selectedData[i]['keepBool'] = True
                else:
                    selectedData[i]['keepBool'] = False

            selectedItem.setData(selectedData)

    def selectAllRight(self):
        selected = self.ui.unresolvedView.selectedIndexes()   
        for idx in selected:
            selectedItem = self.ui.unresolvedModel.itemFromIndex(idx)           
            selectedData = selectedItem.data()

            if len(selectedData) == 1:
                selectedData[i]['keepBool'] = True

            else:
                for i in range (0, len(selectedData)):
                    if i == 1:
                        selectedData[i]['keepBool'] = True
                    else:
                        selectedData[i]['keepBool'] = False

            selectedItem.setData(selectedData)

    def deselectAllTraces(self):
        selected = self.ui.unresolvedView.selectedIndexes()   
        for idx in selected:
            selectedItem = self.ui.unresolvedModel.itemFromIndex(idx)           
            selectedData = selectedItem.data()

            for i in range (0, len(selectedData)):
                    selectedData[i]['keepBool'] = False

            selectedItem.setData(selectedData)        

    def selectAllTraces(self):
        selected = self.ui.unresolvedView.selectedIndexes()   
        for idx in selected:
            selectedItem = self.ui.unresolvedModel.itemFromIndex(idx)           
            selectedData = selectedItem.data()

            for i in range (0, len(selectedData)):
                    selectedData[i]['keepBool'] = True

            selectedItem.setData(selectedData)         

    def unresolvedMenu(self, position):
        menu = QtWidgets.QMenu()

        resolveAction = menu.addAction("Resolve")
        transferAction = menu.addAction("Transfer")
        selectAllLeftAction = menu.addAction("Select All Left")
        selectAllRightAction = menu.addAction("Select All Right")
        deselectAllTracesAction = menu.addAction("Deselect All Traces")
        selectAllTracesAction = menu.addAction("Select All Traces")


        action = menu.exec_(self.ui.unresolvedView.mapToGlobal(position))

        if action == resolveAction:
            self.loadResolveUnchanged()

        elif action == transferAction:
            self.transferFromLeft()

        elif action == selectAllLeftAction:
            response = leftDialog()
            if response.result() == 1:
                self.selectAllLeft()
            else:
                pass

        elif action == selectAllRightAction:
            response = rightDialog()
            if response.result() == 1:
                self.selectAllRight()
            else:
                pass

        elif action == deselectAllTracesAction:
            response = deselectDialog()
            if response.result() == 1:
                self.deselectAllTraces()
            else:
                pass            
    
        elif action == selectAllTracesAction:
            response = selectDialog()
            if response.result() == 1:
                self.selectAllTraces()
            else:
                pass    




class resolveDialog(QtWidgets.QDialog):
    def __init__(self, item):
        super(resolveDialog, self).__init__()
        self.itemData = item.data()        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self, self.itemData)
        self.nameState = False
        self.updatedState = False
        self.saveState = False
        self.initializeData()
        self.exec_()

        if self.updatedState == True:
            item.setData(self.itemData)

    def initializeData(self):
        for i in range (0, len(self.itemData)):
            getattr(self.ui, 'nameEdit'+str(i+1)).setText(self.itemData[i]["name"])

            myBool = QtCore.QFileInfo(self.itemData[0]["image"]).exists()

            if not myBool:
                minx, miny, maxx, maxy = self.itemData[i]['nullpoints']
                pixmap = QtGui.QPixMap(maxx-minx+100, maxy-miny+100)
                pixmap.fill(fillColor=Qt.black)     
        
            else:       
                pixmap = (QtGui.QPixmap(self.itemData[i]["image"]))

            pixmap = pixmap.copy(*(self.itemData[i]['rect']))

            preCropSize = pixmap.size()

            pixmap = pixmap.copy().scaled(300, 300, QtCore.Qt.KeepAspectRatio)

            preWidth = float(preCropSize.width())
            preHeight = float(preCropSize.height())

            if preWidth == 0.0 or preHeight == 0.0:
                preWidth = 1.0
                preHeight = 1.0

            wScale = pixmap.size().width()/preWidth
            hScale = pixmap.size().height()/preHeight

            scale = numpy.array([wScale, hScale])

            scaledPoints = list(map(tuple, numpy.array(self.itemData[i]['croppedPoints'])*scale))
            points = scaledPoints

            polygon = QtGui.QPolygon()
            for point in points:
                polygon.append(QtCore.QPoint(*point))

            painter = QtGui.QPainter()
            painter.begin(pixmap)
            painter.setPen(QtGui.QColor('red'))
            painter.drawConvexPolygon(polygon)   
            painter.end()
            getattr(self.ui, 'pix'+str(i+1)).setPixmap(pixmap)

    def changeName(self):
        self.nameState == True

    def saveResolutions(self,item):
        self.saveState = True
        if self.nameState == True:
            for i in range (0, len(self.itemData)):
                self.itemData[i+1]['name'] = getattr(self.ui, 'nameEdit'+str(i+1)).text()

        if self.updatedState == True:
            for i in range (0, len(self.itemData)):
                if getattr(self.ui, 'checkBox'+str(i+1)).isChecked():
                    self.itemData[i]['keepBool'] = True
                else:
                    self.itemData[i]['keepBool'] = False

    def updateContour(self, item):
        print ("update contour")
        self.updatedState = True


class Ui_Dialog(object):
    def setupUi(self, Dialog, itemData):
        self.itemData = itemData
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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        #generate photos
        for i in range(0, len(self.itemData)):
            setattr(self, 'pix'+str(i+1), QtWidgets.QLabel(self.verticalLayoutWidget))
            getattr(self, 'pix'+str(i+1)).setMaximumSize(QtCore.QSize(300, 300))
            
            getattr(self, 'pix'+str(i+1)).setText("")
            getattr(self, 'pix'+str(i+1)).setScaledContents(True)
            getattr(self, 'pix'+str(i+1)).setWordWrap(False)
            getattr(self, 'pix'+str(i+1)).setObjectName("pix"+str(i+1))
            self.horizontalLayout.addWidget(getattr(self, 'pix'+str(i+1)))
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")





        #generate name label and name edit
        for i in range(0, len(self.itemData)):
            setattr(self, 'verticalLayout_'+str(i+2), QtWidgets.QVBoxLayout())
            getattr(self, 'verticalLayout_'+str(i+2)).setObjectName("verticalLayout_"+str(i+2))
            setattr(self, 'horizontalLayout_'+str(i+2), QtWidgets.QHBoxLayout())
            getattr(self, 'horizontalLayout_'+str(i+2)).setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
            getattr(self, 'horizontalLayout_'+str(i+2)).setObjectName("horizontalLayout_"+str(i+2))  

            setattr(self, 'nameLabel'+str(i+1), QtWidgets.QLabel(self.verticalLayoutWidget))
            getattr(self, 'nameLabel'+str(i+1)).setMaximumSize(QtCore.QSize(50, 16777215))
            
            getattr(self, 'nameLabel'+str(i+1)).setObjectName("nameLabel"+str(i+1))
            getattr(self, 'nameLabel'+str(i+1)).setText("Name:")
            getattr(self, 'horizontalLayout_'+str(i+2)).addWidget(getattr(self, 'nameLabel'+str(i+1)))

            setattr(self, 'nameEdit'+str(i+1), QtWidgets.QLineEdit(self.verticalLayoutWidget))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(getattr(self, 'nameEdit'+str(i+1)).sizePolicy().hasHeightForWidth())
            getattr(self, 'nameEdit'+str(i+1)).setSizePolicy(sizePolicy)
            getattr(self, 'nameEdit'+str(i+1)).setMaximumSize(QtCore.QSize(200, 16777215))
            getattr(self, 'nameEdit'+str(i+1)).setObjectName("nameEdit"+str(i+1))
            getattr(self, 'horizontalLayout_'+str(i+2)).addWidget(getattr(self, 'nameEdit'+str(i+1)))
            getattr(self, 'verticalLayout_'+str(i+2)).addLayout(getattr(self, 'horizontalLayout_'+str(i+2)))
            getattr(self, 'nameEdit'+str(i+1)).textEdited['QString'].connect(Dialog.changeName)

            
            #generate checkboxes
            setattr(self, 'checkBox'+str(i+1), QtWidgets.QCheckBox(self.verticalLayoutWidget))            
            getattr(self, 'checkBox'+str(i+1)).setMaximumSize(QtCore.QSize(16777215, 20))
            getattr(self, 'checkBox'+str(i+1)).setObjectName("checkBox1")
            getattr(self, 'checkBox'+str(i+1)).setChecked(self.itemData[i]['keepBool'])
            getattr(self, 'checkBox'+str(i+1)).stateChanged['int'].connect(Dialog.updateContour)
            getattr(self, 'checkBox'+str(i+1)).setText("Contour "+str(i+1))
            getattr(self, 'verticalLayout_'+str(i+2)).addWidget(getattr(self, 'checkBox'+str(i+1)))

            self.horizontalLayout_1.addLayout(getattr(self, 'verticalLayout_'+str(i+2)))            

        
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.saveChangesButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.saveChangesButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.saveChangesButton.setObjectName("saveChangesButton")
        self.verticalLayout_1.addWidget(self.saveChangesButton)
        self.cancelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancelButton.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cancelButton.setObjectName("cancelButton")
        self.verticalLayout_1.addWidget(self.cancelButton)
        self.horizontalLayout_1.addLayout(self.verticalLayout_1)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Dialog)
 
        self.saveChangesButton.clicked.connect(Dialog.saveResolutions)
        self.cancelButton.clicked.connect(Dialog.reject)
        self.saveChangesButton.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.resolveLabel.setText(_translate("Dialog", "Resolve Duplicate Contours"))
        self.saveChangesButton.setText(_translate("Dialog", "Save"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))

class Ui_LeftDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Select All Left")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select All Left"))
        self.label.setText(_translate("Dialog", "Are you sure you want to select all traces on the left?"))

class leftDialog(QtWidgets.QDialog):
    def __init__(self):
        super(leftDialog, self).__init__()       
        self.ui = Ui_LeftDialog()
        self.ui.setupUi(self)
        self.exec_()

class Ui_RightDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select All Right"))
        self.label.setText(_translate("Dialog", "Are you sure you want to select all traces on the right?"))

class rightDialog(QtWidgets.QDialog):
    def __init__(self):
        super(rightDialog, self).__init__()       
        self.ui = Ui_RightDialog()
        self.ui.setupUi(self)
        self.exec_()

class Ui_DeselectDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select All Right"))
        self.label.setText(_translate("Dialog", "Are you sure you want to deselect all traces?"))

class deselectDialog(QtWidgets.QDialog):
    def __init__(self):
        super(deselectDialog, self).__init__()       
        self.ui = Ui_DeselectDialog()
        self.ui.setupUi(self)
        self.exec_()

class Ui_SelectDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select All Right"))
        self.label.setText(_translate("Dialog", "Are you sure you want to select all traces?"))

class selectDialog(QtWidgets.QDialog):
    def __init__(self):
        super(selectDialog, self).__init__()       
        self.ui = Ui_SelectDialog()
        self.ui.setupUi(self)
        self.exec_()

def main():

    app = QtWidgets.QApplication(sys.argv)
    mockData = json.load(open('CLZBJ_86.json'))
    #initialWindow = loadDialog()
    #series = initialWindow.output
    #print (series)
    mainWindow = MainWindow(mockData)
    mainWindow.show()
    app.exec_()

main()
