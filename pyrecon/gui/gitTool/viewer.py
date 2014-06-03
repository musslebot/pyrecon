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
        self.setWindowTitle('Repository: '+str(self.repo.directory))
        self.branchList = BranchViewer(self.repo, self)
        self.branchOptions = QPushButton('Branch Options') #===
        self.commitList = CommitViewer(self.repo, self)
        self.commitOptions = QPushButton('Commit Options') #===
        self.content = QStackedWidget() #=== View contents of repo
        # self.refreshBut = QPushButton('Sync && Refresh')
    def loadFunctions(self): #===
        # self.refreshBut.clicked.connect(self.refreshAll)
        # self.refreshBut.setMinimumHeight(50)
        self.branchOptions.clicked.connect(self.branchList.openOptions)
        self.commitOptions.clicked.connect(self.commitList.openOptions)
    def loadLayout(self):
        container = QVBoxLayout()
        contentLayout = QVBoxLayout()
        # contentLayout.addWidget(self.refreshBut)
        contentLayout.addWidget(QLabel('Repository Content'))
        contentLayout.addWidget(self.content)
        branchLayout = QVBoxLayout()
        branchHeader = QHBoxLayout()
        branchHeader.addWidget(QLabel('Branches'))
        branchHeader.addWidget(self.branchOptions)
        branchLayout.addLayout(branchHeader)
        branchLayout.addWidget(self.branchList)
        commitLayout = QVBoxLayout()
        commitHeader = QHBoxLayout()
        commitHeader.addWidget(QLabel('Commits'))
        commitHeader.addWidget(self.commitOptions)
        commitLayout.addLayout(commitHeader)
        commitLayout.addWidget(self.commitList)
        listLayout = QHBoxLayout()
        listLayout.addLayout(branchLayout)
        listLayout.addLayout(commitLayout)
        container.addLayout(contentLayout)
        container.addLayout(listLayout)
        self.setLayout(container)
    def refreshAll(self): #===
        if self.repo.isBehind(): # fetch from remote
            #=== BehindHandler()?
            print 'behind'
        if self.repo.isDirty():
            #=== ModifiedHandler()?
            print 'modified'
        self.branchList.refresh()
        self.commitList.refresh()
        return

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
        self.itemDoubleClicked.connect( self.openMenu )
    def loadBranches(self):
        for branch in self.repo.branches:
            item = self.BranchItem(branch)
            self.addItem(item)
    def loadColors(self):
        '''Alternates lightgray and white with green for the current HEAD'''
        count = 0
        for i in range(self.count()):
            item = self.item(i)
            if (not self.repo.head.is_detached and
                item.branch.commit == self.repo.head.commit):
                item.setBackground(QColor('lightgreen'))
            elif count%2 == 0:
                item.setBackground(QColor('lightgray'))
            else:
                item.setBackground(QColor('white'))
            count+=1
        if self.repo.isDetached(): # HEAD is detached
            '''Add detached head item to list.'''
            item = QListWidgetItem()
            item.setText('DETACHED HEAD')
            item.setTextAlignment(Qt.AlignHCenter)
            item.setSizeHint(QSize(self.sizeHint().width(), 30))
            item.setBackground(QColor('lightgreen'))
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
            #=== check for remote version
            #=== ask if remote version should be deleted too
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
            #=== check for remote version
            #=== ask if remote version should be deleted too
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
    def mergeBranches(self): #===
        return

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
            return
    def __init__(self, repository, viewer):
        QListWidget.__init__(self)
        self.repo = repository
        self.viewer = viewer
        self.menu = self.CommitMenu()
        self.loadCommits()
        self.loadColors()
        self.setWordWrap(True)
        self.setFlow(QListView.LeftToRight)
        self.itemDoubleClicked.connect( self.openMenu )
    def loadCommits(self):
        if not self.repo.head.is_detached: # check for detached head
            head = self.repo.head.ref
            for commit in self.repo.iter_commits('origin/'+str(head.name)):
                item = self.CommitItem(commit)
                self.addItem(item)
        # Check current state; Provide handling
        if self.repo.is_dirty():
            a = DirtyHandler(self.repo)
    def loadColors(self):
        count = 0
        for i in range(self.count()):
            item = self.item(i)
            if (item.commit == self.repo.head.commit):
                item.setBackground(QColor('lightgreen'))
            elif count%2 == 0:
                item.setBackground(QColor('lightgray'))
            else:
                item.setBackground(QColor('white'))
            count+=1
    def refresh(self):
        self.clear()
        self.loadCommits()
        self.loadColors()
    def openMenu(self, item):
        action = self.menu.exec_( QCursor.pos() )
        if action.text() == 'Checkout':
            response = self.repo.checkout(commit=item.commit)
            self.viewer.refreshAll()
    def openOptions(self): #===
        return
