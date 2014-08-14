gitTool
=============

# Overview
gitTool was designed in order to maintain different states of a project, and to provide the ability to traverse back and forth between these states with ease. This tool achieves this by interfacing `git` a source code management (SCM) software. Git saves the current states as a `commit`. `Commits` reference previous `commits` and each serve as an indivdual snapshot of the project throughout time. A user can also `branch` off of a `commit` in order to create two versions who are descendants of the same `commit`. So, in a sense, gitTool is a graphical user interface (GUI) to a lesser `git`. The reduced functionality is meant to prevent the user from being distracted by the complexity of `git`, whilst still taking advantage if its more essential functions. Therefore, I encourage users to delve deeper into the `git` universe to take advantage of all it has to offer.<br> [more about git](http://git-scm.com/)

# Introduction
<b>Terminology:</b><br>
* <b>`repository`</b> - the place where your project is stored -- in this instance, a folder (or directory) whose contents are the series (.ser) and section (.##) files<br>
 * `local repository` - a copy of the `repository` that exists on the machine you're using (local machine)<br>
 * `remote repository` - a repository that exists elsewhere (usually a server of some sort)<br>
* <b>`commit`</b> - a 'snapshot' of your projects status, changing to a different `commit` (`checkout`) alters your `repository's` contents in order to show the snapshot associated with a particular `commit`<br>
* <b>`branch`</b> - the complete range of `commits` that share an `ancestor commit` with some other `branch`<br>

# Walkthrough (GUI)
To use gitTool, first open the PyRECONSTRUCT GUI suite through the following commands in a Python shell:<br>
<pre>
import pyrecon
pyrecon.start()
</pre>

Open the gitTool by clicking on Tools > gitTool

The following pop-up will appear:<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/tree/master/pyrecon/tools/gitTool/images/browseandclone.png "browse and clone")<br>

To open a `repository` that exists on your machine, click the Browse button and search your computer for the repository

To `clone` a `repository` that exists elsewhere (a `remote repository`), click the Clone button and enter the address to the remote repository

You will now be presented with a window that displays the current state of your repository and provides functions for interacting with your project:<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/tree/master/pyrecon/tools/gitTool/images/repoviewer.png "repo viewer")<br>

* The most important feature of gitTool is the <b>Sync with remote</b> button. Each user will be working on their own local repository independently but must consistently `push` their new `commits` to the `remote repository` or `pull` others' `commits` from the `remote repository` in order to maintain a fluid, shared project.
 * More information about syncing is shown in the Sync section, below

* Under `Local Branches` (left) are the branches that currently exist on your local machine<br>
 * The ability to `checkout`, `rename`, or `delete` a local branch can be accessed by double-clicking a particular branch in the list
 * More advanced options (creating a new `branch` and `merging` branches) are accessed via the Branch Options button

* Under `Local Commits` (right) are the `commits` that currently exist on the `branch` you're currently in<br>
 * The newest commits are on the left end, whereas the old `commits` are on the right, going all the way back to the first commit
 * You can `checkout` old `commits` by double-clicking a `commit` in the list and then clicking `checkout`

Sync
---
After clicking Sync with remote, the Sync Manager window will appear:<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/tree/master/pyrecon/tools/gitTool/images/syncmanager.png "sync manager")<br>
The left pane shows `local branches` and the right shows `remote branches`. They are color-coded according to their relative status as follows:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Green</b> - local/remote are up-to-date<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Yellow</b> - local/remote are out of sync<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Red</b> - this branch does not exist in the repository<br>

Merge
---





