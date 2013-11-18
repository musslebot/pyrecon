#!/usr/bin/python
import argparse, re
parser = argparse.ArgumentParser(description='Renames objects in a series to match a specified series, based on overlapping sections in a specified section number')
parser.add_argument('Primary Series', metavar='pri', nargs=1, type=str, help='[string] Path to primary series')
parser.add_argument('Secondary Series', metavar='sec', nargs=1, type=str, help='[string] Path to secondary series')
parser.add_argument('Overlap Section', metavar='secNo', nargs=1, type=int, help='[integer] Section number with overlapping objects')
parser.add_argument('Rename to Series #', metavar='renameTo', nargs=1, type=int, default=1, help='[integer] Rename objects to series 1 or 2 (default: 1)')
parser.add_argument('Save Path', metavar='saveTo', nargs=1, type=str, default='./renameFRI/', help='[string] Save path for the output (default: ./renameFRI/)')
args = vars(parser.parse_args())  

from pyrecon.tools import classes, mergeTool

def main(primarySerPath, secondarySerPath, ovlpingSec, savePath='./renameFRI/'):
    # Load complete series from XML files
    series1 = classes.loadSeries(primarySerPath)
    series2 = classes.loadSeries(secondarySerPath)
    
    # Load Contours (traces/stamps/etc.) from the overlapping section (ovlpingSec) 
    conts1 = [cont for cont in series1.sections[ovlpingSec].contours]
    conts2 = [cont for cont in series2.sections[ovlpingSec].contours]
    
    # Print options
    print('Renaming ovlping objects to match: '+series1.name+' based on section: '+str(ovlpingSec))
    
    # Organize contours based on name
    ax = re.compile('a[0-9]{1,}_[a-z]{0,}$')
    axons1 = [cont for cont in conts1 if ax.match(cont.name) != None]
    axons2 = [cont for cont in conts2 if ax.match(cont.name) != None]
    print('axons1: '+str(axons1)) #===
    print('axons2: '+str(axons2)) #===
    
    dend = re.compile('d[0-9]{1,}_[a-z]{0,}$', re.IGNORECASE)
    dends1 = [cont for cont in conts1 if dend.match(cont.name) != None]
    dends2 = [cont for cont in conts2 if dend.match(cont.name) != None]
    print('dends1: '+str(dends1)) #===
    print('dends2: '+str(dends2)) #===
    
    prot = re.compile('d[0-9]{1,}p[0-9]{0,}', re.IGNORECASE)
    prots1 = [cont for cont in conts1 if prot.match(cont.name) != None]
    prots2 = [cont for cont in conts2 if prot.match(cont.name) != None]
    print('prots1: '+str(prots1)) #===
    print('prots2: '+str(prots2)) #===
    
    glia1 = []
    glia2 = []
    
    # Gather overlapping contours
    ovlpsA, ovlpsB = mergeTool.checkOverlappingContours(conts1, conts2, sameName=False) # Don't base on same name only
    print('chkOvlp:\n'+str([cont.name for cont in ovlpsA])+'\n'+str([cont.name for cont in ovlpsB]))
    
    # Separate overlapping contours into complete overlaps vs conflicting overlaps
    completeOvlps, conflictingOvlps = mergeTool.separateOverlappingContours(ovlpsA, ovlpsB, sameName=False)
    print('compOvlps:')
    for item in completeOvlps:
        print [thing.name for thing in item]
    print('confOvlps:')
    for item in conflictingOvlps:
        print [thing.name for thing in item]
    
if __name__ == '__main__':
    print ('name == __main__')
    main(args['Series 1'][0],
         args['Series 2'][0],
         args['Overlap Section'][0],
         args['Rename to Series #'][0],
         args['Save Path'][0])
