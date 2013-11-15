'''Merge two series together'''
import sys, os, re
from pyrecon.tools.classes import loadSeries, Series, Section
from lxml import etree as ET
 
if len(sys.argv) >= 3:
    ser = os.path.basename( sys.argv[1] ) # Name of series
    ser2 = os.path.basename( sys.argv[2] ) 
    inpath = os.path.abspath( os.path.dirname(sys.argv[1]) )+'/' # Directory of series
    inpath2 = os.path.abspath( os.path.dirname(sys.argv[2]) )+'/'
    if len(sys.argv) == 4:
        mergeoutpath = os.path.abspath(sys.argv[3])+'/merged/' #===
    else:
        mergeoutpath = os.path.dirname( os.path.dirname(inpath) )+'/merged/' #===

def main():
    if __name__ != '__main__':
        print('Welcome to reconstructmergetool')
        return
    if len(sys.argv) > 1:
        #1)Create series object
        series = loadSeries( inpath+ser )
        series2 = loadSeries( inpath2+ser2 )
        
        #2)Merge series attributes
        mergeSer = mergeSeries( series, series2 )
        mergeSer.sections = mergeAllSections( series, series2 )

        #4)Output .ser file
        mergeSer.writeseries( mergeoutpath )
        
        #5)Output section file(s)
        mergeSer.writesections( mergeoutpath )

def serAttHandler(ser1atts, ser2atts, ser3atts, conflicts):
    '''Resolves conflicts regarding series attributes'''
    for conflict in conflicts:
        print('\nSeries attributes do not match: '+str(conflict))
        print('1: '+ser1atts[conflict]+'\n'+'2: '+ser2atts[conflict])
        a = 3
        while a not in [1,2]:
            a = int(raw_input('Choose attribute to pass to output series... 1 or 2: '))
            if a == 1:
                ser3atts[conflict] = ser1atts[conflict]
            elif a == 2:
                ser3atts[conflict] = ser2atts[conflict]
            else:
                print('Invalid choice. Please enter 1 or 2')
    return ser3atts
    
def serContHandler(ser1conts, ser2conts, ser3conts):
    # add leftover, unique zcontours to ser3conts
    ser3conts.extend(ser1conts)
    ser3conts.extend(ser2conts)
    while len(ser3conts) > 20:
        print('Current length: '+str(len(ser3conts)))
        a = raw_input('Too many series contours to output, enter index of contour to delete\n'\
                      +str([cont.name for cont in ser3conts]))
        ser3conts.pop( int(a) )
        print('\n')
    return ser3conts

def serZContHandler(ser1zconts, ser2zconts, ser3zconts ):
    # add leftover, unique zcontours to ser3zconts
    ser3zconts.extend(ser1zconts)
    ser3zconts.extend(ser2zconts)
    return ser3zconts

def secAttHandler(s1atts, s2atts, comparison):
    mergedAttributes = {}
    for att in comparison:
        if not comparison[att]:
            a = raw_input('CONFLICT: mergeSecAtts')
            if a == 1:
                mergedAttributes[att] = s1atts[att]
            else:
                mergedAttributes[att] = s2atts[att]
        else:
            mergedAttributes[att] = s1atts[att]
    return mergedAttributes

def secImgHandler(s1,s2):
    s3imgs = []
    print('1: '+str(s1.imgs[0].output()))
    print('2: '+str(s2.imgs[0].output()))
    a='hello'
    while str(a) not in ['1','2']:
        a = raw_input('Enter image to use in merged series: ')
        if str(a).lower() == '1':
            s3imgs = s1.imgs
        elif str(a).lower() == '2':
            s3imgs = s2.imgs
    return s3imgs

def secContHandler(uniqueA, compOvlp, confOvlp, uniqueB):
    '''Returns list of contours to be added to merged series'''
    outputContours = []
    
    # Add unique contours to output
    outputContours.extend(uniqueA)
    outputContours.extend(uniqueB)
    
    # Add a single copy of compOvlp pair to output
    for pair in compOvlp:
        outputContours.append(pair[0])
    
    # Handle conflicting overlaps
    for pair in confOvlp:
        print('Conflicting contour overlap')
        print(pair[0])
        print(pair[1])
        sel = raw_input('Please enter 1, 2, or both to select what to output: ')
        if sel == '1':
            outputContours.append(pair[0])
        elif sel == '2':
            outputContours.append(pair[1])
        else:
            outputContours.append(pair[0])
            outputContours.append(pair[1])
    return outputContours

def mergeSeries(serObj1, serObj2, name=None, \
                mergeSerAttfxn = serAttHandler, \
                mergeSerContfxn = serContHandler, \
                mergeSerZContfxn = serZContHandler):
    '''Returns a merged series object as defined by the mergefxn parameters. The <Series>.sections will \
    be empty and must be populated with a mergeSections function'''
    
    print('Merging series objects...'),
    if not name:
        name = serObj1.name
    
    # Create merged parts    
    mergedAtts = mergeSeriesAttributes( serObj1, serObj2, handler=mergeSerAttfxn)
    mergedConts = mergeSeriesContours( serObj1.contours, serObj2.contours, handler=mergeSerContfxn)
    mergedZConts = mergeSeriesZContours( serObj1.contours, serObj2.contours, handler=mergeSerZContfxn)
    mergedSeries = Series( root=ET.Element('Series',mergedAtts), name=name ) # Create series w/ merged atts
    mergedSeries.contours = list(mergedConts+mergedZConts) # Append merged Contours/ZContours
    print('DONE')
    
    return mergedSeries
    
def mergeSeriesAttributes(serObj1, serObj2, handler=serAttHandler ):
    '''Merges the attributes from two series. Conflicts handled with handler parameter.
    Attributes are returned in the form of a dictionary.'''
    # Compare and merge series attributes from ser1Obj/ser2Obj
    # Handle conflict independently
    ser1atts = serObj1.output()[0]
    ser2atts = serObj2.output()[0]
    ser3atts = {}
    conflicts = {}
    for att in ser1atts:
        # If the same -> merge to ser3atts...
        if ser1atts[att] == ser2atts[att]:
            ser3atts[att] = ser1atts[att]
        # ...otherwise, add to conflicts dictionary
        else:
            conflicts[att] = True
    return handler(ser1atts, ser2atts, ser3atts, conflicts)

def mergeSeriesContours(ser1conts, ser2conts, handler=serContHandler):
    '''Merges the contours from two series. Conflicts handled with handler parameter.
    Contours returned in the form of a list.'''
    ser1conts = [cont for cont in ser1conts if cont.tag == 'Contour']
    ser2conts = [cont for cont in ser2conts if cont.tag == 'Contour']
    ser3conts = []
    for elem in ser1conts:
        for elem2 in ser2conts:
            if elem == elem2: # Merge same contours
                ser3conts.append( elem )
                ser1conts.remove( elem )
                ser2conts.remove( elem2 )
    return handler(ser1conts, ser2conts, ser3conts)
    
def mergeSeriesZContours(ser1conts, ser2conts, threshold=(1+2**(-17)), handler=serZContHandler):
    ser1zconts = [cont for cont in ser1conts if cont.tag == 'ZContour']
    ser2zconts = [cont for cont in ser2conts if cont.tag == 'ZContour']
    ser3zconts = []
    for elem in ser1zconts:
        for elem2 in ser2zconts:
            if elem.name == elem2.name and elem.overlaps(elem2, threshold):
                ser3zconts.append( elem ) 
                ser1zconts.remove( elem )
                ser2zconts.remove( elem2 )
    return handler(ser1zconts, ser2zconts, ser3zconts)

def mergeAllSections(serObj1, serObj2, name=None, \
                     secAttfxn = secAttHandler, \
                     secImgfxn = secImgHandler, \
                     secContfxn = secContHandler, \
                     attOverride = None, \
                     imageOverride = None, \
                     contOverride = None):
    '''Takes in two series, returns list of merged sections'''
    print('Merging Sections...')
    # Create list of parallel section pairs (paired by section name)
    pairlist = [(x,y) for x in serObj1.sections for y in serObj2.sections if x.index == y.index]
     
    # Merge sections
    mergedSections = []
    for (x,y) in pairlist:
        print(x.name+' '+y.name)
        mergedSections.append( mergeSection(x,y, name, \
                                            secAttfxn = secAttfxn, \
                                            secImgfxn = secImgfxn, \
                                            secContfxn = secContfxn, \
                                            attOverride = attOverride, \
                                            imageOverride = imageOverride, \
                                            contOverride = contOverride) )
    print('...DONE')
    return mergedSections

def mergeSection(sec1, sec2, name=None, \
                 secAttfxn = secAttHandler, \
                 secImgfxn = secImgHandler, \
                 secContfxn = secContHandler, \
                 attOverride = None, \
                 imageOverride = None, \
                 contOverride = None):
    '''Takes in two sections, returns a 3rd merged section'''
    # create section w/ merged attributes
    if attOverride != None:
        if int(attOverride) == 1:
            sec3 = mergeSectionAttributes(sec1, sec1, name, handler=secAttfxn)
        elif int(attOverride) == 2:
            sec3 = mergeSectionAttributes(sec2, sec2, name, handler=secAttfxn)
    else:
        sec3 = mergeSectionAttributes( sec1, sec2, name, handler=secAttfxn )
    
    # check section images
    if imageOverride != None:
        if int(imageOverride) == 1:
            sec3.imgs = sec1.imgs
        elif int(imageOverride) == 2:
            sec3.imgs = sec2.imgs
        elif int(imageOverride) == 3:
            sec3.imgs = (sec1.imgs).extend(sec2.imgs)
    else:
        sec3.imgs = mergeSectionImgs( sec1, sec2, handler=secImgfxn )
    
    # merge section contours
    if contOverride != None:
        if int(contOverride) == 1:
            sec3.contours = sec1.contours
        elif int(contOverride) == 2:
            sec3.contours = sec2.contours
        elif int(contOverride) == 3:
            sec3.contours = (sec1.contours).extend(sec2.contours)
    else:
        sec3.contours = mergeSectionContours( sec1, sec2, handler=secContfxn )
    return sec3

def checkSectionAttributes(sec1, sec2):
    '''Returns dictionary of True/False for each attribute,
    describing if they are the same between both sections'''
    chkDict = {}
    # chk attributes
    s1atts = sec1.output()
    s2atts = sec2.output()
    for att in s1atts:
        chkDict[att] = (s1atts[att] == s2atts[att])
    return chkDict

def mergeSectionAttributes(sec1, sec2, name=None, handler=secAttHandler):
    '''Takes in two sections and a chkDict from chkSecAtts,
    returns merged section attributes (non-Contour/images)'''
    comparisonDict = checkSectionAttributes(sec1, sec2)
    mergedAttributes = handler( sec1.output(), sec2.output(), comparisonDict )
    
    # Create element tree Section element
    elem = ET.Element('Section')
    for att in mergedAttributes:
        elem.set(str(att), mergedAttributes[att])
    if not name: #=== sec1 name?
        name = sec1.name
    else:
        name = name+'.'+str(sec1.index)
    sec3 = Section(elem, name)
    return sec3

def mergeSectionImgs(s1, s2, handler=secImgHandler):
    '''Returns imgs to be addeded to new section'''
    if s1.imgs[0] != s2.imgs[0]:
        return handler(s1,s2)
    # If all the same, just copy 1st series' images
    return s1.imgs

def checkOverlappingContours(contsA, contsB, threshold=(1+2**(-17)), sameName=True):
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

def separateOverlappingContours(ovlpsA, ovlpsB, threshold=(1+2**(-17)), sameName=True):
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

def mergeSectionContours(sA,sB, handler=secContHandler): #===
    '''Returns merged contours between two sections'''
    # Populate shapely shapes
    sA.popshapes()
    sB.popshapes()
    
    # Copy contour lists for both sections; these lists are altered
    contsA = [cont for cont in sA.contours]
    contsB = [cont for cont in sB.contours]
    
    # Find overlapping contours
    ovlpsA, ovlpsB = checkOverlappingContours(contsA, contsB)
    
    # Separate into completely overlapping or incompletely overlapping
    compOvlp, confOvlp = separateOverlappingContours(ovlpsA, ovlpsB) #===

    # Identify unique contours
    uniqueA, uniqueB = contsA, contsB
    
    # Handle conflicts
    mergedConts = handler(uniqueA, compOvlp, confOvlp, uniqueB)
    
    return mergedConts
    

def bethBellMerge(path_FPNCT_BB, path_FPNCT_JNB): #===
    # First load FPNCT_BB and delete everything except those in saveList
    saveList = [re.compile('[d][0-9]{0,2}vftz[0-9]{0,2}[a-z]?$', re.I), # d##vftz##_
                re.compile('[d][0-9]{0,2}vftzcfa[0-9]{0,2}[a-z]?$', re.I), # d##vftzcfa##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}[a-z]?$', re.I), # d##ax##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dcv[0-9]{0,2}[a-z]?$', re.I), # d##ax##dcv##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dssvdh[0-9]{0,2}[a-z]?$', re.I), # d##ax##dssvdh##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dssvrh[0-0]{0,2}[a-z]?$', re.I), # d##ax##dssvrh##_
                re.compile('[d][0-9]{0,2}ax[0-9]{0,2}dssvrhclose[0-9]{0,2}[a-z]?$', re.I), # d##ax##dssvrhclose##_
                re.compile('[d][0-9]{0,2}c[0-9]{0,2}[a-z]?$', re.I), # d##c##_
                re.compile('[d][0-9]{0,2}c[0-9]{0,2}scale[0-9]{0,2}[a-z]?$', re.I), # d##c##scale##_
                re.compile('[d][0-9]{0,2}cfa[0-9]{0,2}[a-z]?$', re.I)] # d##cfa##_
    ser1 = loadSeries(path_FPNCT_BB)
    for section in ser1.sections:
        savedContours = []
        for contour in section.contours:
            for prog in saveList:
                if len(prog.findall(contour.name)) != 0:
                    savedContours.append(contour)
                    break
        section.contours = savedContours
    
    # Now load FPNCT_JNB and delete everything in delList
    delList = [re.compile('[d][0-9]{0,2}c[0-9]{0,2}[a-z]?$', re.I), # d##c##_
               re.compile('[d][0-9]{0,2}cfa[0-9]{0,2}[a-z]?$', re.I)] # d##cfa##_
    
    ser2 = loadSeries(path_FPNCT_JNB)
    for section in ser2.sections:
        deletedContours = []
        for contour in section.contours:
            for prog in delList:
                if len(prog.findall(contour.name)) != 0:
                    deletedContours.append(contour.name)
                    break
        section.contours = [cont for cont in section.contours if cont.name not in deletedContours]
    
    ser3 = mergeSeries(ser1, ser2, name='FPNCT_merge')
    # imageOverride set to 2; imageOverride 1 has different image and domain1 transforms
    ser3.sections = mergeAllSections(ser1, ser2, name='FPNCT_merge', imageOverride=2)
    
    # OUTPUT
    ser3.writeseries('/home/michaelm/Documents/Test Series/bb/FPNCT_merge/')
    ser3.writesections('/home/michaelm/Documents/Test Series/bb/FPNCT_merge/')
    
class mergeObject:
    '''Abstract class to easily change functions for reconstructmergetool.py'''
    def __init__(self):
        
        # META STUFF
        self.name = 'newSeries'
        self.outputPath = os.getcwd()+'/'+str(self.name)+'/'
        
        # SERIES MERGE FUNCTIONS
        self.handleSerAtts = serAttHandler
        self.handleSerConts = serContHandler
        self.handleSerZConts = serZContHandler
        
        # SECTION MERGE FUNCTIONS
        self.handleSecAtts = secAttHandler
        self.handleSecImgs = secImgHandler
        self.handleSecConts = secContHandler

# Fxns
    def merge(self, path_to_series1, path_to_series2):
        '''Merges two series together based on mergeObjects' attributes'''
        s1 = loadSeries(path_to_series1)
        s2 = loadSeries(path_to_series2)

        mergedSeries = mergeSeries( s1, s2, name = self.name, \
                                mergeSerAttfxn = self.handleSerAtts, \
                                mergeSerContfxn = self.handleSerConts, \
                                mergeSerZContfxn = self.handleSerZConts  )
        
        mergedSeries.sections = mergeAllSections( s1, s2, self.name, \
                                              secAttfxn = self.handleSecAtts, \
                                              secImgfxn = self.handleSecImgs, \
                                              secContfxn = self.handleSecConts)
        mergedSeries.writeseries( self.outputPath )
        mergedSeries.writesections( self.outputPath )
        
# Setters
    def setName(self, string):
        self.name = str(string)
        self.outputPath = os.getcwd()+'/'+str(self.name)+'/'
        print('Merged series name changed to: '+self.name)
        print
        
    def setOutpath(self, string):
        self.outputPath = str(string)
        print('New output path set: '+self.outputPath)
        print
        
    def setSerAttfxn(self, fxn):
        self.handleSerAtts = fxn
        print('New series attribute handler set')
        print
        
    def setSerContfxn(self, fxn):
        self.handleSerConts = fxn
        print('New series contour handler set')
        
    def setSerZContfxn(self, fxn):
        self.handleSerZConts = fxn
        print('New series zcontour handler set')
        
    def setSecAttfxn(self, fxn):
        self.handleSecAtts = fxn
        print('New section attribute handler set')
        print
        
    def setSecImgfxn(self, fxn):
        self.handleSecImgs = fxn
        print('New section image handler set')
        print
        
    def setSecContfxn(self, fxn):
        self.handleSecConts = fxn
        print('New section contour handler set')
        print
    def current(self):
        print('CURRENT MERGEOBJECT SETTINGS:')
        print('Name: '+str(self.name))
        print('Outpath: '+str(self.outputPath))
        print
        print('Series Attribute Handler: '+str(self.handleSerAtts))
        print('Series Contour Handler: '+str(self.handleSerConts))
        print('Series ZContour Handler: '+str(self.handleSerZConts))
        print
        print('Section Attribute Handler: '+str(self.handleSecAtts))
        print('Section Image Handler: '+str(self.handleSecImgs))
        print('Section Contour Handler: '+str(self.handleSecConts))
main()

