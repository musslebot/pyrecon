from git import *
import os, subprocess

class RepoManager(Repo): #===
    '''Inherits from GitPythons Repo, added functions for easier access'''
    def __init__(self, repository):
        Repo.__init__(self, repository)
        self.directory = self.working_dir
        os.chdir(self.directory)

    # Local functions
    def checkout(self, branch=None, commit=None):
        print 'checkout', branch #===
        return
    def isDirty(self, untracked=False):
        '''Return True if the repository is modified.
        untracked=True (check untracked files too)'''
        return self.is_dirty(untracked_files=untracked)
    def stash(self): #===
        return
    def commit(self): #===
        '''Start process for new commit.'''
        return
    def newBranch(self): #===
        '''Start process for new branch creation.'''
        return
    def rename(self, branch=None):
        print 'rename', branch #===
        return
    def delete(self, branch=None):
        print 'delete', branch #===
        return
    def merge(self): #===
        '''Merge two git objects'''
        return
    def status(self):
        cmd = ['git', 'status']
        return subprocess.check_output(cmd)

    # From remote
    def isBehind(self):
        '''Returns True if the current HEAD is behind remote HEAD.'''
        self.fetch()
        if 'behind' in self.status():
            return True
        return False
    def fetch(self):
        '''Fetch changes from remote origin.'''
        cmd = ['git','fetch'] 
        return subprocess.check_output(cmd)
    def pull(self):
        '''Pull is fetch+merge.'''
        return

    # To remote
    def push(self):
        #=== check for changes
        cmd = ['git','push','origin','HEAD']
        return subprocess.check_output(cmd)