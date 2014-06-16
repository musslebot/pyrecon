from PySide.QtGui import QApplication, QMessageBox
from dialogs import RepoHandler, Message
from viewer import RepoViewer

def main(repository=None): #===
    '''Pass in a path to git repository... return populated RepositoryViewer object'''
    if repository is None:
        helper = RepoHandler()
    try:
        print helper.repo #===
        return RepoViewer(helper.repo)
    except Exception, e:
        Message('Error loading repository!\nReason:\n\t'+str(e))

#=== TEST SCRIPT
if __name__ == '__main__':
    app = QApplication.instance()
    if app == None:
        app = QApplication([])
    a = main()
    a.show()
    app.exec_()