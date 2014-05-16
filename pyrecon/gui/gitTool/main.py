import pyrecon, time, subprocess, os
from git import *
from PySide.QtCore import *
from PySide.QtGui import *

class RepositoryViewer(QWidget):
    '''Provides a GUI for interacting with a GitPython repository'''
    def __init__(self, repository):
        QWidget.__init__(self)
        self.repository = repository # The repository being used
        self.setWindowTitle('Repository - '+str(self.repository.working_dir))
        os.chdir(self.repository.working_dir) # Switch directory to repository's directory
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
        self.functions = FunctionsBar( self.repository )
        self.view = QStackedWidget() #===
    def loadFunctions(self):
        self.pickBranch.clicked.connect( self.checkoutBranch )
        self.pickCommit.clicked.connect( self.checkoutCommit )
        self.refreshBut.clicked.connect( self.refresh )
    def refresh(self):
        '''Refresh lists to match current repository status'''
        self.branches.refresh()
        self.commits.refresh() #=== will remove commits more recent than the one currently checkedout
    def checkoutBranch(self):
        '''Checkout branch and refresh() lists'''
        # Retrieve branch object
        item = self.branches.selectedItems().pop()
        branch = item.branch
        try:
            branch.checkout() # Checkout branch
            # Refresh commitList with commits from new branch
            self.branches.refresh()
            self.commits.refresh()
        except GitCommandError:
            if self.repository.is_dirty():
                print 'dirty repository: develop handler' #=== handle dirty working directory
        self.functions.clickConsole()
    def checkoutCommit(self):
        '''Reset HEAD to commit and refresh() lists'''
        # Retrive commit object
        item = self.commits.selectedItems().pop()
        commit = item.commit
        self.repository.head.reset(commit) # Reset head to commit
        self.branches.refresh()
        # self.commits.refresh() # removes commits more recent than the one being checkedout
        self.commits.loadColors()
        # Display console
        self.functions.clickConsole()
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
        functionsAndView = QVBoxLayout()
        functionsAndView.addWidget(self.view)
        functionsAndView.addWidget(self.functions)
        # Main container
        container = QHBoxLayout()
        container.addLayout(branchesAndCommits)
        container.addLayout(functionsAndView)
        self.setLayout(container)

class FunctionsBar(QWidget): #===
    def __init__(self, repository):
        QWidget.__init__(self)
        self.repository = repository
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
    def loadObjects(self):
        self.log = QPushButton('Log')
        self.log.setToolTip('View the log of git commands')
        self.console = QPushButton('Console')
        self.console.setToolTip('Open the console to run more sophisticated git commands')
        self.merge = QPushButton('Merge Tool')
        self.merge.setToolTip('Begin the process of merging a commit into the current status')
        self.branch = QPushButton('New Branch')
        self.branch.setToolTip('Create a new branch from the currently selected commit')
        self.functionView = QStackedWidget()
        # Load functions into QStackedWidget()
        self.functionView.addWidget( QTextEdit() ) # 0th index: Log
        self.functionView.addWidget( CommandConsole(self.repository) ) # 1st index: Console
        # self.functionView.addWidget() # 2nd index: Merge #===
        # self.functionView.addWidget() # 3rd index: Branch #===
    def loadFunctions(self): #===
        self.log.clicked.connect( self.clickLog )
        self.console.clicked.connect( self.clickConsole )
        self.merge.clicked.connect( self.clickMerge )
        self.branch.clicked.connect( self.clickBranch )
    def loadLayout(self):
        container = QVBoxLayout()
        buttons = QHBoxLayout()
        buttons.addWidget(self.log)
        buttons.addWidget(self.console)
        buttons.addWidget(self.merge)
        buttons.addWidget(self.branch)
        container.addLayout(buttons)
        container.addWidget(self.functionView)
        self.setLayout(container)
    def clickLog(self): #===
        ret = subprocess.check_output(['git', 'log'])
        self.functionView.widget(0).setText(ret)
        self.functionView.setCurrentIndex(0)
    def clickConsole(self): #===
        ret = subprocess.check_output(['git', 'status'])
        self.functionView.widget(1).output.setText(ret)
        self.functionView.setCurrentIndex(1)
    def clickMerge(self): #===
        print 'merge clicked'
    def clickBranch(self): #===
        print 'branch clicked'

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

class DirtyHandler(QWidget): #===
    '''Class for handling a dirty repository. Display modified/untracked files and allow user to handle them for a stash or push.'''
    def __init__(self, repository):
        QWidget.__init__(self)
        self.repository = repository
        # Untracked files
        self.untracked = self.repository.untracked_files
        self.diff = self.repository.head.commit.diff(None)# Diff rel to working dir
        self.checkStatus()
    def checkStatus(self):
        if (self.repository.is_dirty() and
            len(self.untracked) == 0 and 
            'up-to-date' in self.repository.git.pull()):
            print 'Files in the repository have been modified'
            #=== show changes
            #=== ask to stash or push
            return
        elif (self.repository.is_dirty() and
            len(self.untracked) > 0 and
            'up-to-date' in self.repository.git.pull()):
            print 'Files have been modified and there are untracked files.'
            #=== show changes
            #=== what to do with untracked files? add, rm
            #=== ask to stash or push
            return

class CommandConsole(QWidget):
    def __init__(self, repository):
        QWidget.__init__(self)
        self.repository = repository
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.subprocessCommand() # Run the default command
    def loadObjects(self):
        self.inputLine = QLineEdit('git status')
        self.output = QTextEdit()
    def loadFunctions(self):
        self.inputLine.returnPressed.connect( self.subprocessCommand )
    def loadLayout(self):
        inputBox = QHBoxLayout()
        inputBox.addWidget( self.inputLine )
        outputBox = QHBoxLayout()
        outputBox.addWidget( self.output )
        container = QVBoxLayout()
        container.addLayout(inputBox)
        container.addLayout(outputBox)
        self.setLayout(container)
    def subprocessCommand(self): #===
        cmdList = self.inputLine.text().split(' ')
        print 'run command', cmdList
        try:
            rets = subprocess.check_output( cmdList )
        except CalledProcessError:
            rets = str(CalledProcessError)
        self.output.setText( rets )

def main(repository=None):
    '''Pass in a path to git repository... return populated RepositoryViewer object'''
    if repository is None:
        #=== Ask to init repository
        print 'None as repository, open search or init'
        return
    # Open repository for gitTool
    repo = Repo(repository) # Open repository as GitPython Repo object
    if repo.is_dirty():
        #=== DirtyHandler()
        print 'repository is dirty ;)'
        return
    return RepositoryViewer(repo)

#=== TEST SCRIPT
if __name__ == '__main__':
    app = QApplication.instance()
    if app == None:
        app = QApplication([])
    a = main('~/Documents/pyreconGitTesting')
    a.show()
    app.exec_()
