# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'seriesLoadWidget.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

import json
import numpy
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PyQt5 import QtCore, QtGui, QtWidgets

from pyrecon.tools.reconstruct_reader import process_series_directory
from pyrecon.tools.reconstruct_writer import write_series
from pyrecon.tools.mergetool import backend


DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite://")
ENGINE = create_engine(DATABASE_URI, echo=False)
SESSION = sessionmaker(bind=ENGINE)()


def start_database(series_path_list, app):
    splash_pix = QtGui.QPixmap('loading2.gif')
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    progressBar = QtWidgets.QProgressBar(splash)
    progressBar.setMinimum(0)
    splash.setMask(splash_pix.mask())
    splash.show()

    i = 0
    progressBar.setValue(i)

    if bool(os.getenv("CREATE_DB",  1)):
        backend.create_database(ENGINE)

    # Load series from series_path_list
    print (series_path_list)
    series_list = []
    for series_path in series_path_list:
        series_path = series_path if os.path.isdir(series_path) \
                      else os.path.dirname(series_path)
        series_list.append(process_series_directory(series_path))

    # Assign "Main" Series (one with ideal alignment)
    main_series_path = series_path_list[0] if os.path.isdir(series_path_list[0]) \
                       else os.path.dirname(series_path_list[0])

    progressBar.setMaximum(len((series_list[0]).sections) + 6)
    i = 1
    progressBar.setValue(i)
    app.processEvents()

    # Load each Series' contours into the database
    section_indices = set()
    for series in series_list:
        section_indices.update(series.sections.keys())

    for series_number, series in enumerate(series_list):
        for section_index in section_indices:
            section = series.sections.get(section_index)
            if section:
                # Load Section contours into database and determine matches
                backend.load_db_contours_from_pyrecon_section(SESSION, section, series_number)

    i = 2
    progressBar.setValue(i)
    app.processEvents()

    # Find matches

    for section_index in section_indices:

        i = 2 + (section_index)
        progressBar.setValue(i)
        app.processEvents()

        db_contours = backend.query_all_contours_in_section(SESSION, section_index).all()
        backend.load_db_contourmatches_from_db_contours_and_pyrecon_series_list(
            SESSION,
            db_contours,
            series_list
        )

    i += 1
    progressBar.setValue(i)
    app.processEvents()

    backend.cleanup_redundant_matches(SESSION)

    i += 1
    progressBar.setValue(i)
    app.processEvents()

    # Generate payload for frontend
    series_matches = backend.prepare_frontend_payload(SESSION, series_list)

    i += 1
    progressBar.setValue(i)
    app.processEvents()

    json_fp = os.path.join(main_series_path, "merged")
    if not os.path.exists(json_fp):
        os.makedirs(json_fp)
    json_fp = json_fp + "/mergetool.json"
    with open(json_fp, "w") as f:
        json.dump(series_matches, f)

    i += 1
    progressBar.setValue(i)
    app.processEvents()

    splash.close()
    return series_matches


def write_merged_series(series_dict):
    to_keep = backend.get_output_contours_from_series_dict(SESSION, series_dict["sections"])

    series_path_list = []
    for path in series_dict["series"]:
        path = path if os.path.isdir(path) else os.path.dirname(path)
        series_path_list.append(path)

    new_series = backend.create_output_series(SESSION, to_keep, series_path_list)
    merged_fp = series_path_list[0] + "/merged/"
    write_series(new_series, merged_fp, sections=True, overwrite=False)
    return True


def write_realigned_log(series_dict):
    potential_realigned = []
    for _, section in series_dict["sections"].items():
        for group in section["potential_realigned"]:
            for contour in group:
                if contour["keepBool"]:
                    realigned_kept = "{}.{}".format(
                        contour["section"],
                        contour["name"]
                    )
                    potential_realigned.append(realigned_kept)

    if potential_realigned:
        path = series_dict["series"][0]
        path = path if os.path.isdir(path) else os.path.dirname(path)
        realigned_log = path + "/merged/realigned.log"
        with open(realigned_log, "w") as f:
            f.write("\n".join(realigned_log))


class Ui_RestoreDialog(object):
    def setupUi(self, RestoreDialog):
        RestoreDialog.setObjectName("RestoreDialog")
        RestoreDialog.resize(406, 330)
        self.verticalLayoutWidget = QtWidgets.QWidget(RestoreDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 381, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.welcomeLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.welcomeLabel.setScaledContents(False)
        self.welcomeLabel.setWordWrap(True)
        self.welcomeLabel.setObjectName("welcomeLabel")
        self.verticalLayout.addWidget(self.welcomeLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RestoreDialog)

        #restoring from json
        self.buttonBox.accepted.connect(RestoreDialog.yesClicked)

        #not restoring from json
        self.buttonBox.rejected.connect(RestoreDialog.noClicked)
        QtCore.QMetaObject.connectSlotsByName(RestoreDialog)

    def retranslateUi(self, RestoreDialog):
        _translate = QtCore.QCoreApplication.translate
        RestoreDialog.setWindowTitle(_translate("RestoreDialog", "pyRECONSTRUCT"))
        self.welcomeLabel.setText(_translate("RestoreDialog", "Welcome to pyRECONSTRUCT! Are you restoring from a previous merge tool session?"))


class RestoreDialog(QtWidgets.QDialog):
    def __init__(self):
        super(RestoreDialog, self).__init__()

        self.ui = Ui_RestoreDialog()
        self.ui.setupUi(self)
        self.reload = False
        self.restoreBool = True
        self.fileList = []
        self.jsonFile = None
        self.exec_()

    def yesClicked(self):
        """ Restoring from a previous session.
        """
        print("yesClicked")
        self.ui.selectSessionLabel = QtWidgets.QLabel(self.ui.verticalLayoutWidget)
        self.ui.selectSessionLabel.setObjectName("selectSessionLabel")
        self.ui.verticalLayout.addWidget(self.ui.selectSessionLabel)
        self.ui.horizontalLayout = QtWidgets.QHBoxLayout()
        self.ui.horizontalLayout.setObjectName("horizontalLayout")
        self.ui.lineEdit = QtWidgets.QLineEdit(self.ui.verticalLayoutWidget)
        self.ui.lineEdit.setObjectName("lineEdit")
        self.ui.lineEdit.setReadOnly(True)
        self.ui.horizontalLayout.addWidget(self.ui.lineEdit)
        self.ui.browseButton = QtWidgets.QPushButton(self.ui.verticalLayoutWidget)
        self.ui.browseButton.setObjectName("browseButton")
        self.ui.browseButton.clicked.connect(self.loadJson)
        self.ui.horizontalLayout.addWidget(self.ui.browseButton)
        self.ui.verticalLayout.addLayout(self.ui.horizontalLayout)

        #load or cancel the .json file
        self.ui.buttonBox_2 = QtWidgets.QDialogButtonBox(self.ui.verticalLayoutWidget)
        self.ui.buttonBox_2.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.ui.buttonBox_2.setObjectName("buttonBox_2")
        self.ui.verticalLayout.addWidget(self.ui.buttonBox_2)

        #load the json file
        self.ui.buttonBox_2.accepted.connect(self.close)

        #cancel the .json load: just reload restore dialog
        self.ui.buttonBox_2.rejected.connect(self.cancelClicked)
        self.ui.buttonBox_2.rejected.connect(self.close)
        self.ui.selectSessionLabel.setText(
            "Please select the session file you would like to import.")
        self.ui.browseButton.setText("Browse...")
        #clicking yes starts the Main Window with the given dictionary

    def noClicked(self):
        """ Not restoring from a previous session.
        """
        self.restoreBool = False
        self.close()

    def loadJson(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Series", "/home/", "Json File (*.json)")
        self.ui.lineEdit.setText(str(fileName[0]))
        self.jsonFile = fileName[0]
        self.fileList = [fileName[0]]
        print("self.jsonFile: {}".format(self.jsonFile))

    def returnFileList(self):
        return self.fileList

    def cancelClicked(self):
        self.close()


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
        self.loadLineEdit.setReadOnly(True)
        self.horizontalLayout_3.addWidget(self.loadLineEdit)
        self.loadSeriesButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.loadSeriesButton.setObjectName("loadSeriesButton")
        self.horizontalLayout_3.addWidget(self.loadSeriesButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.addSeriesButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addSeriesButton.setObjectName("addSeriesButton")
        self.gridLayout.addWidget(self.addSeriesButton, 1, 0, 1, 1)
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
        self.cancelButton.clicked.connect(loadDialog.close)
        self.selectButton.clicked.connect(loadDialog.startMainWindow)
        self.addSeriesButton.clicked.connect(loadDialog.addSeries)
        QtCore.QMetaObject.connectSlotsByName(loadDialog)


    def retranslateUi(self, loadDialog):
        _translate = QtCore.QCoreApplication.translate
        loadDialog.setWindowTitle(_translate("loadDialog", "Dialog"))
        self.welcomeLabel.setText(_translate(
            "loadDialog", "Welcome to pyRECONSTRUCT! Please select a series."))
        self.addSeriesButton.setText(_translate("loadDialog", "Add Series..."))
        self.loadSeriesButton.setText(_translate("loadDialog", "Load Series..."))
        self.cancelButton.setText(_translate("loadDialog", "Cancel"))
        self.selectButton.setText(_translate("loadDialog", "Import Series"))


class loadJsonSeriesDialog(QtWidgets.QDialog):
    def __init__(self, jsonFile):
        super(loadJsonSeriesDialog, self).__init__()

        self.jsonFile = jsonFile
        self.ui = Ui_loadJsonSeriesDialog()
        self.ui.setupUi(self)
        self.counter = 5
        self.fileList = []
        json_data = json.load(open(self.jsonFile))
        for i, path in enumerate(json_data["series"]):
            if i == 0:
                path_input = getattr(self.ui, 'loadLineEdit')
            else:
                self.addSeries()
                path_input = getattr(self.ui, 'loadLineEdit_{}'.format(self.counter))
            path_input.setText(path)
        self.exec_()

    def loadSeries(self):
        # NOTE: for some reason this is never being called
        print("loadSeries: {}".format(self))
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Series", "/home/", "Series File (*.ser)")
        if fileName != None:
            if (self.sender().objectName() == 'loadSeriesButton'):
                self.ui.loadLineEdit.setText(str(fileName[0]))
            else:
                number = (self.sender().objectName())[-1]
                getattr(self.ui, 'loadLineEdit_'+str(self.counter)).setText(str(fileName[0]))

        self.fileList.append(str(fileName[0]))

    def addSeries(self):
        self.counter += 1

        setattr(self.ui, 'horizontalLayout_'+str(self.counter), QtWidgets.QHBoxLayout())
        setattr(self.ui, 'loadLineEdit_'+str(self.counter), QtWidgets.QLineEdit(self.ui.verticalLayoutWidget))
        getattr(self.ui, 'loadLineEdit_'+str(self.counter)).setReadOnly(True)
        getattr(self.ui, 'horizontalLayout_'+str(self.counter)).addWidget(getattr(self.ui, 'loadLineEdit_'+str(self.counter)))
        setattr(self.ui, 'loadSeriesButton'+str(self.counter),QtWidgets.QPushButton(self.ui.verticalLayoutWidget))
        getattr(self.ui, 'horizontalLayout_'+str(self.counter)).addWidget(getattr(self.ui, 'loadSeriesButton'+str(self.counter)))
        getattr(self.ui, 'loadSeriesButton'+str(self.counter)).setText("Load Series...")
        getattr(self.ui, 'loadSeriesButton'+str(self.counter)).setObjectName('loadSeriesButton'+str(self.counter))
        getattr(self.ui, 'loadSeriesButton'+str(self.counter)).clicked.connect(self.loadSeries)

        self.ui.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 281+(30*(self.counter - 5))))
        self.resize(400, 300 + (30*(self.counter - 5)))

        self.ui.verticalLayout_3.addLayout(getattr(self.ui, 'horizontalLayout_'+str(self.counter)))

    def startMainWindow(self):
        if (len(self.fileList) > 1):
            alignSelection = MultipleSeriesDialog(self.fileList)

            if (alignSelection.result() == 0):
                pass
            elif (alignSelection.result() == 1):
                newFileList = alignSelection.returnFileList()
                self.fileList = newFileList
        self.close()


class Ui_loadJsonSeriesDialog(object):

    def setupUi(self, loadJsonSeriesDialog):
        loadJsonSeriesDialog.setObjectName("loadJsonSeriesDialog")
        loadJsonSeriesDialog.resize(400, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(loadJsonSeriesDialog)
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
        self.loadLineEdit.setReadOnly(True)
        self.horizontalLayout_3.addWidget(self.loadLineEdit)
        self.loadSeriesButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.loadSeriesButton.setObjectName("loadSeriesButton")
        self.horizontalLayout_3.addWidget(self.loadSeriesButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.addSeriesButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addSeriesButton.setObjectName("addSeriesButton")
        self.gridLayout.addWidget(self.addSeriesButton, 1, 0, 1, 1)
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

        self.retranslateUi(loadJsonSeriesDialog)
        self.loadSeriesButton.clicked.connect(loadJsonSeriesDialog.loadSeries)
        self.cancelButton.clicked.connect(loadJsonSeriesDialog.close)
        self.selectButton.clicked.connect(loadJsonSeriesDialog.startMainWindow)
        self.addSeriesButton.clicked.connect(loadJsonSeriesDialog.addSeries)
        QtCore.QMetaObject.connectSlotsByName(loadJsonSeriesDialog)

    def retranslateUi(self, loadJsonSeriesDialog):
        _translate = QtCore.QCoreApplication.translate
        loadJsonSeriesDialog.setWindowTitle(_translate("loadJsonSeriesDialog", "Dialog"))
        self.welcomeLabel.setText(_translate(
            "loadJsonSeriesDialog",
            ("Please locate the series used in this .json file. "
            "Import the series in the same order used originally.")
        ))
        self.addSeriesButton.setText(_translate("loadJsonSeriesDialog", "Add Series..."))
        self.loadSeriesButton.setText(_translate("loadJsonSeriesDialog", "Load Series..."))
        self.cancelButton.setText(_translate("loadJsonSeriesDialog", "Cancel"))
        self.selectButton.setText(_translate("loadJsonSeriesDialog", "Import Series"))


class loadDialog(QtWidgets.QDialog):
    def __init__(self):
        super(loadDialog, self).__init__()

        self.ui = Ui_loadDialog()
        self.ui.setupUi(self)
        self.counter = 5
        self.fileList = []
        self.exec_()

    def loadSeries(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Series", "/home/",
                                                         "Series File (*.ser)")
        if fileName != None:
            if (self.sender().objectName() == 'loadSeriesButton'):
                self.ui.loadLineEdit.setText(str(fileName[0]))
            else:
                number = (self.sender().objectName())[-1]
                getattr(self.ui, 'loadLineEdit_'+str(self.counter)).setText(str(fileName[0]))

        self.fileList.append(str(fileName[0]))

    def addSeries(self):
        self.counter += 1

        setattr(self.ui, 'horizontalLayout_'+str(self.counter), QtWidgets.QHBoxLayout())
        setattr(self.ui, 'loadLineEdit_'+str(self.counter), QtWidgets.QLineEdit(self.ui.verticalLayoutWidget))
        getattr(self.ui, 'loadLineEdit_'+str(self.counter)).setReadOnly(True)
        getattr(self.ui, 'horizontalLayout_'+str(self.counter)).addWidget(getattr(self.ui, 'loadLineEdit_'+str(self.counter)))
        setattr(self.ui, 'loadSeriesButton'+str(self.counter),QtWidgets.QPushButton(self.ui.verticalLayoutWidget))
        getattr(self.ui, 'horizontalLayout_'+str(self.counter)).addWidget(getattr(self.ui, 'loadSeriesButton'+str(self.counter)))
        getattr(self.ui, 'loadSeriesButton'+str(self.counter)).setText("Load Series...")
        getattr(self.ui, 'loadSeriesButton'+str(self.counter)).setObjectName('loadSeriesButton'+str(self.counter))
        getattr(self.ui, 'loadSeriesButton'+str(self.counter)).clicked.connect(self.loadSeries)

        self.ui.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 281+(30*(self.counter - 5))))
        self.resize(400, 300 + (30*(self.counter - 5)))

        self.ui.verticalLayout_3.addLayout(getattr(self.ui, 'horizontalLayout_'+str(self.counter)))

    def startMainWindow(self):
        if (len(self.fileList) > 1):
            alignSelection = MultipleSeriesDialog(self.fileList)

            if (alignSelection.result() == 0):
                pass
            elif (alignSelection.result() == 1):
                self.fileList = alignSelection.returnFileList()
        self.close()


class Ui_MultipleSeriesDialog(object):
    def setupUi(self, MultipleSeriesDialog, fileList):
        MultipleSeriesDialog = MultipleSeriesDialog
        MultipleSeriesDialog.setObjectName("MultipleSeriesDialog")
        MultipleSeriesDialog.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        MultipleSeriesDialog.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtWidgets.QWidget(MultipleSeriesDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 0, 381, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.questionLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.questionLabel.setFont(font)
        self.questionLabel.setWordWrap(True)
        self.questionLabel.setObjectName("questionLabel")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.questionLabel.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.questionLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.noButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.noButton.setObjectName("noButton")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.noButton.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.noButton)
        self.yesButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.yesButton.setObjectName("yesButton")
        self.yesButton.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.yesButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.noButton.clicked.connect(MultipleSeriesDialog.close)
        self.yesButton.clicked.connect(MultipleSeriesDialog.yesClicked)

        self.retranslateUi(MultipleSeriesDialog)
        QtCore.QMetaObject.connectSlotsByName(MultipleSeriesDialog)

    def retranslateUi(self, MultipleSeriesDialog):
        _translate = QtCore.QCoreApplication.translate
        MultipleSeriesDialog.setWindowTitle(_translate("MultipleSeriesDialog", "Dialog"))
        self.questionLabel.setText(_translate("MultipleSeriesDialog", "You have selected multiple series. Do these series have differing alignments or attributes?"))
        self.noButton.setText(_translate("MultipleSeriesDialog", "No"))
        self.yesButton.setText(_translate("MultipleSeriesDialog", "Yes"))


class MultipleSeriesDialog(QtWidgets.QDialog):
    def __init__(self, fileList):
        super(MultipleSeriesDialog, self).__init__()
        #self.setResult(0)
        self.ui = Ui_MultipleSeriesDialog()
        self.ui.setupUi(self, fileList)
        self.fileList = fileList
        self.exec_()

    def yesClicked(self):
        self.setResult(1)
        self.ui.question2Label = QtWidgets.QLabel(self.ui.verticalLayoutWidget)
        self.ui.question2Label.setText("Which series/alignment would you like to output to?")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.ui.question2Label.setSizePolicy(sizePolicy)
        self.ui.question2Label.setObjectName("question2Label")
        self.ui.verticalLayout.addWidget(self.ui.question2Label)

        self.ui.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.ui.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.ui.verticalLayout_5.setObjectName("verticalLayout_5")

        for i in range (len(self.fileList)):
            setattr(self.ui, 'horizontalLayout_'+str(i), QtWidgets.QHBoxLayout())
            setattr(self.ui, 'series'+str(i)+'button', QtWidgets.QRadioButton(self.ui.verticalLayoutWidget))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

            getattr(self.ui, 'series'+str(i)+'button').setSizePolicy(sizePolicy)
            getattr(self.ui, 'series'+str(i)+'button').setMinimumSize(QtCore.QSize(0, 20))
            getattr(self.ui, 'series'+str(i)+'button').setText("")
            getattr(self.ui, 'horizontalLayout_'+str(i)).addWidget(getattr(self.ui, 'series'+str(i)+'button'))
            setattr(self.ui,'lineEdit'+str(i), QtWidgets.QLineEdit(self.ui.verticalLayoutWidget))
            getattr(self.ui,'lineEdit'+str(i)).setReadOnly(True)
            getattr(self.ui, 'horizontalLayout_'+str(i)).addWidget(getattr(self.ui,'lineEdit'+str(i)))
            getattr(self.ui, 'horizontalLayout_'+str(i)).setStretch(1,20)
            self.ui.verticalLayout_5.addWidget(getattr(self.ui, 'series'+str(i)+'button'))
            getattr(self.ui,'lineEdit'+str(i)).setText(str(self.fileList[i]))
            self.ui.verticalLayout_5.addLayout(getattr(self.ui, 'horizontalLayout_'+str(i)))
            self.ui.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 281+(50*(i-1))))
            self.resize(400, 300 + (50*(i - 1)))


        self.ui.verticalLayout.addLayout(self.ui.verticalLayout_5)
        #whatever
        self.ui.buttonBox_2 = QtWidgets.QDialogButtonBox(self.ui.verticalLayoutWidget)
        self.ui.buttonBox_2.setOrientation(QtCore.Qt.Horizontal)
        self.ui.buttonBox_2.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.ui.buttonBox_2.accepted.connect(self.seriesSelected)
        self.ui.buttonBox_2.rejected.connect(self.close)
        self.ui.buttonBox_2.setObjectName("buttonBox_2")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.ui.buttonBox_2.setSizePolicy(sizePolicy)
        self.ui.verticalLayout.addWidget(self.ui.buttonBox_2)

    def seriesSelected(self):
        for i in range (len(self.fileList)):
            if getattr(self.ui, 'series'+str(i)+'button').isChecked():
                self.fileList.insert(0, self.fileList.pop(i))
                self.accept()
                break
            else:
                continue

    def returnFileList(self):
        return self.fileList


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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.saveStatusButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.saveStatusButton.setObjectName("saveStatusButton")
        self.horizontalLayout.addWidget(self.saveStatusButton)
        self.completeButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.completeButton.setObjectName("completeButton")
        self.horizontalLayout.addWidget(self.completeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        self.menuFile.addAction(self.actionSave_Resolutions)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionView_All)
        self.menuEdit.addAction(self.actionTransfer_all)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        self.resolveButton.clicked.connect(MainWindow.loadResolveLeft)
        self.transferAllButton.clicked.connect(MainWindow.transferAllRight)
        self.transferLeftButton.clicked.connect(MainWindow.transferFromLeft)
        self.transferRightButton.clicked.connect(MainWindow.transferFromRight)
        self.viewAllButton.clicked.connect(MainWindow.viewAll)

        #TODO: fix this for complete output
        self.completeButton.clicked.connect(MainWindow.saveSeries)
        self.actionSave_Resolutions.triggered.connect(MainWindow.saveSeries)
        self.saveStatusButton.clicked.connect(MainWindow.saveSeries)
        self.actionExit.triggered.connect(MainWindow.close)
        self.actionTransfer_all.triggered.connect(MainWindow.transferAllRight)
        self.actionView_All.triggered.connect(MainWindow.viewAll)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.unresolvedLabel.setText(_translate("MainWindow", "Unresolved Potential Duplicates"))
        self.resolveButton.setText(_translate("MainWindow", "Resolve Selected"))
        self.transferLeftButton.setText(_translate("MainWindow", "Transfer >>"))
        self.viewAllButton.setText(_translate("MainWindow", "Resolve All"))
        self.transferAllButton.setText(_translate("MainWindow", "Transfer All"))
        self.resolvedLabel.setText(_translate("MainWindow", "Resolved Duplicates, Exact Duplicates, and Unique Traces"))
        self.transferRightButton.setText(_translate("MainWindow", "Transfer <<"))
        self.saveStatusButton.setText(_translate("MainWindow", "Save Current Status"))
        self.completeButton.setText(_translate("MainWindow", "Resolve Complete"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionSave_Resolutions.setText(_translate("MainWindow", "Save Resolutions"))
        self.actionResolve_all_Left.setText(_translate("MainWindow", "Resolve All (Left)"))
        self.actionResolve_all_Right.setText(_translate("MainWindow", "Resolve All (Right)"))
        self.actionTransfer_all.setText(_translate("MainWindow", "Transfer All"))
        self.actionView_All.setText(_translate("MainWindow", "View All"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data, fileList):
        super(MainWindow, self).__init__()
        self.fileList = fileList
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initializeDataset(data)

    def initializeDataset(self, data):
        # Convert string keys to ints
        data = {int(k): v for k,v in data["sections"].items()}
        for section_index, matches in data.items():

            # Potential duplicates
            potential_matches = matches["potential"]
            if len(potential_matches) > 0:
                for j in range (0, len(potential_matches)):
                    potential_data = potential_matches[j]
                    unresolvedItem = QtGui.QStandardItem(potential_matches[j][0]["name"])
                    unresolvedItem.setData(potential_data)
                    unresolvedItem.setText(
                        str(section_index)+"."+str(potential_data[0]["name"]))
                    if potential_data[0].get("side"):
                        if potential_data[0]["side"] == ("L"):
                            self.ui.unresolvedModel.appendRow(unresolvedItem)
                        elif potential_data[0]["side"] == ("R"):
                            self.ui.resolvedModel.appendRow(unresolvedItem)
                    else:
                        self.ui.unresolvedModel.appendRow(unresolvedItem)
                    unresolvedItem.setBackground(QtGui.QColor('red'))

            # Potential realigned duplicates
            pot_realigned_matches = matches["potential_realigned"]
            if len(pot_realigned_matches) > 0:
                for j in range (0, len(pot_realigned_matches)):
                    unresolvedItem = QtGui.QStandardItem(pot_realigned_matches[j][0]["name"])
                    pot_realigned_data = pot_realigned_matches[j]
                    unresolvedItem.setData(pot_realigned_data)
                    unresolvedItem.setText(
                        str(section_index)+"."+str(pot_realigned_data[0]["name"]))
                    if pot_realigned_data[0].get("side"):
                        if pot_realigned_data[0]["side"] == ("L"):
                            self.ui.unresolvedModel.appendRow(unresolvedItem)
                        elif pot_realigned_data[0]["side"] == ("R"):
                            self.ui.resolvedModel.appendRow(unresolvedItem)

                    else:
                        self.ui.unresolvedModel.appendRow(unresolvedItem)
                    unresolvedItem.setBackground(QtGui.QColor('orange'))

            # Exact duplicates
            exact_matches = matches["exact"]
            if len(exact_matches) > 0:
                for j in range(0, len(exact_matches)):
                    resolvedItem = QtGui.QStandardItem(exact_matches[j][0]["name"])
                    exact_data = exact_matches[j]
                    resolvedItem.setData(exact_data)
                    resolvedItem.setText(str(section_index)+"."+str(exact_data[0]["name"]))
                    if exact_data[0].get("side"):
                        if exact_data[0]["side"] == ("L"):
                            self.ui.unresolvedModel.appendRow(resolvedItem)
                        elif exact_data[0]["side"] == ("R"):
                            self.ui.resolvedModel.appendRow(resolvedItem)
                    else:
                        self.ui.resolvedModel.appendRow(resolvedItem)
                    resolvedItem.setBackground(QtGui.QColor('yellow'))

            # Unique contours
            unique_matches = matches["unique"]
            if len(unique_matches) > 0:
                for j in range (0, len(unique_matches)):
                    resolvedItem = QtGui.QStandardItem(unique_matches[j][0]["name"])
                    unique_data = unique_matches[j]
                    resolvedItem.setData(unique_data)
                    resolvedItem.setText(
                        str(section_index)+"."+str(unique_data[0]["name"]))
                    if unique_data[0].get("side"):
                        if unique_data[0]["side"] == ("L"):
                            self.ui.unresolvedModel.appendRow(resolvedItem)
                        elif unique_data[0]["side"] == ("R"):
                            self.ui.resolvedModel.appendRow(resolvedItem)
                    else:
                        self.ui.resolvedModel.appendRow(resolvedItem)
                    resolvedItem.setBackground(QtGui.QColor('green'))

        self.ui.unresolvedView.doubleClicked.connect(self.loadResolveLeft)
        self.ui.resolvedView.doubleClicked.connect(self.loadResolveRight)

    def loadSeries(self):
        print("load series: {}".format(self))

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
            resoMarker = resolution.DialogCode()

            if resoMarker:
                self.ui.unresolvedModel.takeRow(0)
                self.ui.resolvedModel.appendRow(nextItem)

        self.ui.resolvedView.update()
        self.ui.unresolvedView.update()

    def saveSeries(self):
        print ("save series")
        outputDict = {
            "series": self.fileList,
            "sections": {}
        }
        outputDict["sections"]["0"] = {
            "potential_realigned": [],
            "unique": [],
            "potential": [],
            "exact": [],
            "section": 0
        }

        for idx in range (0, self.ui.unresolvedModel.rowCount()):
            nextItemIndex = self.ui.unresolvedModel.index(idx, 0)
            nextItem = self.ui.unresolvedModel.itemFromIndex(nextItemIndex)
            nextItemSection = nextItem.data()[0]["section"]
            nextItemData = nextItem.data()
            nextItemData[0]["side"] = "L"
            nextItem.setData(nextItemData)

            next_section = str(nextItemSection)
            if outputDict["sections"].get(next_section):
                if (nextItem.background().color().name()) == "#ff0000":
                    outputDict["sections"][next_section]["potential"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#ffa500":
                    outputDict["sections"][next_section]["potential_realigned"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#008000":
                    outputDict["sections"][next_section]["unique"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#ffff00":
                    outputDict["sections"][next_section]["exact"].append(
                        nextItem.data())

            else:
                outputDict["sections"][next_section] = {
                    "potential_realigned": [],
                    "unique": [],
                    "potential": [],
                    "exact": [],
                    "section": nextItemSection
                }
                if (nextItem.background().color().name()) == "#ff0000":
                    outputDict["sections"][next_section]["potential_realigned"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#ffa500":
                    outputDict["sections"][next_section]["potential_realigned"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#008000":
                    outputDict["sections"][next_section]["unique"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#ffff00":
                    outputDict["sections"][next_section]["exact"].append(
                        nextItem.data())

        for idx in range (0, self.ui.resolvedModel.rowCount()):
            nextItemIndex = self.ui.resolvedModel.index(idx, 0)
            nextItem = self.ui.resolvedModel.itemFromIndex(nextItemIndex)
            nextItemSection = nextItem.data()[0]["section"]
            nextItemData = nextItem.data()
            nextItemData[0]["side"] = "R"
            nextItem.setData(nextItemData)
            next_section = str(nextItemSection)

            if outputDict["sections"].get(next_section):
                if (nextItem.background().color().name()) == "#ff0000":
                    outputDict["sections"][next_section]["potential"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#ffa500":
                    outputDict["sections"][next_section]["potential_realigned"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#008000":
                    outputDict["sections"][next_section]["unique"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#ffff00":
                    outputDict["sections"][next_section]["exact"].append(
                        nextItem.data())
            else:
                outputDict["sections"][next_section] = {
                    "potential_realigned": [],
                    "unique": [],
                    "potential": [],
                    "exact": [],
                    "section": nextItemSection
                }
                if (nextItem.background().color().name()) == "#ff0000":
                    outputDict["sections"][next_section]["potential_realigned"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#ffa500":
                    outputDict["sections"][next_section]["potential_realigned"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#008000":
                    outputDict["sections"][next_section]["unique"].append(
                        nextItem.data())
                elif (nextItem.background().color().name()) == "#ffff00":
                    outputDict["sections"][next_section]["exact"].append(
                        nextItem.data())

        save_dir = os.path.join(self.fileList[0] if os.path.isdir(self.fileList[0]) \
                   else os.path.dirname(self.fileList[0]), "merged")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        with open(os.path.join(save_dir, "savedstatus.json"), "w") as f:
            json.dump(outputDict, f)

        if (self.sender().objectName() == "completeButton"):
            self.close()
            write_merged_series(outputDict)
            write_realigned_log(outputDict)
            return (outputDict, self.fileList)

    def loadResolveLeft(self):
        selected = self.ui.unresolvedView.selectedIndexes()
        rowNumbers = []
        for idx in selected:
            rowNumbers.append(idx.row())

        oldIndex = 0
        rowNumbers = sorted(rowNumbers)
        for i in range(len(rowNumbers)):
            indexObj = self.ui.unresolvedModel.index(rowNumbers[i] - oldIndex, 0)
            selectedItem = self.ui.unresolvedModel.itemFromIndex(indexObj)
            resolution = resolveDialog(selectedItem)
            if (resolution.result() == 0):
                break
            else:
                self.ui.unresolvedModel.takeRow(rowNumbers[i] - oldIndex)
                self.ui.resolvedModel.appendRow(selectedItem)

                self.ui.resolvedView.update()
                self.ui.unresolvedView.update()
            oldIndex +=1

    def loadResolveRight(self):
        selected = self.ui.resolvedView.selectedIndexes()
        for idx in selected:
            selectedItem = self.ui.resolvedModel.itemFromIndex(idx)
            resolution = resolveDialog(selectedItem)
            if (resolution.result() == 0):
                break

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
            self.loadResolveLeft()
        elif action == transferAction:
            self.transferFromLeft()
        elif action == selectAllLeftAction:
            response = leftDialog()
            if response.result() == 1:
                self.selectAllLeft()
        elif action == selectAllRightAction:
            response = rightDialog()
            if response.result() == 1:
                self.selectAllRight()
        elif action == deselectAllTracesAction:
            response = deselectDialog()
            if response.result() == 1:
                self.deselectAllTraces()
        elif action == selectAllTracesAction:
            response = selectDialog()
            if response.result() == 1:
                self.selectAllTraces()


class resolveDialog(QtWidgets.QDialog):
    def __init__(self, item):
        super(resolveDialog, self).__init__()
        self.itemData = item.data()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self, self.itemData)
        self.nameState = False
        self.updatedState = False
        self.initializeData()
        self.exec_()
        self.show()
        if self.updatedState == True or self.nameState == True:
            item.setData(self.itemData)

    def initializeData(self):
        for i in range (0, len(self.itemData)):
            getattr(self.ui, 'nameEdit'+str(i+1)).setText(self.itemData[i]["name"])
            getattr(self.ui, 'seriesLabel'+str(i)).setText("Series: "+self.itemData[i]["series"])
            getattr(self.ui, 'sectionLabel'+str(i)).setText("Section: "+str(self.itemData[i]["section"]))

            image_exists = QtCore.QFileInfo(self.itemData[0]["image"]).exists()
            if not image_exists:
                minx, miny, maxx, maxy = self.itemData[i]['nullpoints']
                pixmap = QtGui.QPixMap(maxx-minx+100, maxy-miny+100)
                pixmap.fill(fillColor=Qt.black)
            else:
                pixmap = (QtGui.QPixmap(self.itemData[i]["image"]))

            pixmap = pixmap.copy(*(self.itemData[i]['rect']))
            print(self.itemData[i]['rect'])

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
        self.nameState = True

    def updateContour(self, item):
        self.updatedState = True

    def saveResolutions(self,item):
        self.setResult(1)
        if self.nameState == True:
            # Contour was changed
            for i in range (0, len(self.itemData)):
                new_name = getattr(self.ui, 'nameEdit'+str(i+1)).text()
                self.itemData[i]['name'] = new_name
        if self.updatedState == True:
            # Keep checkbox triggered
            for i in range (0, len(self.itemData)):
                is_checked = getattr(self.ui, 'checkBox'+str(i+1)).isChecked()
                if is_checked:
                    self.itemData[i]['keepBool'] = True
                else:
                    self.itemData[i]['keepBool'] = False


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
            setattr(self, 'seriesLabel'+str(i), QtWidgets.QLabel(self.verticalLayoutWidget))
            getattr(self, 'seriesLabel'+str(i)).setObjectName("seriesLabel"+str(i))
            getattr(self, 'seriesLabel'+str(i)).setText("Series:")
            getattr(self, 'verticalLayout_'+str(i+2)).addWidget(getattr(self, 'seriesLabel'+str(i)))
            setattr(self, 'sectionLabel'+str(i), QtWidgets.QLabel(self.verticalLayoutWidget))
            getattr(self, 'sectionLabel'+str(i)).setObjectName("sectionLabel"+str(i))
            getattr(self, 'sectionLabel'+str(i)).setText("Section:")
            getattr(self, 'verticalLayout_'+str(i+2)).addWidget(getattr(self, 'sectionLabel'+str(i)))
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
        self.label.setText(_translate(
            "Dialog", "Are you sure you want to select all traces on the right?"))


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
        self.label.setText(_translate(
            "Dialog", "Are you sure you want to deselect all traces?"))


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
        self.label.setText(_translate(
            "Dialog", "Are you sure you want to select all traces?"))


class selectDialog(QtWidgets.QDialog):
    def __init__(self):
        super(selectDialog, self).__init__()
        self.ui = Ui_SelectDialog()
        self.ui.setupUi(self)
        self.exec_()


def startLoadDialogs():
    app = QtWidgets.QApplication(sys.argv)
    initialWindow = RestoreDialog()
    if (initialWindow.restoreBool == False):
        loadSeries = loadDialog()
        fileList = loadSeries.fileList
        if len(fileList) == 0:
            app.quit()
        else:
            jsonData = start_database(fileList, app)

    elif (len(initialWindow.returnFileList()) > 0):
        jsonFile = initialWindow.jsonFile
        # loadSeries = loadJsonSeriesDialog(jsonFile)
        jsonData = json.load(open(jsonFile))
        # fileList = loadSeries.fileList
        # NOTE: for some reason, not able to retrieve fileList from loadJsonSeriesDialog.
        # Maybe the button is misnamed or something. But for now, we will go directly from
        # the JSON file.
        fileList = jsonData["series"]
        if DATABASE_URI == "sqlite://":
            # Only start_database if it is in memory
            # NOTE: this will need to change if we multiprocess the db loading
            start_database(fileList, app)

    if 'jsonData' in locals():
        mainWindow = MainWindow(jsonData, fileList)
        mainWindow.show()
        app.exec_()
    else:
        app.quit()


def main():
    startLoadDialogs()


main()
