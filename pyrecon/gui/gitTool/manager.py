from git import *
import os, subprocess

class RepoManager(Repo): #===
    '''Inherits from GitPythons Repo, added functions for easier access'''
    def __init__(self, repository):
        Repo.__init__(self, repository)
        self.directory = self.working_dir
        os.chdir(self.directory)

    # Local state accessors
    def needsHandling(self, untracked=False): #===
        '''Returns True if the repo needs any kind of handling.'''
        return (self.isDirty(untracked=untracked) or self.isDetached() or self.isBehind() or self.isDiverged())
    def isDirty(self, untracked=False):
        '''Return True if the repository is modified.
        untracked=True (check untracked files too)'''
        return self.is_dirty(untracked_files=untracked)
    def isDetached(self):
        '''Return True if head is detached'''
        return self.head.is_detached
    def isBehind(self):
        '''Returns True if the current branch is behind remote branch.'''
        self.fetch()
        return 'behind' in self.status()
    def isDiverged(self): #===
        '''Returns True if the current branch has diverged from remote'''
        self.fetch()
        return 'diverged' in self.status()

    # Local functions
    def checkout(self, branch=None, commit=None): #===
        if branch is not None:
            cmd = ['git','checkout',str(branch.name)]
        elif commit is not None:
            cmd = ['git','checkout',str(commit.hexsha)]
        return subprocess.check_output(cmd)
    def stash(self, untracked=False, message=None): #===
        '''Stash command'''
        cmd = ['git','stash','save']
        if untracked:
            cmd.append('-u')
        if message is not None:
            cmd.append(str(message))
        return subprocess.check_output(cmd)
    def commit(self): #===
        '''Start process for new commit.'''
        return
    def newBranch(self, name):
        cmd = ['git', 'branch', str(name)]
        return subprocess.check_output(cmd)
    def rename(self, branch, newName):
        cmd = ['git', 'branch', '-m', str(branch.name), str(newName)]
        return subprocess.check_output(cmd) #=== only local?
    def delete(self, branch): #===
        # if on branch, switch to master first
        if (not self.isDetached() and self.head.ref.name == branch):
            self.branches.master.checkout()
        # delete branch
        cmd = ['git','branch','-D',str(branch)]
        return subprocess.check_output(cmd)
    def merge(self): #===
        '''Merge two git objects'''
        return
    def status(self):
        cmd = ['git', 'status']
        return subprocess.check_output(cmd)

    # From remote
    def fetch(self, refspec=None):
        '''Fetch changes from remote origin.'''
        cmd = ['git','fetch','origin'] 
        if refspec is not None:
            cmd.append(str(refspec))
        return subprocess.check_output(cmd)
    def pull(self):
        '''Pull is fetch+merge.'''
        return

    # To remote
    def push(self, remote='origin', refspec='HEAD'):
        #=== check for changes; test what happens if remote is ahead
        cmd = ['git','push',str(remote),str(refspec)]
        return subprocess.check_output(cmd)