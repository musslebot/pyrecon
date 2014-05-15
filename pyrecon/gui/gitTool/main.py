import pyrecon, time
from git import *
from PySide.QtCore import *
from PySide.QtGui import *

class RepositoryViewer(QWidget):
    '''Provides a GUI for interacting with a GitPython repository'''
    def __init__(self, repository):
        QWidget.__init__(self)
        self.repository = repository # The repository being used
        self.setWindowTitle('Repository - '+str(self.repository.working_dir))
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        # List of branches in the repository
        self.branches = BranchList( self.repository )
        # List of commits for the currently selected branch
        self.commits = CommitList( self.repository )
        self.refreshBut = QPushButton('Refresh')
        self.refreshBut.setToolTip('Click this if you\'ve made changes in the repository outside of this tool')
        self.pickBranch = QPushButton('Checkout this branch')
        self.pickBranch.setMinimumHeight(50)
        self.pickCommit = QPushButton('Checkout this commit')
        self.pickCommit.setMinimumHeight(50)
    def loadFunctions(self):
        self.pickBranch.clicked.connect( self.checkoutBranch )
        self.pickCommit.clicked.connect( self.checkoutCommit )
        self.refreshBut.clicked.connect( self.refresh )
    def refresh(self):
        '''Refresh lists to match current repository status'''
        self.branches.refresh()
        self.commits.refresh()
    def checkoutBranch(self):
        '''Checkout branch and refresh() lists'''
        # Retrieve branch object
        item = self.branches.selectedItems().pop()
        branch = item.branch
        branch.checkout() # Checkout branch
        # Refresh commitList with commits from new branch
        self.branches.refresh()
        self.commits.refresh()
    def checkoutCommit(self):
        '''Reset HEAD to commit and refresh() lists'''
        # Retrive commit object
        item = self.commits.selectedItems().pop()
        commit = item.commit
        self.repository.head.reset(commit) # Reset head to commit
        self.branches.refresh()
        self.commits.refresh()
    def loadLayout(self):
        # BranchList and CommitList
        branchesAndCommits = QVBoxLayout()
        branchesLabel = QLabel('Branches')
        branchesLabelandRef = QHBoxLayout()
        branchesLabelandRef.addWidget(branchesLabel)
        branchesLabelandRef.addWidget(self.refreshBut)
        branchesAndCommits.addLayout( branchesLabelandRef )
        branchesAndCommits.addWidget(self.branches)
        branchesAndCommits.addWidget(self.pickBranch)
        commitsLabel = QLabel('Commits')
        branchesAndCommits.addWidget( commitsLabel )
        branchesAndCommits.addWidget(self.commits)
        branchesAndCommits.addWidget(self.pickCommit)
        # Functions and View
        # functionsAndView = QVBoxLayout()
        # functionsAndView.addWidget(self.functions)
        # functionsAndView.addWidget(self.view)
        # Main container
        container = QHBoxLayout()
        container.addLayout(branchesAndCommits)
        # container.addLayout(functionsAndView)
        self.setLayout(container)

class BranchList(QListWidget):
    def __init__(self, repository):
        QListWidget.__init__(self)
        self.setWindowTitle('Branches')
        self.repository = repository
        self.loadBranches()
        self.loadColors()
    def loadBranches(self):
        for branch in self.repository.heads:
            item = BranchListItem(branch)
            self.addItem(item)
    def loadColors(self):
        '''Alternates lightgray and white with green for the current HEAD'''
        count = 0
        for i in range(self.count()):
            item = self.item(i)
            if item.branch == self.repository.head.ref:
                item.setBackground(QColor('lightgreen'))
            elif count%2 == 0:
                item.setBackground(QColor('lightgray'))
            else:
                item.setBackground(QColor('white'))
            count+=1
    def refresh(self):
        self.clear()
        self.loadBranches()
        self.loadColors()

class BranchListItem(QListWidgetItem):
    def __init__(self, branch):
        QListWidgetItem.__init__(self)
        self.branch = branch
        self.setText(self.branch.name)
        self.setTextAlignment(Qt.AlignHCenter)
        self.setSizeHint(QSize(self.sizeHint().width(), 30))

class CommitList(QListWidget):
    def __init__(self, repository):
        QListWidget.__init__(self)
        self.setWindowTitle('Commit History')
        self.repository = repository
        self.loadCommits()
        self.loadColors()
        self.setWordWrap(True)
    def loadCommits(self):
        for commit in self.repository.iter_commits(): #=== Get commits from branch, not repository... otherwise will remove commits greater than currently selected date
            item = CommitListItem(commit)
            self.addItem(item)
    def loadColors(self):
        count = 0
        for i in range(self.count()):
            item = self.item(i)
            if item.commit == self.repository.head.ref.commit: #===
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
