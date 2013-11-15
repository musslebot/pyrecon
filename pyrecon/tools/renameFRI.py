#!/usr/bin/python
import argparse
parser = argparse.ArgumentParser(description='Renames objects in a series to match a specified series, based on overlapping sections in a specified section number')
parser.add_argument('Series 1', metavar='s1', nargs=1, type=str, help='[string] Path to series 1')
parser.add_argument('Series 2', metavar='s2', nargs=1, type=str, help='[string] Path to series 2')
parser.add_argument('Overlap Section', metavar='secNo', nargs=1, help='[integer] Section number with overlapping objects')
parser.add_argument('Rename to Series #', metavar='renameTo', nargs=1, type=int, default=1, help='[integer] Rename objects to series 1 or 2 (default: 1)')
parser.add_argument('Save Path', metavar='saveTo', nargs=1, type=str, default='./renameFRI/', help='[string] Save path for the output (default: ./renameFRI/)')
args = vars(parser.parse_args())  
if __name__ == '__main__':
    print ('name == __main__')

from pyrecon.tools import classes, mergeTool

def main(series1Path, series2Path, ovlpingSec, renameTo=1, savePath='./renameFRI/'):
    # Load complete series from XML files
    series1 = classes.loadSeries(series1Path)
    series2 = classes.loadSeries(series2Path)
    
    # Load Contours (traces/stamps/etc.) from the overlapping section (ovlpingSec) 
    conts1 = [cont for cont in series1.sections[ovlpingSec].contours]
    conts2 = [cont for cont in series2.sections[ovlpingSec].contours]
    
    # Print options
    if renameTo == 1: namingTo = series1.name
    else: namingTo = series2.name
    print('Renaming ovlping objects to match: '+namingTo+' based on section: '+str(ovlpingSec))
    
    # Gather overlapping contours
    ovlpsA, ovlpsB = mergeTool.checkOverlappingContours(conts1, conts2, sameName=False) # Don't base on same name only
    print('chkOvlp:\n'+str(ovlpsA)+'\n'+str(ovlpsB))
    
    # Separate overlapping contours into complete overlaps vs conflicting overlaps
    completeOvlps, conflictingOvlps = mergeTool.separateOverlappingContours(ovlpsA, ovlpsB, sameName=False)
    print('sepOvlps:\n'+str(completeOvlps)+'\n'+str(conflictingOvlps))
    

