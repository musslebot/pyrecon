#!/usr/bin/python
import argparse, re
parser = argparse.ArgumentParser(description='Renames objects in a series to match a specified series, based on overlapping sections in a specified section number')
parser.add_argument('Primary Series', metavar='primary', nargs=1, type=str, help='[string] Path to primary series')
parser.add_argument('Secondary Series', metavar='secondary', nargs=1, type=str, help='[string] Path to secondary series')
parser.add_argument('Overlap Section', metavar='section', nargs=1, type=int, help='[integer] Section number with overlapping objects')
parser.add_argument('Save Path', metavar='savePath', nargs=1, type=str, default='./renameFRI/', help='[string] Save path for the output (default: ./renameFRI/)')
args = vars(parser.parse_args())  
from pyrecon.tools import classes, mergeTool

# Set up object name regex stuff



def main(primarySerPath, secondarySerPath, ovlpingSec, savePath='./renameFRI/'):
    # Load complete series from XML files
    series1 = classes.loadSeries(primarySerPath)
    series2 = classes.loadSeries(secondarySerPath)
    
    # Load Contours (traces/stamps/etc.) from the overlapping section (ovlpingSec) 
    print('Loading contours from overlapping section') #===
    conts1 = [cont for cont in series1.sections[ovlpingSec].contours]
    conts2 = [cont for cont in series2.sections[ovlpingSec].contours]
    
    # Print options
    print('Renaming ovlping objects to match: '+series1.name+' based on section: '+str(ovlpingSec))
    
    # Organize contours based on name
    
    
    
    
    prot = re.compile('d[0-9]{1,}p[0-9]{2}', re.IGNORECASE)
    print('Gathering protrusions...') #===
    prots1 = [cont for cont in conts1 if prot.match(cont.name) != None]
    prots2 = [cont for cont in conts2 if prot.match(cont.name) != None]
    print('prots1: '+str([prot.name for prot in prots1])) #===
    print('prots2: '+str([prot.name for prot in prots2])) #===
    
    # Gather overlapping contours
    print('Checking for overlapping contours...') #===
#     ovlpsA, ovlpsB = mergeTool.checkOverlappingContours(axons1, axons2, sameName=False) # Don't base on same name only
#     print('chkOvlp:\n'+str([cont.name for cont in ovlpsA])+'\n'+str([cont.name for cont in ovlpsB]))
    
    # Separate overlapping contours into complete overlaps vs conflicting overlaps
    print('Separating overlapping contours...') #===
#     completeOvlps, conflictingOvlps = mergeTool.separateOverlappingContours(ovlpsA, ovlpsB, sameName=False)
    print('compOvlps:') #===
#     for item in completeOvlps:
#         print [thing.name for thing in item]
    print('confOvlps:') #===
#     for item in conflictingOvlps:
#         print [thing.name for thing in item]

def getAxons(conts1, conts2):
    ax = re.compile('a[0-9]{1,}_[a-z]{2}$')
    print('Gathering axons...') #===
    axons1 = [cont for cont in conts1 if ax.match(cont.name) != None]
    axons2 = [cont for cont in conts2 if ax.match(cont.name) != None]
    print('axons1: '+str([ax.name for ax in axons1])) #===
    print('axons2: '+str([ax.name for ax in axons2])) #===
    return axons1, axons2

def getDendrites(conts1, conts2):
    dend = re.compile('d[0-9]{1,}_[a-z]{2}$', re.IGNORECASE)
    print('Gathering dendrites...') #===
    dends1 = [cont for cont in conts1 if dend.match(cont.name) != None]
    dends2 = [cont for cont in conts2 if dend.match(cont.name) != None]
    print('dends1: '+str([dend.name for dend in dends1])) #===
    print('dends2: '+str([dend.name for dend in dends2])) #===
    return dends1, dends2

def getProtrusions(conts1, conts2):
    prot = re.compile('d[0-9]{1,}p[0-9]{2}', re.IGNORECASE)
    print('Gathering protrusions...') #===
    prots1 = [cont for cont in conts1 if prot.match(cont.name) != None]
    prots2 = [cont for cont in conts2 if prot.match(cont.name) != None]
    print('prots1: '+str([prot.name for prot in prots1])) #===
    print('prots2: '+str([prot.name for prot in prots2])) #===
    return

if __name__ == '__main__':
    print ('name == __main__')
    main(args['Primary Series'][0],
         args['Secondary Series'][0],
         args['Overlap Section'][0],
         args['Save Path'][0])
