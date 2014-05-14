import pyrecon, time
from git import *
from PySide.QtCore import *
from PySide.QtGui import *

class RepositoryViewer(QWidget):
    '''Provides a GUI for interacting with a GitPython repository'''
    def __init__(self, repository):
        QWidget.__init__(self)
        self.repository = repository
        print('Current head: '+str(self.repository.head.reference)) #===
        self.setWindowTitle('Repository - '+str(self.repository.working_dir))
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.branches = BranchList( [self.repository.head.ref]+[branch for branch in self.repository.heads if branch != self.repository.head.ref] )
        self.branches.item(0).setBackground(QColor('lightgreen'))
        self.commits = CommitList( [commit for commit in self.repository.iter_commits()] )
        self.commits.item(0).setBackground(QColor('lightgreen'))
        self.pickBranch = QPushButton('Checkout this branch')
        self.pickBranch.setMinimumHeight(50)
        self.pickCommit = QPushButton('Checkout this commit')
        self.pickCommit.setMinimumHeight(50)
        self.functions = QWidget()
        self.view = QWidget()
    def loadFunctions(self):
        self.pickBranch.clicked.connect( self.checkoutBranch )
        self.pickCommit.clicked.connect( self.checkoutCommit )
    def checkoutBranch(self):
        item = self.branches.selectedItems().pop()
        branch = item.branch
        branch.checkout()
        # Refresh commitList with commits from new branch
        self.commits.refresh( [commit for commit in self.repository.iter_commits()] )
        self.commits.item(0).setBackground(QColor('lightgreen')) #=== should this be default? Assumes that the latest commit is the one that will be in the repository when branch is switched. i.e. modified working dirs dont have a commit!!!!
        self.branches.loadColors()
        item.setBackground(QColor('lightgreen'))
    def checkoutCommit(self):
        item = self.commits.selectedItems().pop()
        commit = item.commit
        print 'Checkout commit: '+str(commit)
        self.repository.head.reset(commit) # reset head to commit
        self.commits.loadColors()
        item.setBackground(QColor('lightgreen'))
    def loadLayout(self):
        # BranchList and CommitList
        branchesAndCommits = QVBoxLayout()
        branchesLabel = QLabel('Branches')
        branchesLabel.setAlignment( Qt.AlignHCenter )
        branchesAndCommits.addWidget( branchesLabel )
        branchesAndCommits.addWidget(self.branches)
        branchesAndCommits.addWidget(self.pickBranch)
        commitsLabel = QLabel('Commits')
        commitsLabel.setAlignment( Qt.AlignHCenter )
        branchesAndCommits.addWidget( commitsLabel )
        branchesAndCommits.addWidget(self.commits)
        branchesAndCommits.addWidget(self.pickCommit)
        # Functions and View
        functionsAndView = QVBoxLayout()
        functionsAndView.addWidget(self.functions)
        functionsAndView.addWidget(self.view)
        # Main container
        container = QHBoxLayout()
        container.addLayout(branchesAndCommits)
        container.addLayout(functionsAndView)
        self.setLayout(container)

class BranchList(QListWidget):
    def __init__(self, branchList):
        QListWidget.__init__(self)
        self.setWindowTitle('Branches [*]')
        self.branches = branchList
        self.loadBranches()
        self.loadColors()
    def loadBranches(self):
        for branch in self.branches:
            item = BranchListItem(branch)
            self.addItem(item)
    def loadColors(self):
        count = 0
        for i in range(self.count()):
            item = self.item(i)
            if count%2 == 0:
                item.setBackground(QColor('lightgray'))
            else:
                item.setBackground(QColor('white'))
            count+=1
    def refresh(self, newBranchList=None):
        if newBranchList is not None:
            self.branches = newBranchList
        self.clear()
        self.loadBranches()

class BranchListItem(QListWidgetItem):
    def __init__(self, branch):
        QListWidgetItem.__init__(self)
        self.branch = branch
        self.setText(self.branch.name) #===
        self.setTextAlignment(Qt.AlignHCenter)
        self.setSizeHint(QSize(self.sizeHint().width(), 30))

class CommitList(QListWidget):
    def __init__(self, commitList):
        QListWidget.__init__(self)
        self.setWindowTitle('Commit History [*]')
        self.commits = commitList
        self.loadCommits()
        self.loadColors()
        self.setWordWrap(True)
    def loadCommits(self):
        for commit in self.commits:
            item = CommitListItem(commit)
            self.addItem(item)
    def loadColors(self):
        count = 0
        for i in range(self.count()):
            item = self.item(i)
            if count%2 == 0:
                item.setBackground(QColor('lightgray'))
            else:
                item.setBackground(QColor('white'))
            count+=1
    def refresh(self, newCommitList=None):
        if newCommitList is not None:
            self.commits = newCommitList
        self.clear()
        self.loadCommits()
        self.loadColors()
    
class CommitListItem(QListWidgetItem):
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

def main(repository):
    repo = Repo(repository) # Open repository as GitPython Repo object
    return RepositoryViewer(repo)

#=== TEST SCRIPT
if __name__ == '__main__':
    app = QApplication.instance()
    if app == None:
        app = QApplication([])
    a = main('~/Documents/pyreconGitTesting')
    a.show()
    app.exec_()
