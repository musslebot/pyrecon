from PySide.QtCore import *
from PySide.QtGui import *
from manager import RepoManager
from dialogs import *
import time

class RepoViewer(QWidget): #===
    '''Contains RepoManager for using git commands and provides a GUI for interacting with a git repository.'''
    def __init__(self, repository):
        QWidget.__init__(self)
        self.repo = RepoManager(repository)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self): #===
        self.setWindowTitle('Repository Viewer')
        self.branchList = BranchViewer(self.repo, self)
        self.branchOptions = QPushButton('Branch Options')
        self.branchOptions.setMaximumWidth(100)
        self.commitList = CommitViewer(self.repo, self)
        self.commitOptions = QPushButton('Commit Options')
        self.commitOptions.setMaximumWidth(100)
        # self.content = QStackedWidget() #=== View contents of repo
        self.syncBut = QPushButton('Sync with remote')
        self.syncBut.setMinimumHeight(50)
        self.syncBut.setToolTip('Open manager for handling remote content.')
        # Labels
        self.repoLabel = QLabel('Repository: %s'%self.repo.directory)
        self.repoLabel.setFont(QFont('Arial',14))
        self.branchLabel = QLabel('Local Branches')
        self.branchLabel.setFont(QFont('Arial',16))
        self.commitLabel = QLabel('Local Commits')
        self.commitLabel.setFont(QFont('Arial',16))
    def loadFunctions(self): #===
        self.syncBut.clicked.connect(self.remoteSync)
        self.branchOptions.clicked.connect(self.branchList.openOptions)
        self.commitOptions.clicked.connect(self.commitList.openOptions)
    def loadLayout(self):
        container = QVBoxLayout()
        contentLayout = QVBoxLayout()
        remoteButs = QHBoxLayout()
        remoteButs.addWidget(self.syncBut)
        contentLayout.addWidget(self.repoLabel)
        # contentLayout.addWidget(self.content)
        branchLayout = QVBoxLayout()
        branchHeader = QHBoxLayout()
        branchHeader.addWidget(self.branchLabel)
        branchHeader.addWidget(self.branchOptions)
        branchLayout.addLayout(branchHeader)
        branchLayout.addWidget(self.branchList)
        commitLayout = QVBoxLayout()
        commitHeader = QHBoxLayout()
        commitHeader.addWidget(self.commitLabel)
        commitHeader.addWidget(self.commitOptions)
        commitLayout.addLayout(commitHeader)
        commitLayout.addWidget(self.commitList)
        listLayout = QHBoxLayout()
        listLayout.addLayout(branchLayout)
        listLayout.addLayout(commitLayout)
        container.addLayout(contentLayout)
        container.addLayout(listLayout)
        container.addLayout(remoteButs)
        self.setLayout(container)
    def refreshAll(self): #===
        if self.repo.needsHandling():
            print 'needs handling!' #===
        self.branchList.refresh()
        self.commitList.refresh()
    def remoteSync(self,remote='origin',refspec=None): #===
        self.repo.fetch()
        if self.repo.isDirty():
            Message('gitTool has detected modifications to your current working directory -- These need to be handled before any remote syncing can be done.')
            a = DirtyHandler(self.repo)
            if a.result():
                pass
            else:
                return 
        # Open handler dialog
        rem = SyncHandler(self.repo) #===
        self.refreshAll()

class BranchViewer(QListWidget):
    class BranchItem(QListWidgetItem):
        def __init__(self, branch):
            QListWidgetItem.__init__(self)
            self.branch = branch
            self.setText(self.branch.name)
            self.setTextAlignment(Qt.AlignHCenter)
            self.setSizeHint(QSize(self.sizeHint().width(), 30))
    class BranchMenu(QMenu):
        def __init__(self):
            QMenu.__init__(self)
            self.loadActions()
        def loadActions(self):
            self.addAction('Checkout')
            self.addAction('Rename')
            self.addAction('Delete')
    class BranchOptions(QMenu):
        def __init__(self):
            QMenu.__init__(self)
            self.loadActions()
        def loadActions(self):
            self.addAction('New Branch')
            self.addAction('Merge Branches')
    def __init__(self, repository, viewer):
        QListWidget.__init__(self)
        self.setWindowTitle('Branches')
        self.repo = repository
        self.viewer = viewer
        self.menu = self.BranchMenu()
        self.options = self.BranchOptions()
        self.loadBranches()
        self.loadColors()
        self.setAlternatingRowColors(True)
        self.itemDoubleClicked.connect( self.openMenu )
    def loadBranches(self):
        for branch in self.repo.branches:
            item = self.BranchItem(branch)
            self.addItem(item)
    def loadColors(self):
        '''Alternates lightgray and white with green for the current HEAD'''
        for i in range(self.count()):
            item = self.item(i)
            if (not self.repo.head.is_detached and
                item.branch.name == self.repo.head.ref.name):
                item.setBackground(QColor('lightgreen'))
        # HEAD is detached
        if self.repo.isDetached():
            '''Add detached head item to list.'''
            item = QListWidgetItem()
            item.setText('DETACHED HEAD\nYou are currently not on any branch.')
            item.setToolTip('You may be checking out an old commit!')
            item.setTextAlignment(Qt.AlignHCenter)
            item.setSizeHint(QSize(self.sizeHint().width(), 30))
            item.setBackground(QColor('red'))
            item.setForeground(QColor('white'))
            self.insertItem(0,item)
    def refresh(self):
        self.clear()
        self.loadBranches()
        self.loadColors()
    def openMenu(self, item):
        action = self.menu.exec_( QCursor.pos() )
        if action.text() == 'Checkout':
            self.repo.checkout(branch=item.branch)
            self.viewer.refreshAll()
        elif action.text() == 'Rename':
            self.renameBranch(item.branch)
        elif action.text() == 'Delete':
            self.deleteBranch(item.branch)
    def openOptions(self):
        action = self.options.exec_( QCursor.pos() )
        if action.text() == 'New Branch': #===
            self.createBranch()
        elif action.text() == 'Merge Branches': #===
            self.mergeBranches()
    def renameBranch(self, branch):
        dialog = BranchHandler.RenameBranch(branch)
        if dialog.result(): # success
            newName = dialog.textLine.text()
            response = self.repo.rename(branch, newName)
            self.viewer.refreshAll()
            if response == '':
                Message('Successfully renamed branch: %s -> %s'%(branch.name,newName))
            else:
                Message(response)
        else:
            Message('Rename aborted...')
    def deleteBranch(self, branch):
        dialog = BranchHandler.DeleteBranch(branch)
        if dialog.result():
            response = self.repo.delete(branch=branch.name)
            self.viewer.refreshAll()
            if response == '':
                Message('Successfully deleted branch: %s'%(branch.name))
            else:
                Message(response)
        else:
            Message('Delete aborted...')
    def createBranch(self):
        dialog = BranchHandler.NewBranch()
        if dialog.result():
            newBranchName = dialog.branchName.text()
            response = self.repo.newBranch(newBranchName)
            self.viewer.refreshAll()
            if response == '':
                Message('New branch created: %s'%(newBranchName))
            else:
                Message(response)
        else:
            Message('Branch creation aborted...')
    def mergeBranches(self):
        dialog = MergeHandler(self.repo)
        if dialog.result():
            CommitHandler(self.repo)
        else:
            Message('mergeTool indicates that the merge was not successful...')
        self.viewer.refreshAll()

class CommitViewer(QListWidget):
    class CommitItem(QListWidgetItem):
        def __init__(self, commit):
            QListWidgetItem.__init__(self)
            self.commit = commit # GitPython commit object
            self.formatData()
            self.setText(self.date+'\n'+self.message)
            self.setToolTip('Hexsha: '+self.hexsha+'\n'+'Author:\t'+self.author)
            self.setTextAlignment(Qt.AlignHCenter)
        def formatData(self):
            # Format info to be displayed as item text
            self.date = str(time.asctime(time.gmtime(self.commit.committed_date)))
            self.author = str(self.commit.author)
            self.hexsha = str(self.commit.hexsha)
            self.message = str(self.commit.message)
    class CommitMenu(QMenu):
        def __init__(self):
            QMenu.__init__(self)
            self.loadActions()
        def loadActions(self):
            self.addAction('Checkout')
    class CommitOptions(QMenu):
        def __init__(self):
            QMenu.__init__(self)
            self.loadActions()
        def loadActions(self):
            self.addAction('Create New Commit')
            self.addAction('Stash Manager')
    def __init__(self, repository, viewer):
        QListWidget.__init__(self)
        self.repo = repository
        self.viewer = viewer
        self.menu = self.CommitMenu()
        self.options = self.CommitOptions()
        self.loadCommits()
        self.loadColors()
        self.setWordWrap(True)
        self.setFlow(QListView.LeftToRight)
        self.setAlternatingRowColors(True) #===
        self.itemDoubleClicked.connect( self.openMenu )
    def loadCommits(self): #=== avoid remote?
        # Not detached HEAD
        if (not self.repo.isDetached() and
            not self.repo.isAhead() and
            self.repo.head.ref.name in self.repo.git.branch('-r')
            ):
            head = self.repo.head.ref
            # git commits from remote (origin) #===
            for commit in self.repo.iter_commits('origin/'+str(head.name)):
                item = self.CommitItem(commit)
                self.addItem(item)
        # Detached HEAD or not remote
        else:
            for commit in self.repo.iter_commits():
                item = self.CommitItem(commit)
                self.addItem(item)
    def loadColors(self):
        for i in range(self.count()):
            item = self.item(i)
            if (item.commit == self.repo.head.commit):
                item.setBackground(QColor('lightgreen'))
    def refresh(self): #===
        if not self.repo.isDetached():
            self.clear()
            self.loadCommits()
        self.loadColors()
    def openMenu(self, item):
        action = self.menu.exec_( QCursor.pos() )
        if action.text() == 'Checkout':
            response = self.repo.checkout(commit=item.commit)
            self.viewer.refreshAll()
    def openOptions(self): #===
        action = self.options.exec_( QCursor.pos() )
        if action.text() == 'Create New Commit':
            self.newCommit()
        elif action.text() == 'Stash Manager':
            self.openStash()
    def newCommit(self): #===
        '''Begin process for making a new commit'''
        Message('New commit manager coming soon!')
    def openStash(self): #===
        '''Open the stash manager'''
        dialog = StashHandler(self.repo)

class ContentViewer(QStackedWidget): #===
    '''View the contents of the current repository.'''
    class ListView(QWidget): #===
        def __init__(self):
            QWidget.__init__(self)
    class GraphicalView(QWidget): #===
        def __init__(self):
            QWidget.__init__(self)
    def __init__(self, repository, viewer):
        QStackedWidget.__init__(self)
        return
