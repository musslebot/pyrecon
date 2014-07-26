mergeTool
=============

# Overview
mergeTool was designed to ease the merging of series projects that have been worked on by different people e.g. Bobby and Amanda worked on series ABCDE on different computers, each tracing their own structures. Now that they're finished, they wish to merge their projects together.
mergeTool provides a GUI to help resolve conflicts with overlapping contours.

# Walkthrough (GUI)
To use the mergeTool, first open the PyRECONSTRUCT GUI suite through the following commands in a Python shell: <br>
<pre>
import pyrecon
pyrecon.start()
</pre>

Open the excelTool by clicking on Tools > mergeTool

Browse or enter the path to the two separate .ser files you wish to merge and click 'Load Series'

After a short while (depending on size of the series) a list of all the sections will appear on the left, color coded based on whether there are merge conflicts in the section.

