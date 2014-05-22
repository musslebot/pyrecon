'''This file contains the QDialogs used in the gitTool.'''
from PySide.QtCore import *
from PySide.QtGui import *
import subprocess, os
from git import *

class NewBranchDialog(QDialog):
    '''Dialog for creating a new branch.'''
    def __init__(self, repository):
        QDialog.__init__(self)
        self.setWindowTitle('Create New Branch')
        self.repository = repository
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.textLabel1 = QLabel('This will create a new branch named:')
        self.branchName = QLineEdit('<enter new branch name>')
        self.textLabel2 = QLabel('from the current state of the repository:\n'+self.repository.head.commit.hexsha)
        self.acceptBut = QPushButton('Make new branch')
        self.cancelBut = QPushButton('Cancel')
    def loadFunctions(self):
        self.acceptBut.clicked.connect( self.userAccept )
        self.cancelBut.clicked.connect( self.userReject )
    def loadLayout(self):
        info = QVBoxLayout()
        info.addWidget(self.textLabel1)
        info.addWidget(self.branchName)
        info.addWidget(self.textLabel2)
        buttons = QHBoxLayout()
        buttons.addWidget(self.cancelBut)
        buttons.addWidget(self.acceptBut)
        container = QVBoxLayout()
        container.addLayout(info)
        container.addLayout(buttons)
        self.setLayout(container)
    def userAccept(self):
        if subprocess.call(['git', 'check-ref-format', '--branch', str(self.branchName.text())]) != 0:
            msg = QMessageBox()
            msg.setText('The branch name you have entered is invalid. Please try again...')
            msg.setInformativeText('From the documentation, git does NOT allow the following in branch names:\ntwo consecutive dots (..)\nASCII control characters (i.e. bytes whose values are lower than 040, or 177 DEL), space, tilde ~, caret ^, or colon :\nquestion-mark ?, asterisk *, or open bracket [\nbegin or end with a slash / or contain multiple consecutive slashes\nend with a dot .\na sequence @{\na back-slash \\')
            msg.exec_()
        else:
            self.done(1)
    def userReject(self):
        self.done(0)

class DirtyHandler(QDialog): #===
    '''Class for handling a dirty repository. Display modified/untracked files and allow user to handle them via stash or clean.'''
    def __init__(self, repository):
        QDialog.__init__(self)
        self.repository = repository
        # self.remote = Remote(repository, 'origin') #=== for checking ahead/behind maybe
        self.setWindowTitle('Dirty Repository Manager')

        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.info = QTextEdit()# Info about the current dirty state
        self.info.setText( subprocess.check_output( ['git','status'] ) )
        self.saveButton = QPushButton('Save current state')
        self.commitButton = QPushButton('Commit a new version')
        self.forceUpdateButton = QPushButton('Overwrite with most recent version')
        self.forceResetButton = QPushButton('Reset to state before modification')

    def loadFunctions(self):
        # Button function links
        self.saveButton.clicked.connect( self.saveStatus )
        self.commitButton.clicked.connect( self.commitStatus )
        self.forceUpdateButton.clicked.connect( self.updateStatus )
        self.forceResetButton.clicked.connect( self.resetStatus )
        # Button ToolTips
        self.saveButton.setToolTip('This will save (stash) the current state into the stash, which can be retrieved at a later time via the \"git stash\" command ')
        self.commitButton.setToolTip('This will initiate the process of creating and pushing the current status to the repository as a new version')
        self.forceUpdateButton.setToolTip('This will overwrite the current status with the most recent version of this branch')
        self.forceResetButton.setToolTip('This will overwrite the current status with the version before changes were made')

    def loadLayout(self):
        container = QVBoxLayout()
        info = QVBoxLayout()
        info.addWidget(self.info)
        buttons = QVBoxLayout()
        #=== status dependent loads
        buttons.addWidget(self.saveButton)
        buttons.addWidget(self.commitButton)
        buttons.addWidget(self.forceUpdateButton)
        buttons.addWidget(self.forceResetButton)
        container.addLayout(info)
        container.addLayout(buttons)
        self.setLayout(container)

    #===
    def saveStatus(self):
        return
    def commitStatus(self): #===
        CommitHandler(self.repository)
    def updateStatus(self):
        return
    def resetStatus(self):
        return

class CommitHandler(QDialog): #===
    class StageManager(QWidget):
        '''Allows the user to choose what to stage from modified and untracked files'''
        def __init__(self, repository):
            QWidget.__init__(self)
            self.repository = repository
            self.repository.git.reset('HEAD') # Unstage possible staged files
            # Get modified/untracked file names
            self.modified = [str(diff.a_blob.name) for diff in self.repository.head.commit.diff(None)]
            self.untracked = self.repository.untracked_files
            self.loadObjects()
            self.loadFunctions()
            self.loadLayout()
        def loadObjects(self):
            self.modLabel = QLabel('Modified files')
            self.modifiedList = QListWidget()
            self.modifiedList.addItems(self.modified)
            self.untLabel = QLabel('Untracked (new) files')
            self.untrackedList = QListWidget()
            self.untrackedList.addItems(self.untracked)
            self.moveButton = QPushButton('<->')
            self.outLabel = QLabel('Files to add to new version')
            self.outList = QListWidget()
        def loadFunctions(self):
            self.moveButton.clicked.connect( self.moveStuff )
            self.modifiedList.setSelectionMode( QAbstractItemView.ExtendedSelection )
            self.untrackedList.setSelectionMode( QAbstractItemView.ExtendedSelection )
            self.outList.setSelectionMode( QAbstractItemView.ExtendedSelection )
        def loadLayout(self):
            modAndUntLists = QVBoxLayout()
            modAndUntLists.addWidget( self.modLabel )
            modAndUntLists.addWidget( self.modifiedList )
            modAndUntLists.addWidget( self.untLabel )
            modAndUntLists.addWidget( self.untrackedList )
            fileLists = QHBoxLayout()
            fileLists.addLayout(modAndUntLists)
            fileLists.addWidget(self.moveButton)
            outList = QVBoxLayout()
            outList.addWidget(self.outLabel)
            outList.addWidget(self.outList)
            fileLists.addLayout(outList)
            container = QVBoxLayout()
            container.addLayout(fileLists)
            self.setLayout(container)
        def moveStuff(self):
            # Get selected items for each list
            modSelected = self.modifiedList.selectedItems()
            untSelected = self.untrackedList.selectedItems()
            outSelected = self.outList.selectedItems()
            # Take selected items, insert into appropriate list
            for item in modSelected:
                taken = self.modifiedList.takeItem(self.modifiedList.row(item))
                self.outList.insertItem(self.outList.count(), taken)
            for item in untSelected:
                taken = self.untrackedList.takeItem(self.untrackedList.row(item))
                self.outList.insertItem(self.outList.count(), taken)
            for item in outSelected:
                taken = self.outList.takeItem( self.outList.row(item) )
                if taken.text() in self.modified: # if item is modified
                    self.modifiedList.insertItem(self.modifiedList.count(),taken)
                elif taken.text() in self.untracked: # if item is untracked
                    self.untrackedList.insertItem(self.untrackedList.count(),taken)
                else:
                    print 'ERROR MOVING ITEM', taken
    def __init__(self, repository):
        QDialog.__init__(self)
        self.setWindowTitle('Create New Version')
        self.repository = repository
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.stageManager = self.StageManager(self.repository)
        self.messageManager = QTextEdit()
        self.stack = QTabWidget()
        self.stack.addTab(self.stageManager, u'Version File Manager')
        self.stack.addTab(self.messageManager, u'Version Message')
        self.doneButton = QPushButton('Finish')
        self.cancelButton = QPushButton('Cancel')
    def loadFunctions(self):
        self.doneButton.clicked.connect( self.finishCommit )
        self.doneButton.clicked.connect( self.cancelCommit )
    def loadLayout(self):
        container = QVBoxLayout()
        container.addWidget( QLabel('Decide what files to add and the message for the new version') )
        container.addWidget( self.stack )
        buttons = QHBoxLayout()
        buttons.addWidget(self.doneButton)
        buttons.addWidget(self.cancelButton)
        container.addLayout(buttons)
        self.setLayout(container)
    def finishCommit(self): #===
        print 'doneClicked()!'
    def cancelCommit(self): #===
        print 'cancelClicked()!'
        self.done(0)

class SaveStatus(QDialog): #===
    def __init__(self, repository):
        QDialog.__init__(self)
        self.repository = repository

        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()

    def loadObjects(self):
        return
    def loadFunctions(self):
        return
    def loadLayout(self):
        return

class InvalidRepoHandler(QDialog): #===
    def __init__(self, path):
        QDialog.__init__(self)
        self.path = path
        os.chdir(self.path)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.info1 = QTextEdit()
        self.info1.setText(str(self.path)+' is an invalid Git repository. Would you like to initialize it as a git repository?')
        self.yes = QPushButton('Yes, initialize repository')
        self.no = QPushButton('No, quit the gitTool')
    def loadFunctions(self):
        self.yes.clicked.connect( self.clickYes )
        self.no.clicked.connect( self.clickNo )
    def loadLayout(self):
        container = QVBoxLayout()
        container.addWidget(self.info1)
        buttons = QHBoxLayout()
        buttons.addWidget(self.yes)
        buttons.addWidget(self.no)
        container.addLayout(buttons)
        self.setLayout(container)
    def clickYes(self):
        rets = subprocess.check_output(['git','init'])
        print rets
        #=== need to setup remote repository
        self.done(1)
    def clickNo(self):
        self.done(0)

