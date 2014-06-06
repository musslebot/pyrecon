'''This file contains the QDialogs used in the gitTool.'''
from PySide.QtCore import *
from PySide.QtGui import *
import subprocess, os
from git import *
from pyrecon.gui.main import BrowseWidget

class Message(QMessageBox):
    '''Create a basic popup message containing a message.'''
    def __init__(self, message, details=None):
        QMessageBox.__init__(self)
        self.setText(str(message))
        if details is not None:
            self.setInformativeText(str(details))
        self.exec_()

# Handlers for managing local repo
class BranchHandler(QDialog):
    class NewBranch(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            self.setWindowTitle('Create New Branch')
            self.loadObjects()
            self.loadFunctions()
            self.loadLayout()
            self.exec_()
        def loadObjects(self):
            self.textLabel1 = QLabel('This will create a new branch named:')
            self.branchName = QLineEdit()
            self.textLabel2 = QLabel('from the currently checked-out commit.')
            self.acceptBut = QPushButton('Finish')
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
            buttons.addWidget(self.acceptBut)
            buttons.addWidget(self.cancelBut)
            container = QVBoxLayout()
            container.addLayout(info)
            container.addLayout(buttons)
            self.setLayout(container)
        def userAccept(self):
            '''Check if valid branch name.'''
            if subprocess.call(['git', 'check-ref-format', '--branch', str(self.branchName.text())]) != 0:
                msg = QMessageBox()
                msg.setText('The branch name you have entered is invalid. Please try again...')
                msg.setInformativeText('From the documentation, git does NOT allow the following in branch names:\ntwo consecutive dots (..)\nASCII control characters (i.e. bytes whose values are lower than 040, or 177 DEL), space, tilde ~, caret ^, or colon :\nquestion-mark ?, asterisk *, or open bracket [\nbegin or end with a slash / or contain multiple consecutive slashes\nend with a dot .\na sequence @{\na back-slash \\')
                msg.exec_()
            else:
                self.done(1)
        def userReject(self):
            self.done(0)
    class DeleteBranch(QDialog):
        def __init__(self, branch):
            QDialog.__init__(self)
            self.branch = branch
            self.loadObjects()
            self.loadFunctions()
            self.loadLayout()
            self.exec_()
        def loadObjects(self):
            self.info = QLabel('You are about to delete the branch: %s\nThis canNOT be undone, and you will lose data.'%(self.branch.name))
            self.continueBut = QPushButton('Delete')
            self.cancelBut = QPushButton('Cancel')
        def loadFunctions(self):
            self.continueBut.clicked.connect( self.okay )
            self.cancelBut.clicked.connect( self.cancel )
        def loadLayout(self):
            buttons = QHBoxLayout()
            buttons.addWidget(self.cancelBut)
            buttons.addWidget(self.continueBut)
            container = QVBoxLayout()
            container.addWidget(self.info)
            container.addLayout(buttons)
            self.setLayout(container)
        def okay(self):
            self.done(1)
        def cancel(self):
            self.done(0)
    class RenameBranch(QDialog):
        def __init__(self, branch):
            QDialog.__init__(self)
            self.branch = branch
            self.loadObjects()
            self.loadFunctions()
            self.loadLayout()
            self.exec_()
        def loadObjects(self):
            self.label = QLabel('Enter new name for branch: %s'%self.branch.name)
            self.textLine = QLineEdit()
            self.okayBut = QPushButton('Rename')
            self.cancelBut = QPushButton('Cancel')
        def loadFunctions(self):
            self.okayBut.setMinimumHeight(50)
            self.cancelBut.setMinimumHeight(50)
            self.okayBut.clicked.connect( self.okay )
            self.cancelBut.clicked.connect( self.cancel )
        def loadLayout(self):
            container = QVBoxLayout()
            container.addWidget(self.label)
            container.addWidget(self.textLine)
            buttons = QHBoxLayout()
            buttons.addWidget(self.okayBut)
            buttons.addWidget(self.cancelBut)
            container.addLayout(buttons)
            self.setLayout(container)
        def okay(self):
            self.done(1) 
        def cancel(self):
            self.done(0)

class CommitHandler(QDialog):
    '''Handles adding/removing files from the index, supplying a commit message, and pushing to the remote repository.'''
    class StageManager(QWidget):
        '''Allows the user to choose what to stage from modified and untracked files'''
        def __init__(self, repository):
            QWidget.__init__(self)
            self.repository = repository
            self.repository.head.reset() # Unstage possible staged files
            # Get modified/untracked file names #=== what if detached?
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
        self.setWindowTitle('Create New Commit')
        self.repository = repository
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.stageManager = self.StageManager(self.repository)
        self.doneButton = QPushButton('Push New Version')
        self.cancelButton = QPushButton('Cancel')
        self.newBranch = QCheckBox('Commit to new branch?')
    def loadFunctions(self):
        self.doneButton.clicked.connect( self.finishCommit )
        self.doneButton.setMinimumHeight(50)
        self.cancelButton.clicked.connect( self.cancelCommit )
        self.cancelButton.setMinimumHeight(50)
    def loadLayout(self):
        container = QVBoxLayout()
        header = QHBoxLayout()
        header.addWidget(QLabel('ADD FILES TO THE NEW VERSION'))
        header.addWidget(self.newBranch)
        container.addLayout( header )
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
        # If newBranch is checked
        #=== make new branch
        if self.newBranch.isChecked():
            branchDialog = NewBranchHandler(self.repository)
            if branchDialog.result(): # successful: result() == 1
                branchName = branchDialog.branchName.text()
                branch = self.repository.create_head( branchName )
                msg = QMessageBox()
                msg.setText('Branch created: '+str(branchName))
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setText('New branch creations failed... try again.')
                msg.exec_()
                return
            try:
                branch.checkout() # Checkout branch
                subprocess.call(['git','branch','-u','origin'])
            except BaseException, e:
                msg = QMessageBox()
                msg.setText('Failed to switch to new branch. Aborting...\nReason:\n')
                msg.setInformativeText(str(e))
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
            subprocess.call(['git', 'push', 'origin', str(self.repository.head.ref.name)])
            self.done(1)
        else:
            return
    def cancelCommit(self):
        self.repository.head.reset() # Unstage any changes
        self.done(0)

class StashHandler(QDialog):
    class LoadStash(QDialog):
        def __init__(self, repository):
            QDialog.__init__(self)
            self.loadObjects()
            self.loadFunctions()
            self.loadLayout()
            self.exec_()
        def loadObjects(self):
            self.stashList = QComboBox()
            self.loadButton = QPushButton('Load Stashed State')
            self.cancelButton = QPushButton('Cancel')
        def loadFunctions(self):
            self.loadButton.setMinimumHeight(50)
            self.loadButton.clicked.connect( self.loadStash )
            self.cancelButton.clicked.connect( self.close )
            # Get stash list
            ret = subprocess.check_output(['git', 'stash','list'])
            self.stashList.insertItems(1,ret.split('\n'))
            self.stashList.insertItem(0,'<select stashed state>')
            self.stashList.setCurrentIndex(0)
        def loadLayout(self):
            container = QVBoxLayout()
            container.addWidget(self.stashList)
            container.addWidget(self.loadButton)
            container.addWidget(self.cancelButton)
            self.setLayout(container)
        def loadStash(self):
            index = self.stashList.currentIndex()
            # Did user select appropriate stash?
            msg = QMessageBox()
            if index == 0:
                msg.setText('Please select appropriate stashed state to load.')
                msg.exec_()
                return
            # Pop stash
            try:
                ret = subprocess.check_output(['git','stash','pop','stash@{%d}'%(index-1)])
                msg.setText('Stashed state successfully loaded!\n\n'+str(ret))
                msg.exec_()
                self.done(1)
            except BaseException, e:
                msg.setText('Error loading stashed state.\n\nReason:\n'+str(e))
                msg.exec_()
                return
    class SaveStash(QDialog):
        def __init__(self, repository):
            QDialog.__init__(self)
            self.repository = repository
            self.setWindowTitle('Stash Save Manager')
            self.loadObjects()
            self.loadFunctions()
            self.loadLayout()
            self.exec_()
        def loadObjects(self):
            self.currentState = QTextEdit()
            self.message = QLineEdit()
            self.includeUntracked = QCheckBox("Include untracked files")
            self.saveButton = QPushButton('Stash')
        def loadFunctions(self):
            self.currentState.setText(subprocess.check_output(['git','status']))
            self.message.setText('<Enter optional message>')
            self.saveButton.clicked.connect( self.saveStash )
            self.saveButton.setMinimumHeight(50)
        def loadLayout(self):
            container = QVBoxLayout()
            container.addWidget(self.currentState)
            container.addWidget(self.message)
            container.addWidget(self.includeUntracked)
            container.addWidget(self.saveButton)
            self.setLayout(container)
        def saveStash(self):
            msg = QMessageBox()
            try:
                # Save stash
                # - get message
                if self.message.text() == '<Enter optional message>':
                    stashMessage = ''
                else:
                    stashMessage = self.message.text()
                # - build list of commands
                cmdList = ['git','stash','save',str(stashMessage)]
                # - untracked
                if self.includeUntracked.isChecked():
                    cmdList.insert(3,'-u')
                # - run command
                ret = subprocess.check_output(cmdList)
                msg.setText('Stash successful!')
                msg.setInformativeText(ret)
                msg.exec_()
                self.done(1)
            except BaseException, e:
                msg.setText('Stash unsuccessful! :(')
                msg.setInformativeText('Reason:\n'+str(e)) # show exception
                msg.exec_()
    def __init__(self, repository):
        QDialog.__init__(self)
        self.setWindowTitle('Stash Manager')
        self.repository = repository
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.label = QLabel('Would you like to save (stash) the current state or load a previously stashed state?')
        self.saveButton = QPushButton('Stash Current State')
        self.loadButton = QPushButton('Load Stashed State')
    def loadFunctions(self):
        self.saveButton.setMinimumHeight(50)
        self.loadButton.setMinimumHeight(50)
        self.saveButton.clicked.connect( self.saveStash )
        self.loadButton.clicked.connect( self.loadStash )
    def loadLayout(self):
        buttons = QHBoxLayout()
        buttons.addWidget(self.saveButton)
        buttons.addWidget(self.loadButton)
        container = QVBoxLayout()
        container.addWidget(self.label)
        container.addLayout(buttons)
        self.setLayout(container)
    def saveStash(self):
        if not self.repository.is_dirty():
            msg = QMessageBox()
            msg.setText('Your repository has no changes to stash!')
            msg.exec_()
            return
        saveProcess = self.SaveStash(self.repository)
        if saveProcess.result():
            self.done(1)
        else:
            return
    def loadStash(self):
        if self.repository.is_dirty():
            msg = QMessageBox()
            msg.setText('Your repository is dirty! Please commit or clean your repository before loading a stashed state.')
            msg.exec_()
            return #===
        loadProcess = self.LoadStash(self.repository)
        if loadProcess.result():
            self.done(1)
        else:
            return

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
        self.goButton.clicked.connect( self.beginMergeTool )
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
    def beginMergeTool(self):
        try:
            from pyrecon.main import openSeries
            from pyrecon.tools.mergeTool.main import createMergeSet
            from pyrecon.gui.mergeTool.main import MergeSetWrapper
            # Get indeces
            srcB = self.srcBranchSelect.currentIndex()-1 # -1 to account for <choose branch> label
            srcC = self.srcCommitSelect.currentIndex()-1 # -1 to account for <choose commit> label
            dstB = self.dstBranchSelect.currentIndex()-1
            dstC = self.dstBranchSelect.currentIndex()-1
            # Get git objects for these indeces
            # - load source files into repository
            srcBranch = self.repository.branches[srcB]
            self.repository.git.checkout(srcBranch)
            srcCommit = [com for com in self.repository.iter_commits()][srcC]
            self.repository.git.checkout(srcCommit)
            ser2 = openSeries(self.repository.working_dir)
            # - load destination files into repository
            dstBranch = self.repository.branches[dstB]
            self.repository.git.checkout(dstBranch)
            dstCommit = [com for com in self.repository.iter_commits()][dstC]
            ser1 = openSeries(self.repository.working_dir)
            
            # MergeTool
            mergeSet = createMergeSet(ser1,ser2)
            mergeGui = MergeSetWrapper(mergeSet)
            
            mergeDialog = QDialog() # To make it popup in a window
            container = QHBoxLayout()
            container.addWidget(mergeGui)
            mergeDialog.setLayout(container)
            mergeDialog.setWindowTitle('MergeTool - git')
            mergeDialog.exec_()
            self.done(1)
        except BaseException, e:
            msg = QMessageBox()
            msg.setText('Could not start mergeTool!\n\nReason:\n'+str(e))
            msg.exec_()
            return

# Handlers for states that conflict with remote
class SyncHandler(QDialog):
    class LocalBranchItem(QListWidgetItem):
        class LocalMenu(QMenu):
            def __init__(self, color):
                QMenu.__init__(self)
                self.loadActions(color)
            def loadActions(self, color):
                if color == 'green':
                    self.addAction('Already in sync')
                elif color == 'yellow':
                    self.addAction('Sync with remote')
                elif color == 'red':
                    self.addAction('Push to remote')
        def __init__(self, name, remName, color):
            QListWidgetItem.__init__(self)
            self.setText(name)
            self.loadSpecifics(remName, color)
            self.setTextAlignment(Qt.AlignHCenter)
            self.setSizeHint(QSize(self.sizeHint().width(), 30))
        def loadSpecifics(self, remName, color):
            self.menu = self.LocalMenu(color)
            if color == 'green':
                self.setToolTip('This local branch is synced with %s'%remName)
                self.setBackground(QColor('lightgreen'))
            elif color == 'yellow':
                self.setToolTip('This local branch is tracking %s but is out-of-sync'%remName)
                self.setBackground(QColor('yellow'))
            elif color == 'red':
                self.setToolTip('This local branch does not exist in the remote repository.')
                self.setBackground(QColor('red'))
                self.setForeground(QColor('white'))
    class RemoteBranchItem(QListWidgetItem):
        class RemoteMenu(QMenu):
            def __init__(self, color):
                QMenu.__init__(self)
                self.loadActions(color)
            def loadActions(self, color):
                if color == 'green':
                    self.addAction('Already in sync')
                elif color == 'yellow':
                    self.addAction('Sync with local')
                elif color == 'red':
                    self.addAction('Pull to local')
        def __init__(self, name, locName, color):
            QListWidgetItem.__init__(self)
            self.setText(name)
            self.loadSpecifics(locName, color)
            self.setTextAlignment(Qt.AlignHCenter)
            self.setSizeHint(QSize(self.sizeHint().width(), 30))
        def loadSpecifics(self, locName, color):
            self.menu = self.RemoteMenu(color)
            if color == 'green':
                self.setToolTip('This remote branch is tracked by %s and is up-to-date'%locName)
                self.setBackground(QColor('lightgreen'))
            elif color == 'yellow':
                self.setToolTip('This remote branch is tracked by %s but is out-of-sync'%locName)
                self.setBackground(QColor('yellow'))
            elif color == 'red':
                self.setToolTip('This remote branch is not tracked by your local repository.')
                self.setBackground(QColor('red'))
                self.setForeground(QColor('white'))
    def __init__(self, repo):
        QDialog.__init__(self)
        self.setWindowTitle('Sync Manager')
        self.repo = repo
        self.repo.remote().fetch() # Fetch the most up-to-date remote
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.loadBranchLists()
        self.exec_()
    def loadObjects(self):
        self.localLabel = QLabel('Local Branches')
        self.localBranches = QListWidget()
        self.remoteLabel = QLabel('Remote Branches')
        self.remoteBranches = QListWidget()
        self.doneBut = QPushButton('Finished')
        self.doneBut.setMinimumHeight(50)
    def loadFunctions(self):
        self.doneBut.clicked.connect( self.finish )
        self.localBranches.itemDoubleClicked.connect( self.openMenu )
        self.remoteBranches.itemDoubleClicked.connect( self.openMenu )
    def loadLayout(self):
        container = QVBoxLayout()
        local = QVBoxLayout()
        local.addWidget(self.localLabel)
        local.addWidget(self.localBranches)
        remote = QVBoxLayout()
        remote.addWidget(self.remoteLabel)
        remote.addWidget(self.remoteBranches)
        branches = QHBoxLayout()
        branches.addLayout(local)
        branches.addLayout(remote)
        container.addLayout(branches)
        container.addWidget(self.doneBut)
        self.setLayout(container)
    def pairBranches(self):
        '''Group branches together based on their sync status.
        green -> in sync
        yellow -> out of sync
        red -> no remote-to-local relationship
        '''
        # Get branches
        local = [branch for branch in self.repo.branches]
        remote = [branch.lstrip(' ') for branch in self.repo.git.branch('-r').split('\n') if '->' not in branch] # This is only names of remote branch #=== is '->' a good exception?
        # Pair local branches with tracked remote branch and sync state color
        tracked = []
        for branch in local:
            # Local branch is tracking remote branch
            if str(branch.tracking_branch()) in remote:
                remoteRef = self.repo.remote().refs[branch.name]
                # is branch out of sync?
                if branch.commit == remoteRef.commit:
                    tracked.append( (branch.name,remoteRef.name,'green') ) # in sync
                else:
                    tracked.append( (branch.name,remoteRef.name,'yellow') ) # not synced
            else:
                tracked.append( (branch.name,None,'red') ) # not tracked
        # append remote branches that dont have local ref
        appendedRemotes = [branch[1] for branch in tracked]
        for branch in remote:
            if branch not in appendedRemotes:
                tracked.append( (None,branch,'red') )
        return tracked
    def loadBranchLists(self):
        '''Load local and remote branches into their branch lists, in order: green -> yellow -> red'''
        branchPairs = self.pairBranches()
        synced = [pair for pair in branchPairs if pair[2] == 'green']
        outSync = [pair for pair in branchPairs if pair[2] == 'yellow']
        noTrack = [pair for pair in branchPairs if pair[2] == 'red']
        for pair in synced:
            self.localBranches.addItem( self.LocalBranchItem(pair[0],pair[1],'green') )
            self.remoteBranches.addItem( self.RemoteBranchItem(pair[1],pair[0],'green'))
        for pair in outSync:
            self.localBranches.addItem( self.LocalBranchItem(pair[0],pair[1],'yellow') )
            self.remoteBranches.addItem( self.RemoteBranchItem(pair[1],pair[0],'yellow'))
        for pair in noTrack:
            if pair[0] is None: # on remote, not in local
                self.remoteBranches.addItem( self.RemoteBranchItem(pair[1],None,'red') )
            else: # in local, not on remote
                self.localBranches.addItem( self.LocalBranchItem(pair[0],None,'red') )
    def refresh(self): #===
        self.localBranches.clear()
        self.remoteBranches.clear()
        self.loadBranchLists()
    def openMenu(self, item): #===
        action = item.menu.exec_( QCursor.pos() )
        if action.text() in ['Sync with local','Sync with remote']: # remote is ahead, behind, or diverged
            branchName = str(item.text()).replace('origin/','') # name of local copy
            try:
                subprocess.call(['git','checkout',str(branchName)])
            except Exception, e:
                Message('Error:\n'+str(e))
            if self.repo.isAhead():
                a = AheadHandler(branchName)
            elif self.repo.isBehind():
                a = BehindHandler(branchName)
            elif self.repo.isDiverged(): #=== use MergeHandler
                Message('The remote branch and local branch have diverged. Merge them together.')
                a = DivergedHandler(branchName)
        elif action.text() == 'Pull to local': # remote not in local repo
            resp = subprocess.check_output(['git','checkout','-b',str(item.text()).replace('origin/',''),'--track',str(item.text())]) 
            Message(resp)
        elif action.text() == 'Push to remote': # local not in remote repo
            resp = self.repo.push(remote='origin',refspec=item.text(),setupstream=True)
            Message(resp)
        self.refresh()
    def finish(self):
        self.done(1)

class BehindHandler(QDialog): #===
    def __init__(self, branch):
        QDialog.__init__(self)
        self.branch = branch
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.label = QLabel('The local branch is behind the remote branch. Would you like to pull all of the commits ahead of your current state?')
        self.yesBut = QPushButton('Yes')
        self.noBut = QPushButton('No')
        self.yesBut.setMinimumHeight(50)
        self.noBut.setMinimumHeight(50)
    def loadFunctions(self):
        self.yesBut.clicked.connect( self.doPull )
        self.noBut.clicked.connect( self.dontPull )
    def loadLayout(self):
        container = QVBoxLayout()
        container.addWidget(self.label)
        buttons = QHBoxLayout()
        buttons.addWidget(self.yesBut)
        buttons.addWidget(self.noBut)
        container.addLayout(buttons)
        self.setLayout(container)
    def doPull(self):
        try:
            subprocess.call(['git','pull'])
        except Exception, e:
            Message('Error:\n'+str(e))
        self.done(1)
    def dontPull(self):
        self.done(0)

class AheadHandler(QDialog): #===
    def __init__(self,branch):
        QDialog.__init__(self)
        self.branch = branch
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.label = QLabel('The local branch is ahead the remote branch. Would you like to push all of the commits to the remote branch?')
        self.yesBut = QPushButton('Yes')
        self.noBut = QPushButton('No')
        self.yesBut.setMinimumHeight(50)
        self.noBut.setMinimumHeight(50)
    def loadFunctions(self):
        self.yesBut.clicked.connect( self.doPush )
        self.noBut.clicked.connect( self.dontPush )
    def loadLayout(self):
        container = QVBoxLayout()
        container.addWidget(self.label)
        buttons = QHBoxLayout()
        buttons.addWidget(self.yesBut)
        buttons.addWidget(self.noBut)
        container.addLayout(buttons)
        self.setLayout(container)
    def doPush(self):
        try:
            subprocess.call(['git','push','origin','HEAD'])
        except Exception, e:
            Message('Error:\n'+str(e))
        self.done(1)
    def dontPush(self):
        self.done(0)
class DivergedHandler(QDialog): #===
    def __init__(self):
        QDialog.__init__(self)
        self.exec_()
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
        self.stashButton = QPushButton('Save (stash) current state')
        self.commitButton = QPushButton('Commit a new version')
        self.forceResetButton = QPushButton('Delete changes since last commit')
        self.cancelButton = QPushButton('Cancel')
    def loadFunctions(self):
        # Button function links
        self.stashButton.clicked.connect( self.stashStatus )
        self.commitButton.clicked.connect( self.commitStatus )
        self.forceResetButton.clicked.connect( self.resetStatus ) #===
        self.cancelButton.clicked.connect( self.close )
        # Button ToolTips
        self.stashButton.setToolTip('This will save (stash) the current state into the stash, which can be retrieved at a later time via the \"git stash\" command ')
        self.commitButton.setToolTip('This will initiate the process of creating and pushing the current status to the repository as a new version')
        self.forceResetButton.setToolTip('This will overwrite the current status with the version before changes were made')
    def loadLayout(self):
        container = QVBoxLayout()
        info = QVBoxLayout()
        info.addWidget(self.info)
        buttons = QVBoxLayout()
        #=== status dependent loads
        buttons.addWidget(self.stashButton)
        if (not self.repository.isBehind() and
            self.repository.isDirty()
            ):
            buttons.addWidget(self.commitButton)
        if (self.repository.isDirty()):
            buttons.addWidget(self.forceResetButton)
        buttons.addWidget(self.cancelButton)
        container.addLayout(info)
        container.addLayout(buttons)
        self.setLayout(container)
    def commitStatus(self):
        commitProcess = CommitHandler(self.repository)
        if commitProcess.result(): # result == 1
            self.done(1)
        else:
            return
    def stashStatus(self):
        stashProcess = StashHandler(self.repository)
        if stashProcess.result():
            self.done(1)
        else:
            return
    def resetStatus(self):
        '''Hard reset of HEAD'''
        confirm = QMessageBox()
        confirm.setText('Are you sure you want to reset your repository\'s state?')
        confirm.setInformativeText('This will permanently remove any modifications you have made from the previous state and can not be retrieved once deleted.')
        confirm.setStandardButtons( QMessageBox.Yes | QMessageBox.No)
        ret = confirm.exec_()
        if ret == QMessageBox.Yes:
            try:
                self.repository.head.reset('--hard')
                self.done(1)
            except BaseException, e:
                msg = QMessageBox()
                msg.setText('Reset failed.\nReason:\n\n')
                msg.setInformativeText(str(e))
                msg.exec_()
        elif ret == QMessageBox.No:
            msg = QMessageBox()
            msg.setText('Aborting reset...')
            msg.exec_()

# Handlers for connecting gitTool to a local repo
class InvalidRepoHandler(QDialog): #===
    class RemoteRequest(QDialog): #===
        '''Request location of remote repository'''
        def __init__(self):
            QDialog.__init__(self)
            self.loadObjects()
            self.loadFunctions()
            self.loadLayout()
            self.exec_()
        def loadObjects(self):
            self.label = QLabel('Enter the path to the remote repository:')
            self.remotePath = QLineEdit()
            self.doneBut = QPushButton('Continue')
        def loadFunctions(self):
            self.doneBut.setMinimumHeight(50)
            self.doneBut.clicked.connect( self.finish )
        def loadLayout(self):
            container = QVBoxLayout()
            container.addWidget(self.label)
            container.addWidget(self.remotePath)
            container.addWidget(self.doneBut)
            self.setLayout(container)
        def finish(self): #===
            # check if appropriate
            msg = QMessageBox()
            try:
                subprocess.call(['git','remote','add','origin',str(self.remotePath.text())])
                subprocess.call(['git','branch','-u','origin'])
                self.done(1)
            except BaseException, e:
                msg.setText('Error:\n\n'+str(e))
                msg.exec_()
                return
    def __init__(self, path):
        QDialog.__init__(self)
        self.path = path
        os.chdir(self.path)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.info1 = QLabel()
        self.info1.setText(str(self.path)+' is an invalid Git repository. Would you like to initialize it as a git repository?')
        self.yes = QPushButton('Yes, initialize repository')
        self.no = QPushButton('No, quit the gitTool')
    def loadFunctions(self):
        self.yes.setMinimumHeight(50)
        self.no.setMinimumHeight(50)
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
        remReq = self.RemoteRequest()
        self.done(1)
    def clickNo(self):
        self.done(0)

class BrowseRepository(QDialog): #===
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('Browse for your repository')
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.path = BrowseWidget()
        self.doneBut = QPushButton()
    def loadFunctions(self):
        self.doneBut.setMinimumHeight(50)
        self.doneBut.setText('Open Repository')
        self.doneBut.clicked.connect( self.finish )
    def loadLayout(self):
        main = QVBoxLayout()
        main.addWidget(self.path)
        main.addWidget(self.doneBut)
        self.setLayout(main)
    def finish(self):
        self.output = str(self.path.path.text())
        if 'Enter or browse' not in self.output or self.output == '':
            self.done(1)
        else:
            msg=QMessageBox()
            msg.setText('Invalid output directory: '+str(self.output))
            msg.exec_()
            return
