import pyrecon, time
from git import *
from PySide.QtCore import *
from PySide.QtGui import *

class RepositoryViewer(QWidget):
    '''Provides a GUI for interacting with a GitPython repository'''
    def __init__(self, repository):
        QWidget.__init__(self)
        self.repository = repository
        self.setWindowTitle('Repository - '+str(self.repository.working_dir))
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.branches = BranchList( [branch for branch in self.repository.heads] )
        self.commits = CommitList( [commit for commit in self.repository.iter_commits()] )
        self.functions = QWidget()
        self.view = QWidget()
    def loadFunctions(self):
        # change repository button?
        # if branch is clicked, load commitsList
        self.branches.itemClicked.connect( self.branchClicked )
        # if commit is clicked, load functions/view
        return
    def branchClicked(self, item): #===
        print 'Branch clicked: '+str(item)
        self.commits.update( [commit for commit in self.repository.iter_commits()] )
        self.commits.setWindowTitle( 'Commits - '+str(item.name))
    def loadLayout(self):
        # BranchList and CommitList
        branchesAndCommits = QVBoxLayout()
        branchesLabel = QLabel('Branches')
        branchesLabel.setAlignment( Qt.AlignHCenter )
        branchesAndCommits.addWidget( branchesLabel )
        branchesAndCommits.addWidget(self.branches)
        commitsLabel = QLabel('Commits')
        commitsLabel.setAlignment( Qt.AlignHCenter )
        branchesAndCommits.addWidget( commitsLabel )
        branchesAndCommits.addWidget(self.commits)
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
    def loadBranches(self):
        count = 0
        for branch in self.branches:
            item = BranchListItem(branch)
            if count%2 == 0:
                item.setBackground(QColor('lightgray'))
            self.addItem(item)
            count+=1

class BranchListItem(QListWidgetItem):
    def __init__(self, branch):
        QListWidgetItem.__init__(self)
        self.branch = branch
        self.formatData()
        self.setText('Name:\t'+self.name) #===
    def formatData(self):
        self.name = str(self.branch.name)

class CommitList(QListWidget):
    def __init__(self, commitList):
        QListWidget.__init__(self)
        self.setWindowTitle('Commit History [*]')
        self.commits = commitList
        self.loadCommits()
    def loadCommits(self):
        count = 0
        for commit in self.commits:
            item = CommitListItem(commit)
            if count%2 == 0:
                item.setBackground(QColor('lightgray'))
            self.addItem(item)
            count+=1
    def update(self, commitList):
        self.commits = commitList
        self.clear()
        self.loadCommits()
    
class CommitListItem(QListWidgetItem):
    def __init__(self, commit):
        QListWidgetItem.__init__(self)
        self.commit = commit # GitPython commit object
        self.formatData()
        self.setText('Date:\t'+self.date+'\n'+'Author:\t'+self.author)
        self.setToolTip('Hexsha: '+self.hexsha+'\n'+'Commit message:\n\t'+self.message)
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
