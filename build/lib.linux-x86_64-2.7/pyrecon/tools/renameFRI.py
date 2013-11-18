#!/usr/bin/python
import argparse, re
parser = argparse.ArgumentParser(description='Renames objects in a series to match a specified series, based on overlapping sections in a specified section number')
parser.add_argument('Primary Series', metavar='primary', nargs=1, type=str, help='[string] Path to primary series')
parser.add_argument('Secondary Series', metavar='secondary', nargs=1, type=str, help='[string] Path to secondary series')
parser.add_argument('Overlap Section', metavar='section', nargs=1, type=int, help='[integer] Section number with overlapping objects')
parser.add_argument('Save Path', metavar='savePath', nargs=1, type=str, default='./renameFRI/', help='[string] Save path for the output (default: ./renameFRI/)')
args = vars(parser.parse_args())  
from pyrecon.tools import classes, mergeTool
print(classes.__file__)
print(mergeTool.__file__)

# Set up object filters (regex and threshold)
ax = re.compile('a[0-9]{1,}_[a-z]{2}$', re.IGNORECASE)
dend = re.compile('d[0-9]{1,}_[a-z]{2}$', re.IGNORECASE)
prot = re.compile('d[0-9]{1,}p[0-9]{2}', re.IGNORECASE)
threshold=1.3

def main(primarySerPath, secondarySerPath, ovlpingSec, savePath='./renameFRI/'):
    # Load complete series from XML files
    series1 = classes.loadSeries(primarySerPath)
    series2 = classes.loadSeries(secondarySerPath)
    
    # Extract Contours (traces/stamps/etc.) from the overlapping section (ovlpingSec) 
    conts1, conts2 = getContours(series1, series2, ovlpingSec) # get sets of contours in ovlpingSec
    ax1, ax2 = getAxons(conts1, conts2) # filter axons
    den1, den2 = getDendrites(conts1, conts2) # filter dendrites
    pro1, pro2 = getProtrusions(conts1, conts2) # filter protrusions
    
    #=== ADJUST THRESHOLD FOR chkOvlpConts and sepOvlpConts
    # Check overlapping contours
    print('THRESHOLD: '+str(threshold))
    print('ovlp axons')
    a = mergeTool.checkOverlappingContours(ax1, ax2, threshold=(1.3), sameName=False)
    a = mergeTool.separateOverlappingContours(a[0], a[1], threshold=threshold, sameName=False)
    print('Complete ovlps: ')
    for group in a[0]:
        print([thing.name for thing in group])
    print('Conflict ovlps: ')
    for group in a[1]:
        print([thing.name for thing in group])
    
    print('ovlp dendrites')
    b = mergeTool.checkOverlappingContours(den1, den2, threshold=threshold, sameName=False)
    b = mergeTool.separateOverlappingContours(b[0], b[1], threshold=threshold, sameName=False)
    print('Complete ovlps: ')
    for group in b[0]:
        print([thing.name for thing in group])
    print('Conflict ovlps: ')
    for group in b[1]:
        print([thing.name for thing in group])
    
    print('ovlp prots')
    c = mergeTool.checkOverlappingContours(pro1, pro2, threshold=threshold, sameName=False)
    c = mergeTool.separateOverlappingContours(c[0], c[1], threshold=threshold, sameName=False)
    print('Complete ovlps: ')
    for group in c[0]:
        print([thing.name for thing in group])
    print('Conflict ovlps: ')
    for group in c[1]:
        print([thing.name for thing in group])
   
    # Print options
    print('Renaming ovlping objects to match primary series based on section: '+str(ovlpingSec))
    
def getContours(series1, series2, section):
    conts1 = [cont for cont in series1.sections[section].contours]
    conts2 = [cont for cont in series2.sections[section].contours]
    return conts1, conts2
    
def getAxons(conts1, conts2):
    '''Return a sorted lists of AXONS for each of 2 contours lists (filter as stated at top of file)'''
    print('Gathering axons...'),
    axons1 = sorted([cont for cont in conts1 if ax.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    axons2 = sorted([cont for cont in conts2 if ax.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    print('DONE')
    return axons1, axons2

def getDendrites(conts1, conts2):
    '''Return a sorted lists of DENDRITES for each of 2 contours lists (filter as stated at top of file)'''
    print('Gathering dendrites...'),
    dends1 = sorted([cont for cont in conts1 if dend.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    dends2 = sorted([cont for cont in conts2 if dend.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    print('DONE')
    return dends1, dends2

def getProtrusions(conts1, conts2):
    '''Return a sorted lists of PROTRUSIONS for each of 2 contours lists (filter as stated at top of file)'''
    print('Gathering protrusions...'),
    prots1 = sorted([cont for cont in conts1 if prot.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    prots2 = sorted([cont for cont in conts2 if prot.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    print('DONE')
    return prots1, prots2

if __name__ == '__main__':
    print ('name == __main__')
    main(args['Primary Series'][0],
         args['Secondary Series'][0],
         args['Overlap Section'][0],
         args['Save Path'][0])
