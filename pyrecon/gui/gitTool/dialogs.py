'''This file contains the QDialogs used in the gitTool.'''
from PySide.QtCore import *
from PySide.QtGui import *
import subprocess, os
from git import *

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
        self.saveButton.clicked.connect( self.saveStatus ) #===
        self.commitButton.clicked.connect( self.commitStatus )
        self.forceUpdateButton.clicked.connect( self.updateStatus ) #===
        self.forceResetButton.clicked.connect( self.resetStatus ) #===
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
    def commitStatus(self):
        commitProcess = CommitHandler(self.repository)
        if commitProcess.result(): # result == 1
            self.done(1)
        else:
            return
    def updateStatus(self):
        return
    def resetStatus(self):
        return

class CommitHandler(QDialog):
    '''Handles adding/removing files from the index, supplying a commit message, and pushing to the remote repository.'''
    class StageManager(QWidget):
        '''Allows the user to choose what to stage from modified and untracked files'''
        def __init__(self, repository):
            QWidget.__init__(self)
            self.repository = repository
            self.repository.head.reset() # Unstage possible staged files
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
                    print 'ERROR MOVING ITEM', taken.text()
    class MessageManager(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            self.loadObjects()
            self.loadFunctions()
            self.loadLayout()
            self.exec_()
        def loadObjects(self):
            self.message = QLineEdit()
            self.okBut = QPushButton('Okay')
            self.cancelBut = QPushButton('Cancel')
        def loadFunctions(self):
            self.okBut.clicked.connect( self.finish )
            self.cancelBut.clicked.connect( self.cancel )
        def loadLayout(self):
            container = QVBoxLayout()
            container.addWidget(QLabel('Enter a description of the new version:'))
            container.addWidget(self.message)
            buttons = QHBoxLayout()
            buttons.addWidget(self.okBut)
            buttons.addWidget(self.cancelBut)
            container.addLayout(buttons)
            self.setLayout(container)
        def finish(self):
            if len(self.message.text()) == 0:
                msg = QMessageBox()
                msg.setText('Please enter a description of the new version!')
                msg.exec_()
                return
            self.done(1)
        def cancel(self):
            self.done(0)
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
        self.doneButton = QPushButton('Push New Version')
        self.cancelButton = QPushButton('Cancel')
    def loadFunctions(self):
        self.doneButton.clicked.connect( self.finishCommit )
        self.doneButton.setMinimumHeight(50)
        self.cancelButton.clicked.connect( self.cancelCommit )
        self.cancelButton.setMinimumHeight(50)
    def loadLayout(self):
        container = QVBoxLayout()
        container.addWidget( QLabel('ADD FILES TO THE NEW VERSION') )
        container.addWidget( self.stageManager )
        buttons = QHBoxLayout()
        buttons.addWidget(self.doneButton)
        buttons.addWidget(self.cancelButton)
        container.addLayout(buttons)
        self.setLayout(container)
    def finishCommit(self):
        # Check to make sure description is valid
        outputList = self.stageManager.outList
        if outputList.count() == 0:
            msg = QMessageBox()
            msg.setText('Please add files to your new version!')
            msg.exec_()
            return
        # Get list of files to be pushed as new version
        outFiles = [outputList.item(row).text() for row in xrange(outputList.count())]
        self.repository.index.add(outFiles) # Add them to index
        # Get version description
        desc = CommitHandler.MessageManager()
        description = desc.message.text()
        # Confirm before push
        msg = QMessageBox()
        msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
        msg.setText('You are about to push a version to the remote repository branch: '+str(self.repository.head.ref.name)+'\nMake sure everything is correct before clicking OK')
        msg.setInformativeText('DESCRIPTION: '+description+'\n\n'+str(subprocess.check_output(['git','status'])))
        if msg.exec_() == QMessageBox.Ok:
            self.repository.index.commit(description)
            self.repository.remotes.origin.push()
            self.done(1)
        else:
            return
    def cancelCommit(self):
        self.repository.head.reset() # Unstage any changes
        self.done(0)

class StashHandler(QDialog): #===
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

class NewBranchHandler(QDialog):
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

class MergeHandler(QDialog): #===
    def __init__(self, repository):
        QDialog.__init__(self)
        self.setWindowTitle('Merge Manager')
        self.repository = repository
        self.branches = self.repository.branches

        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        # Select the branch/commit to be merged
        self.srcBranchSelect = QComboBox()
        self.srcBranchSelect.addItems(['<source branch>']+[branch.name for branch in self.branches])
        self.srcCommitSelect = QComboBox()
        self.srcCommitSelect.addItem('<select branch first>')
        # Select the branch/commit to merge into
        self.dstBranchSelect = QComboBox()
        self.dstBranchSelect.addItems(['<destination branch>']+[branch.name for branch in self.branches])
        self.dstCommitSelect = QComboBox()
        self.dstCommitSelect.addItem('<select branch first>')
        self.goButton = QPushButton('Start MergeTool')
    def loadFunctions(self):
        self.goButton.setMinimumHeight(50)
        # add items to (src/dst)CommitSelect upon choice of branch
        self.srcBranchSelect.currentIndexChanged.connect( self.updateCommits )
        self.dstBranchSelect.currentIndexChanged.connect( self.updateCommits )
    def loadLayout(self):
        container = QVBoxLayout()
        srcSelect = QVBoxLayout()
        srcSelect.addWidget(QLabel('Merge This'))
        srcSelect.addWidget(self.srcBranchSelect)
        srcSelect.addWidget(self.srcCommitSelect)
        dstSelect = QVBoxLayout()
        dstSelect.addWidget(QLabel('Into This'))
        dstSelect.addWidget(self.dstBranchSelect)
        dstSelect.addWidget(self.dstCommitSelect)
        selector = QHBoxLayout()
        selector.addLayout( srcSelect )
        selector.addLayout( dstSelect )
        container.addLayout(selector)
        container.addWidget(self.goButton)
        self.setLayout(container)
    def updateCommits(self, index):
        branch = self.branches[index-1]
        commits = [com for com in self.repository.iter_commits('origin/'+branch.name)]
        if self.sender() == self.srcBranchSelect: # Update src commits
            self.srcCommitSelect.clear()
            self.srcCommitSelect.addItems(['<source commit>']+[com.message for com in commits])
        elif self.sender() == self.dstBranchSelect: # Update dst commits
            self.dstCommitSelect.clear()
            self.dstCommitSelect.addItems(['<destination commit>']+[com.message for com in commits])

class BrowseRepository(QDialog): #===
    def __init__(self):
        QDialog.__init__(self)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        return
    def loadFunctions(self):
        return
    def loadLayout(self):
        return
