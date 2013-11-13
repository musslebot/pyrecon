# Merges and renames a single series if:
#   Top half of series and bottom half are worked on by different people
#   Section between them has been worked on by both people

from pyrecon.tools import classes, mergeTool

# load overlapping section
# check for overlaps
# output list of names to be changed
# change names