#!/usr/bin/python
import argparse, re
# parser = argparse.ArgumentParser(description='Renames objects in a series to match a specified series, based on overlapping sections in a specified section number')
# parser.add_argument('Primary Series', metavar='primary', nargs=1, type=str, help='[string] Path to primary series')
# parser.add_argument('Secondary Series', metavar='secondary', nargs=1, type=str, help='[string] Path to secondary series')
# parser.add_argument('Overlap Section', metavar='section', nargs=1, type=int, help='[integer] Section number with overlapping objects')
# parser.add_argument('Save Path', metavar='savePath', nargs=1, type=str, default='./renameFRI/', help='[string] Save path for the output (default: ./renameFRI/)')
# args = vars(parser.parse_args())  
from lxml import etree as ET
from pyrecon.tools import classes, mergeTool

# Set up object filters (regex and threshold)
initials = re.compile('.{0,}_[a-z]{2}$', re.IGNORECASE)
ax = re.compile('a[0-9]{1,}$$', re.IGNORECASE)
dend = re.compile('d[0-9]{1,}$', re.IGNORECASE)
cfa = re.compile('d[0-9]{1,}cfa[0-9]{1,}.{1,}$', re.IGNORECASE)
c = re.compile('d[0-9]{1,}c[0-9]{1,}.{1,}$', re.IGNORECASE)
astro = re.compile('astro', re.IGNORECASE)
threshold=(1+3**(-1))

def main(primarySerPath, secondarySerPath, ovlpingSec, savePath='./renameFRI/'):
    # Load complete series from XML files
    series1 = classes.loadSeries(primarySerPath)
    series2 = classes.loadSeries(secondarySerPath)
    
    # Remove all objects that don't end with initials
    series1 = getRidOfMess(series1) 
    series2 = getRidOfMess(series2)
    
    # filter unwanted traces
    for section in series1.sections:
        print section.name
        print [cont.name for cont in section.contours]
    for section in series2.sections:
        print section.name
        print [cont.name for cont in section.contours]
    
#     # Create new series
    newSeries = makeEmptySeries(series1) # make empty series, copy attributes from series1
    renameSer2to1(newSeries, series1, series2, ovlpingSec)
#     
#     newSeries.writeseries(savePath)
#     newSeries.writesections(savePath)

def renameSer2to1(newSeries, series1, series2, ovlpingSec):
    # Populate section[pre to ovlpingSec] with correct names
    for i in range(99,ovlpingSec+1):
        newSec = newSeries.sections[i]
        oldSec = series1.sections[i]
        newSec.contours = oldSec.contours
        newSec.imgs = oldSec.imgs
        newSec.index = oldSec.index
        newSec.thickness = oldSec.thickness
        newSec.alignLocked = oldSec.alignLocked
    
    # Get overlapping traces from ovlpingSec
    traces = extractTracesFromSec(series1, series2, ovlpingSec) # Extract desired traces from series
    matchingTraces = extractOverlapsFromTraces(traces) # find overlapping traces

    

    # Populate the rest of the lists with other traces
    for i in range(ovlpingSec,110):
        newSec = newSeries.sections[i]
        print(newSec.name)
        oldSec = series2.sections[i]
        newSec.contours = renameAxons(matchingTraces, oldSec.contours)
        newSec.imgs = oldSec.imgs
        newSec.index = oldSec.index
        newSec.thickness = oldSec.thickness
        newSec.alignLocked = oldSec.alignLocked

def renameAxons(matchingTraces, oldContours):
    renamedConts = []
    # Rename axons
    for contour in oldContours:
        for axonPair in matchingTraces[0]:
            if contour.name == axonPair[1].name: # rename secondary to primary axon
                print(contour.name+' --> '+axonPair[0].name)
                contour.name = axonPair[0].name
                break
        renamedConts.append(contour)
        print('appended: '+contour.name)
    return renamedConts
                             
def extractOverlapsFromTraces(traces):
    ovlpList = []
    for tup in traces:
        # Get overlaps
        a = checkOverlappingContours(tup[0], tup[1], threshold, sameName=False)
        a = separateOverlappingContours(a[0], a[1], threshold, False)
        pairs = a[0] # matching axon pairs
        ovlpList.append(pairs)
    return ovlpList

def extractTracesFromSec(series1, series2, ovlpingSec):
    # Extract Contours (traces/stamps/etc.) from the overlapping section (ovlpingSec) 
    conts1, conts2 = getContours(series1, series2, ovlpingSec) # get sets of contours in ovlpingSec
    
    # Extract specific traces from conts1, conts2
    ax1, ax2 = getAxons(conts1, conts2) # filter axons
    den1, den2 = getDendrites(conts1, conts2) # filter dendrites
    cfa1, cfa2 = getCFAs(conts1, conts2)
    c1, c2 = getCs(conts1, conts2)

    # make list of tuples
    return [(ax1, ax2), (den1, den2), (cfa1, cfa2), (c1, c2)]
   
def getRidOfMess(series):
    messlessSeries = makeEmptySeries(series)
    for i in range(len(messlessSeries.sections)):
        messlessSeries.sections[i].contours = [cont for cont in series.sections[i].contours if initials.match(cont.name)]
        # Remove initials
        for cont in messlessSeries.sections[i].contours:
            cont.name = cont.name[:-3]
        # Remove unwanted traces
        newContours = []
        for cont in messlessSeries.sections[i].contours:
            if (dend.match(cont.name) != None
                or ax.match(cont.name) != None
                or cfa.match(cont.name) != None
                or c.match(cont.name) != None
                or astro.match(cont.name) != None):
                newContours.append(cont)
        messlessSeries.sections[i].contours = newContours
                
    return messlessSeries

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

def getCFAs(conts1, conts2):
    print('Gathering cfas...'),
    cfa1 = sorted([cont for cont in conts1 if cfa.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    cfa2 = sorted([cont for cont in conts2 if cfa.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    print('DONE')
    return cfa1, cfa2

def getCs(conts1, conts2):
    print('Gathering cs...'),
    c1 = sorted([cont for cont in conts1 if c.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    c2 = sorted([cont for cont in conts2 if c.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    print('DONE')
    return c1, c2

def getAstros(conts1, conts2):
    print('Gathering astrocytes...'),
    astro1 = sorted([cont for cont in conts1 if astro.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    astro2 = sorted([cont for cont in conts2 if astro.match(cont.name) != None],
                    key=lambda Contour: Contour.name)
    print('DONE')
    return astro1, astro2

def checkOverlappingContours(contsA, contsB, threshold=(1+2**(-17)), sameName=False):
    '''Returns lists of mutually overlapping contours.''' 
    ovlpsA = [] # Section A contours that have overlaps in section B
    ovlpsB = [] # Section B contours that have overlaps in section A
    for contA in contsA:
        ovlpA = []
        ovlpB = []
        for contB in contsB:
            if sameName and contA.name == contB.name and contA.overlaps(contB, threshold) != 0:
                ovlpA.append(contA)
                ovlpB.append(contB)
            elif not sameName and contA.overlaps(contB, threshold) != 0:
                ovlpA.append(contA)
                ovlpB.append(contB)
        ovlpsA.extend(ovlpA)
        ovlpsB.extend(ovlpB)
    # Remove all non-unique contours from contsA and contsB
    for cont in ovlpsA:
        if cont in contsA:
            contsA.remove(cont)
    for cont in ovlpsB:
        if cont in contsB:
            contsB.remove(cont)
    return ovlpsA, ovlpsB

def separateOverlappingContours(ovlpsA, ovlpsB, threshold=(1+2**(-17)), sameName=False):
    '''Returns a list of completely overlapping pairs and a list of conflicting overlapping pairs.'''
    compOvlps = [] # list of completely overlapping contour pairs
    confOvlps = [] # list of conflicting overlapping contour pairs
    # Check for COMPLETELY overlapping contours 1st
    for contA in ovlpsA:
        for contB in ovlpsB:
            if sameName and contA.name == contB.name:
                if contA.overlaps(contB, threshold) == 1:
                    compOvlps.append([contA, contB])
            elif not sameName:
                if contA.overlaps(contB, threshold) == 1:
                    if [contA, contB] not in compOvlps:
                        compOvlps.append([contA, contB])
    # Check for CONFLICTING overlapping contours
    for contA in ovlpsA:
        for contB in ovlpsB:
            if sameName and contA.name == contB.name:
                overlap = contA.overlaps(contB, threshold)
                if overlap != 0 and overlap != 1:
                    confOvlps.append([contA, contB])
            elif not sameName:
                overlap = contA.overlaps(contB, threshold)
                if overlap != 0 and overlap != 1:
                    confOvlps.append([contA, contB])
    return compOvlps, confOvlps

def makeEmptySeries(primarySeries):
    # Create .ser file based on primarySeries
    mergedSeries = classes.Series( root=ET.Element('Series',primarySeries.output()[0]), name=primarySeries.name )
    mergedSeries.contours = primarySeries.contours # Copy over primarySeries' Contours and ZContours
    
    # Create element tree Section element
    for section in primarySeries.sections:
        elem = ET.Element('Section')
        for att in section.output():
            elem.set(str(att), section.output()[att])
        else:
            name = mergedSeries.name+'.'+str(section.index)
        sec3 = classes.Section(elem, name)
        mergedSeries.sections.append(sec3)
    return mergedSeries

def mergeAxons(mAxons):
    checkMatches(mAxons)
    return

def mergeDendrites(mDendrites):
    checkMatches(mDendrites)
    return

def mergeCFAs(mCFAs):
    checkMatches(mCFAs)
    return

def mergeCs(mCs):
    checkMatches(mCs)
    return

def checkMatches(matchList):
    print('The following objects will be matched: ')
    for a,b in matchList:
        print a.name+' == '+b.name
    ans = raw_input('Is this okay (y/n)? ')
    if str(ans) == 'y':
        print('Okay')
        print
    else:
        print('Aborting...')
        quit()

# if __name__ == '__main__':
#     main(args['Primary Series'][0],
#          args['Secondary Series'][0],
#          args['Overlap Section'][0],
#          args['Save Path'][0])
