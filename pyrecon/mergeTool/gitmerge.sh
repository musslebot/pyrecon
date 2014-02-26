#!/bin/bash
# FOLLOW THE PYRECONSTRUCT+GIT INSTRUCTIONS IN THE MAIN README FILE

# This passes Git's temp merge files to the python mergeTool
python ${0%/*}/gitmerge.py $1 $2

exit 0 # This tells Git that the merge was a success and preps the commit
# exit -1 # This tells Git that the merge was unsuccessful
# exit <#> # This tells Git that there is/are <#> error(s) from the merge 