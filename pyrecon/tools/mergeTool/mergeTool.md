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

Open the mergeTool by clicking on Tools > mergeTool

Browse or enter the path to the two separate .ser files you wish to merge and click 'Load Series'

After a short while (depending on size of the series) a window will pop up, displaying files and conflict details.
<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/raw/master/pyrecon/tools/mergeTool/images/mergeTool-begin.png "Step 1")
<br>
On the left is a list of all the files, color coded based on the state of their conflicts: green meaning no conflicts and yellow meaning that there are conflicts that need to be resolved.
<br>
To resolve a conflict click on a series or section file in the left navigation window. Once clicked, the right side will update with the 3 tabs that represent data in the file. Click on the tabs individually to view/resolve any conflicts that may exist.
<br>
Here is an example of conflict contours, viewed with clicking the Contours tab:<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/raw/master/pyrecon/tools/mergeTool/images/mergeTool-overlaps.png "Step 2")
<br>
Contours that will be output to the new, merged series occupy the bottom half of the window. Contours that are not yet output occupy the top half. To move a contour to the output series, click on the contour to highlight it, then click Move Selected. <b>*NOTE: (Contours only) the Save Current Status button must be clicked in order to ensure that the contour resolutions will be retained for output.</b>
<br>
The picture above shows two conflicting contours. To resolve them, double-click the item to bring up a resolution window:
<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/raw/master/pyrecon/tools/mergeTool/images/mergeTool-overlaps-res.png "Step 3")
<br>
The two contours will be displayed above the image. Click one of the buttons to choose which contour to keep.
<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/raw/master/pyrecon/tools/mergeTool/images/mergeTool-overlaps-resolved.png "Step 4")
<br>
 *Do not forget to move the contour to output when finished*
<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/raw/master/pyrecon/tools/mergeTool/images/mergeTool-overlaps-toout.png "Step 5")
<br>
Save the state and take note that the section file is now green, indicating that conflicts have been resolved!
<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/raw/master/pyrecon/tools/mergeTool/images/mergeTool-saveSection.png "Step 6")
<br>
Once you are ready to output the new series, click on the Save button in the bottom left:
<br>
![alt text](https://github.com/wtrdrnkr/pyrecon/raw/master/pyrecon/tools/mergeTool/images/mergeTool-save-unresolved.png "Step 7")
<br>
Any conflicts that have not been resolved will appear in a confirmation window: click Cancel to abort the save and continue resolving conflicts. Click okay to default all unresolved conflicts to those shown on the left (the first series you opened in the begining).
<br>
Choose a directory in which to save your series and click Write Series.
<br>
Congratulations on your newly saved series!
<br>

<b>Double-click a section to bring up the quick-merge menu options:</b>
 - <b>Select all left</b> - All conflicts resolve to the left series
 - <b>Select</b> all right - All conflicts resolve to the right series
 - <b>Select</b> both contours, left atts and images - All contour conflicts choose both left and right. Attribute and image conflicts choose the left series
 - <b>Select</b> both contours, right atts and images -- All contour conflicts choose both left and right. Attribute and image conflicts choose the right series
*To select more than one file for quick-merge: select the first file, then hold shift and double-click the last file you wish to quick-merge.

