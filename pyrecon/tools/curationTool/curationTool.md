curationTool
=============

# Overview
curationTool was designed to find and display commonly-missed issues in a RECONSTRUCT series:
 * duplicate traces that overlap on the same section
 * traces of the same name separated by __ number of sections on which they do not exists
 * reverse traces 

# Walkthrough (GUI)
To use the curationTool, first open the PyRECONSTRUCT GUI suite through the following commands in a Python shell: <br>
<pre>
import pyrecon
pyrecon.start()
</pre>

Open the excelTool by clicking on Tools > curationTool

Click 'Load Series' to find your series' .ser file

Check the issues you want to locate and enter the parameter for the number of sections (distant traces)

Click 'Run curationTool' and wait for the text to appear on the right

You can also output this text to a .txt file
 