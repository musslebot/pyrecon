gitTool
=============

# Overview
gitTool was designed in order to maintain different states of a project, and to provide the ability to traverse back and forth between these states with ease. This tool achieves this by interfacing `git` a source code management (SCM) software. Git saves the current states as a `commit`. `Commits` reference previous `commits` and each serve as an indivdual snapshot of the project throughout time. A user can also `branch` off of a `commit` in order to create two versions who are descendants of the same `commit`. So, in a sense, gitTool is a graphical user interface (GUI) to a lesser `git`. The reduced functionality is meant to prevent the user from being distracted by the complexity of `git`, whilst still taking advantage if its more essential functions. Therefore, I encourage users to delve deeper into the `git` universe to take advantage of all it has to offer.<br> [more about git](http://git-scm.com/)

# Introduction
<b>Terminology:</b><br>
<b>`repository`</b> - the place where your project is stored -- in this instance, a folder (or directory) whose contents are the series (.ser) and section (.##) files<br>
> `local repository` - a copy of the `repository` that exists on the machine you're using (local machine)<br>
> `remote repository` - a repository that exists elsewhere (usually a server of some sort)<br>

<b>`commit`</b> - a 'snapshot' of your projects status, changing to a different `commit` alters your `repository's` contents in order to show the snapshot associated with a particular `commit`<br>
<b>`branch`</b> - the complete range of `commits` that share an `ancestor commit` with some other `branch`<br>


# Walkthrough (GUI)
To use gitTool, first open the PyRECONSTRUCT GUI suite through the following commands in a Python shell:<br>
<pre>
import pyrecon
pyrecon.start()
</pre>

Open the gitTool by clicking on Tools > gitTool

The following pop-up will appear:<br>
# IMAGE TO CLONE/OPEN

To open a `repository` that exists on your machine, click the #FIXME open `repository`.

To `clone` a `repository` that exists elsewhere (a `remote repository`), click the #FIXME clone `repository` button

---

You will now be presented with a window that displays the current state of your repository and provides functions for interacting with your project:<br>
# IMAGE TO REPOSITORY VIEWER

Important features:
 Sync - Each user will be working on a project from their own `local repository`. In order to ensure that each user's repository is up-to-date with the `remote repository`, gitTool provides a sync feature in order to `push` and/or `pull` the `commits` to and from the `remote repository`.





