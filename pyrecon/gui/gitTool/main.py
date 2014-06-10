from PySide.QtGui import QApplication, QMessageBox
from dialogs import BrowseRepository, Message
from viewer import RepoViewer

def main(repository=None): #===
    '''Pass in a path to git repository... return populated RepositoryViewer object'''
    if repository is None:
        done = False
        while not done: #=== user can't close application
            try:
                browse = BrowseRepository()
                repo = RepoViewer( browse.output )
                done = True
            except Exception, e:
                msg = Message('Error loading repository:\n'+str(e))
    return repo

#=== TEST SCRIPT
if __name__ == '__main__':
    app = QApplication.instance()
    if app == None:
        app = QApplication([])
    a = main()
    a.show()
    app.exec_()