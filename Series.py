from Contour import *
from ZContour import *
from Section import *
from rObject import *
from lxml import etree as ET
import numpy as np
import os, re
# Recent changes: popgridSize int -> float
class Series:
# Python functions
    # INITIALIZE
    def __init__(self, root=None, name='No Name'):
        self.name = name
        self.tag = 'Series'
        
        self.contours = self.popcontours(root)
        self.sections = [] #Sorted in reconstructmergetool.getsections()
        
        self.index = self.popindex(root)
        self.viewport = self.popviewport(root)
        self.units = self.popunits(root)
        self.autoSaveSeries = self.s2b(self.popautoSaveSeries(root))
        self.autoSaveSection =  self.s2b(self.popautoSaveSection(root))
        self.warnSaveSection = self.s2b(self.popwarnSaveSection(root))
        self.beepDeleting = self.s2b(self.popbeepDeleting(root))
        self.beepPaging = self.s2b(self.popbeepPaging(root))
        self.hideTraces = self.s2b(self.pophideTraces(root))
        self.unhideTraces = self.s2b(self.popunhideTraces(root))
        self.hideDomains = self.s2b(self.pophideDomains(root))
        self.unhideDomains = self.s2b(self.popunhideDomains(root))
        self.useAbsolutePaths = self.s2b(self.popuseAbsolutePaths(root))
        self.defaultThickness = self.popdefaultThickness(root) #float
        self.zMidSection = self.s2b(self.popzMidSection(root))
        self.thumbWidth = self.popthumbWidth(root) #int
        self.thumbHeight = self.popthumbHeight(root) #int
        self.fitThumbSections = self.s2b(self.popfitThumbSections(root))
        self.firstThumbSection = self.popfirstThumbSection(root) #int
        self.lastThumbSection = self.poplastThumbSection(root) #int
        self.skipSections = self.popskipSections(root) #int
        self.displayThumbContours = self.s2b(self.popdisplayThumbContours(root))
        self.useFlipbookStyle = self.s2b(self.popuseFlipbookStyle(root))
        self.flipRate = self.popflipRate(root) #int
        self.useProxies = self.s2b(self.popuseProxies(root))
        self.widthUseProxies = self.popwidthUseProxies(root) #int
        self.heightUseProxies = self.popheightUseProxies(root) #int
        self.scaleProxies = self.popscaleProxies(root) #float
        self.significantDigits = self.popsignificantDigits(root) #int
        self.defaultBorder = self.popdefborder(root)
        self.defaultFill = self.popdeffill(root)
        self.defaultMode = self.popdefaultMode(root) #int
        self.defaultName = self.popdefaultName(root)
        self.defaultComment = self.popdefaultComment(root)
        self.listSectionThickness = self.s2b(self.poplistSectionThickness(root))
        self.listDomainSource = self.s2b(self.poplistDomainSource(root))
        self.listDomainPixelsize = self.s2b(self.poplistDomainPixelsize(root))
        self.listDomainLength = self.s2b(self.poplistDomainLength(root))
        self.listDomainArea = self.s2b(self.poplistDomainArea(root))
        self.listDomainMidpoint = self.s2b(self.poplistDomainMidpoint(root))
        self.listTraceComment = self.s2b(self.poplistTraceComment(root))
        self.listTraceLength = self.s2b(self.poplistTraceLength(root))
        self.listTraceArea = self.s2b(self.poplistTraceArea(root))
        self.listTraceCentroid = self.s2b(self.poplistTraceCentroid(root))
        self.listTraceExtent = self.s2b(self.poplistTraceExtent(root))
        self.listTraceZ = self.s2b(self.poplistTraceZ(root))
        self.listTraceThickness = self.s2b(self.poplistTraceThickness(root))
        self.listObjectRange = self.s2b(self.poplistObjectRange(root))
        self.listObjectCount = self.s2b(self.poplistObjectCount(root))
        self.listObjectSurfarea = self.s2b(self.poplistObjectSurfarea(root))
        self.listObjectFlatarea = self.s2b(self.poplistObjectFlatarea(root))
        self.listObjectVolume = self.s2b(self.poplistObjectVolume(root))
        self.listZTraceNote = self.s2b(self.poplistZTraceNote(root))
        self.listZTraceRange = self.s2b(self.poplistZTraceRange(root))
        self.listZTraceLength = self.s2b(self.poplistZTraceLength(root))
        self.borderColors = self.popbordcolors(root)
        self.fillColors = self.popfillcolors(root)
        self.offset3D = self.popoffset3D(root)
        self.type3Dobject = self.poptype3Dobject(root) #int
        self.first3Dsection = self.popfirst3Dsection(root) #int
        self.last3Dsection = self.poplast3Dsection(root) #int
        self.max3Dconnection = self.popmax3Dconnection(root) #int
        self.upper3Dfaces = self.s2b(self.popupper3Dfaces(root))
        self.lower3Dfaces = self.s2b(self.poplower3Dfaces(root))
        self.faceNormals = self.s2b(self.popfaceNormals(root))
        self.vertexNormals = self.s2b(self.popvertexNormals(root))
        self.facets3D = self.popfacets3D(root) #int
        self.dim3D = self.popdim3D(root)
        self.gridType = self.popgridType(root) #int
        self.gridSize = self.popgridsize(root)
        self.gridDistance = self.popgriddistance(root)
        self.gridNumber = self.popgridnumber(root)
        self.hueStopWhen = self.pophueStopWhen(root) #int
        self.hueStopValue = self.pophueStopValue(root) #int
        self.satStopWhen = self.popsatStopWhen(root) #int
        self.satStopValue = self.popsatStopValue(root) #int
        self.brightStopWhen = self.popbrightStopWhen(root) #int
        self.brightStopValue = self.popbrightStopValue(root) #int
        self.tracesStopWhen = self.s2b(self.poptracesStopWhen(root))
        self.areaStopPercent = self.popareaStopPercent(root) #int
        self.areaStopSize = self.popareaStopSize(root) #int
        self.ContourMaskWidth = self.popContourMaskWidth(root) #int
        self.smoothingLength = self.popsmoothingLength(root) #int
        self.mvmtIncrement = self.popmvmtincrement(root)
        self.ctrlIncrement = self.popctrlincrement(root)
        self.shiftIncrement = self.popshiftincrement(root)
        # Private
        # List of all attributes, used for creating an attribute dictionary for output (see output(self))
        self._attribs = ['index', 'viewport', 'units', 'autoSaveSeries', \
                         'autoSaveSection', 'warnSaveSection', 'beepDeleting', 'beepPaging', \
                         'hideTraces', 'unhideTraces', 'hideDomains', 'unhideDomains', 'useAbsolutePaths', \
                         'defaultThickness', 'zMidSection', 'thumbWidth', 'thumbHeight', 'fitThumbSections', \
                         'firstThumbSection', 'lastThumbSection', 'skipSections', 'displayThumbContours', \
                         'useFlipbookStyle', 'flipRate', 'useProxies', 'widthUseProxies', 'heightUseProxies', \
                         'scaleProxies', 'significantDigits', 'defaultBorder', 'defaultFill', 'defaultMode', \
                         'defaultName', 'defaultComment', 'listSectionThickness', 'listDomainSource', \
                         'listDomainPixelsize', 'listDomainLength', 'listDomainArea', 'listDomainMidpoint', \
                         'listTraceComment', 'listTraceLength', 'listTraceArea', 'listTraceCentroid', \
                         'listTraceExtent', 'listTraceZ', 'listTraceThickness', 'listObjectRange', \
                         'listObjectCount', 'listObjectSurfarea', 'listObjectFlatarea', 'listObjectVolume', \
                         'listZTraceNote', 'listZTraceRange', 'listZTraceLength', 'borderColors', 'fillColors', \
                         'offset3D', 'type3Dobject', 'first3Dsection', 'last3Dsection', 'max3Dconnection', \
                         'upper3Dfaces', 'lower3Dfaces', 'faceNormals', 'vertexNormals', 'facets3D', 'dim3D', \
                         'gridType', 'gridSize', 'gridDistance', 'gridNumber', 'hueStopWhen', 'hueStopValue', \
                         'satStopWhen', 'satStopValue', 'brightStopWhen', 'brightStopValue', 'tracesStopWhen', \
                         'areaStopPercent', 'areaStopSize', 'ContourMaskWidth', 'smoothingLength', \
                         'mvmtIncrement', 'ctrlIncrement', 'shiftIncrement']
    # Allows indexing of section object
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self._list[x]
    # print(<Section>) output
    def __str__(self):
        '''Allows use of print(<Series>) function.'''
        return 'Name: %s\nTag: %s' %(self.name,self.tag)
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        return self.output()[0] == other.output()[0] and self.output()[1] == other.output()[1]
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return self.output()[0] != other.output()[0] and self.output()[1] != other.output()[1]
# Accessors
    def getObjectHierarchy(self, dendrites, protrusions, traces, others): #=== others not implemented
        '''Returns a single hierarchical dictionary with data for each object not in others list'''
        hierarchy = {}
        # Combine lists into a hierarchical dictionary
        for dendrite in dendrites:
            # 1) Create rObject for dendrite
            denObj = rObject(name=dendrite, series=self, tag='dendrite')

            # 2) Load protrusions into dendrite rObjs
            protList = [prot for prot in protrusions if prot[0:3] == dendrite]
            for prot in protList:
                # 1) Create rObject for protrusions
                protObj = rObject(name=prot, series=self, tag='protrusion')
                
                # 2) Load traces into protrusion rObjs
                traceList = [trace for trace in traces if prot[-2:len(prot)] in trace[3:] and prot[0:3] in trace[0:3]]
                for trace in traceList:
                    # 1) Create rObject for traces
                    traceObj = rObject(name=trace, series=self, tag='trace')
                    
                    # Add children to parent rObjs
                    protObj.children.append(traceObj)
                denObj.children.append(protObj)
            hierarchy[dendrite] = denObj
            
        return hierarchy
    
    def getObjectLists(self):
        '''Returns lists of dendrite names, protrusion names, trace names, and a list of other objects in series'''
        dendrite_expression = 'd[0-9]{2}$' # represents base dendrite name (d##)
        protrusion_expression = 'd[0-9]{2}p[0-9]{2}$' # represents base protrusion name (d##p##)
        trace_expression = 'd[0-9]{2}[a-z]{1,6}' # represents trace name (d##
        
        # Convert expressions to usable regular expressions
        dendrite_expression = re.compile(dendrite_expression)
        protrusion_expression = re.compile(protrusion_expression, re.I)
        trace_expression = re.compile(trace_expression, re.I)
        
        # Create lists for names of dendrites, protrusions, traces, and other objects
        dendrites = []
        protrusions = []
        traces = []
        others = []
        for section in self.sections:
            for contour in section.contours:
                # Dendrite
                if dendrite_expression.match(contour.name) != None:
                    dendrites.append(contour.name)
                # Protrusion
                elif protrusion_expression.match(contour.name) != None:
                    protrusions.append(contour.name)
                # Trace
                elif trace_expression.match(contour.name) != None:
                    traces.append(contour.name)
                # Everything else
                else:
                    others.append(contour.name)
        return list(set(dendrites)), list(set(protrusions)), list(set(traces)), list(set(others))

    def output(self):
        '''Returns a dictionary of attributes and a list of contours for building .ser xml file'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for value in values:
            attributes[keys[count]] = value
            count += 1
        return attributes, self.contours
    def getVolume(self, object_name):
        '''Returns volume of the object throughout the series. Volume calculated by summing the value obtained by
        multiplying the area by section thickness over all sections.'''
        vol = 0
        for section in self.sections:
            for contour in section.contours:
                if contour.name == object_name:
                    contour.popshape()
                    vol += (contour._shape.area * section.thickness)
        return vol
    def getTotalVolume(self, object_name):
        related_objects = []
        if object_name[-1].isalpha():
            object_name = object_name[:-1]
            # Get all related objects by base object name
            for section in self.sections:
                for contour in section.contours:
                    if object_name in contour.name:
                        related_objects.append(contour.name)
        # Find total volume by summing volume for all related objects
        totVol = 0
        for obj in list(set(related_objects)):
            totVol+=self.getVolume(obj)
        return totVol
    def getSurfaceArea(self, object_name):
        '''Returns surface area of the object throughout the series. Surface area calculated by summing
        the length multiplied by section thickness across sections.'''
        sArea = 0
        for section in self.sections:
            for contour in section.contours:
                if contour.name == object_name:
                    sArea += (contour.getLength() * section.thickness)
        return sArea
    def getFlatArea(self, object_name):
        '''Returns the flat area of the object throughout the series. Flat area calculated by summing the area of
        the object across all sections.'''
        fArea = 0
        for section in self.sections:
            for contour in section.contours:
                if contour.name == object_name:
                    contour.popshape()
                    if contour.closed:
                        fArea += contour._shape.area
                    else:
                        fArea += (contour.getLength() * section.thickness)
        return fArea
    def getStartEndCount(self, object_name):
        '''Returns a tuple containing the start index, end index, and count of the item in series.'''
        start = 0
        end = 0
        count = 0
        # Count
        for section in self.sections:
            for contour in section.contours:
                if contour.name == object_name:
                    count += 1
            # Start/End
            if object_name in [cont.name for cont in section.contours]:
                # Start index
                if start == 0:
                    start = section.index
                # End index
                end = section.index
        return start, end, count
    def xgetattribs(self):
        '''Returns attributes in appropriate format for xml output'''
        return (str(self.index), str(self.getviewport()), str(self.units), str(self.autoSaveSeries).lower(), \
        str(self.autoSaveSection).lower(), str(self.warnSaveSection).lower(), str(self.beepDeleting).lower(), str(self.beepPaging).lower(), \
        str(self.hideTraces).lower(), str(self.unhideTraces).lower(), str(self.hideDomains).lower(), str(self.unhideDomains).lower(), str(self.useAbsolutePaths).lower(), \
        str(self.defaultThickness), str(self.zMidSection).lower(), str(self.thumbWidth), str(self.thumbHeight), str(self.fitThumbSections).lower(), \
        str(self.firstThumbSection), str(self.lastThumbSection), str(self.skipSections), str(self.displayThumbContours).lower(), \
        str(self.useFlipbookStyle).lower(), str(self.flipRate), str(self.useProxies).lower(), str(self.widthUseProxies), str(self.heightUseProxies), \
        str(self.scaleProxies), str(self.significantDigits), str(self.getdefaultborder()), str(self.getdefaultfill()), str(self.defaultMode), \
        str(self.defaultName), str(self.defaultComment), str(self.listSectionThickness).lower(), str(self.listDomainSource).lower(), \
        str(self.listDomainPixelsize).lower(), str(self.listDomainLength).lower(), str(self.listDomainArea).lower(), str(self.listDomainMidpoint).lower(), \
        str(self.listTraceComment).lower(), str(self.listTraceLength).lower(), str(self.listTraceArea).lower(), str(self.listTraceCentroid).lower(), \
        str(self.listTraceExtent).lower(), str(self.listTraceZ).lower(), str(self.listTraceThickness).lower(), str(self.listObjectRange).lower(), \
        str(self.listObjectCount).lower(), str(self.listObjectSurfarea).lower(), str(self.listObjectFlatarea).lower(), str(self.listObjectVolume).lower(), \
        str(self.listZTraceNote).lower(), str(self.listZTraceRange).lower(), str(self.listZTraceLength).lower(), str(self.getbordercolors()), str(self.getfillcolors()), \
        str(self.getoffset3d()), str(self.type3Dobject), str(self.first3Dsection), str(self.last3Dsection), str(self.max3Dconnection), \
        str(self.upper3Dfaces).lower(), str(self.lower3Dfaces).lower(), str(self.faceNormals).lower(), str(self.vertexNormals).lower(), str(self.facets3D), str(self.getdim3d()), \
        str(self.gridType), str(self.getgridsize()), str(self.getgriddistance()), str(self.getgridnumber()), str(self.hueStopWhen), str(self.hueStopValue), \
        str(self.satStopWhen), str(self.satStopValue), str(self.brightStopWhen), str(self.brightStopValue), str(self.tracesStopWhen).lower(), \
        str(self.areaStopPercent), str(self.areaStopSize), str(self.ContourMaskWidth), str(self.smoothingLength), \
        str(self.getmvmntinc()), str(self.getctrlinc()), str(self.getshiftinc()))
    def getviewport(self):
        ret = ''
        for elem in self.viewport:
            ret += str(elem)+' '
        return ret.rstrip()
    def getdim3d(self):
        ret = ''
        for elem in self.dim3D:
            ret += str(elem)+' '
        return ret.rstrip()
    def getoffset3d(self):
        ret = ''
        for elem in self.offset3D:
            ret += str(elem)+' '
        return ret.rstrip()
    def getmvmntinc(self):
        ret = ''
        for elem in self.mvmtIncrement:
            ret += str(elem)+' '
        return ret.rstrip()
    def getctrlinc(self):
        ret = ''
        for elem in self.ctrlIncrement:
            ret += str(elem)+' '
        return ret.rstrip()
    def getshiftinc(self):
        ret = ''
        for elem in self.shiftIncrement:
            ret += str(elem)+' '
        return ret.rstrip()
    def getdefaultborder(self):
        ret = ''
        for elem in self.defaultBorder:
            ret += str(elem)+' '
        return ret.rstrip()
    def getdefaultfill(self):
        ret = ''
        for elem in self.defaultFill:
            ret += str(elem)+' '
        return ret.rstrip()
    def getgridsize(self):
        ret = ''
        for elem in self.gridSize:
            ret += str(elem)+' '
        return ret.rstrip()
    def getgriddistance(self):
        ret = ''
        for elem in self.gridDistance:
            ret += str(elem)+' '
        return ret.rstrip()
    def getgridnumber(self):
        ret = ''
        for elem in self.gridNumber:
            ret += str(elem)+' '
        return ret.rstrip()
    def getbordercolors(self):
        ret = ''
        for elem in self.borderColors: #elem is a list of 3 floats
            tmp = ''
            for flt in elem:
                tmp += str(flt)+' '
            ret += tmp.rstrip()+', '
        return ret.rstrip()
    def getfillcolors(self):
        ret = ''
        for elem in self.fillColors: #elem is a list of 3 floats
            tmp = ''
            for flt in elem:
                tmp += str(flt)+' '
            ret += tmp.rstrip()+', '   
        return ret.rstrip()

# Helper functions
    def s2b(self, string):
        '''Converts string to bool'''
        if str(string) == 'None':
            return None
        else:
            return string.lower() in ('true')
    def writeseries(self, outpath):
        print('Creating output directory...'),
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        print('DONE')
        print('\tCreated: '+outpath)
        print('Writing series file...'),
        seriesoutpath = outpath+self.name+'.ser'
        #Build series root element
        attdict, contours = self.output()
        root = ET.Element(self.tag, attdict)
        #Build contour elements and append to root
        for contour in contours:
            root.append( ET.Element(contour.tag,contour.output()) )
    
        strlist = ET.tostringlist(root)
        #==========================================================================
        # Needs to be in order: hideTraces/unhideTraces/hideDomains/unhideDomains
            # Fix order:
        strlist = strlist[0].split(' ') # Separate single string into multiple strings for each elem
        count = 0
        for elem in strlist:
            if 'hideTraces' in elem and 'unhideTraces' not in elem:
                strlist.insert(1, strlist.pop(count))
            count += 1
        count = 0
        for elem in strlist:
            if 'unhideTraces' in elem:
                strlist.insert(2, strlist.pop(count))
            count += 1
        count = 0
        for elem in strlist:
            if 'hideDomains' in elem and 'unhideDomains' not in elem:
                strlist.insert(3, strlist.pop(count))
            count += 1
        count = 0
        for elem in strlist:
            if 'unhideDomains' in elem:
                strlist.insert(4, strlist.pop(count))
            count += 1
        #==========================================================================
            # Recombine into list of single str
        tempstr = ''
        for elem in strlist:
            tempstr += elem + ' '
        strlist = []
        strlist.append( tempstr.rstrip(' ') ) # Removes last blank space
    
        # Write to .ser file
        f = open(seriesoutpath, 'w')
        f.write('<?xml version="1.0"?>\n')
        f.write('<!DOCTYPE Section SYSTEM "series.dtd">\n\n')
        for elem in strlist:
            if '>' not in elem:
                f.write(elem),
            else:
                elem = elem+'\n'
                f.write(elem)
                if '/' in elem:
                    f.write('\n')        
        print('DONE')
        print('\tSeries output to: '+str(outpath+self.name+'.ser'))
    def writesections(self, outpath):
        print('Writing section file(s)...'),
        count = 0
        for section in self.sections:
            sectionoutpath = outpath+section.name
            count += 1
            #Build section root element
            attdict = section.output()
            root = ET.Element(section.tag, attdict)
            
            for elem in section.contours:
                curT = ET.Element('Transform', elem.transform.output())
                
                # Image/Image contour transform
                if elem.img != None: # Make transform from image
                    if elem.img.transform.output() == section.imgs[0].transform.output():
                        subelem = ET.Element('Image', section.imgs[0].output())
                        curT.append(subelem)
                        subelem = ET.Element(elem.tag, elem.output())
                        curT.append(subelem)
                        root.append(curT)
                    else:
                        print('Image contour transform != section image contour transform '+section.name)
                        print('i.e.: '+str(elem.transform.output())+' != '+str(section.imgs[0].transform.output()))
                        print('Image not written to xml file')
                else:
                    subelem = ET.Element(elem.tag, elem.output())
                    curT.append(subelem)
                    root.append(curT)
            
            elemtree = ET.ElementTree(root)
            elemtree.write(sectionoutpath, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        print('DONE')
        print('\t%d Section(s) output to: '+str(outpath))%count
    def getSectionsXML(self, path_to_series):
        #Build list of paths to sections
        print('Finding sections...'),
        ser = os.path.basename(path_to_series)
        inpath = os.path.dirname(path_to_series)+'/'
        serfixer = re.compile(re.escape('.ser'), re.IGNORECASE)
        sername = serfixer.sub('', ser)
        # look for files with 'seriesname'+'.'+'number'
        p = re.compile('^'+sername+'[.][0-9]*$')
        pathlist = [f for f in os.listdir(inpath) if p.match(f)] #list of paths to sections
        print('DONE')
        print('\t%d section(s) found in %s'%(len(pathlist),inpath))
        #Create and add section objects to series
        print('Creating section objects...'),
        for sec in pathlist:
            secpath = inpath + sec
            tree = ET.parse(secpath)
            root = tree.getroot() #Section
            section = Section(root,sec)
            self.addsection(section)
        self.sections = sorted(self.sections, key=lambda Section: Section.index) #sort by index
        print('DONE')
    def zeroIdentity(self):
        '''Converts points for all sections in a series to identity transform'''
        print('Converting sections to identity transform...'),
        for sec in self.sections:
            print('Converting to unity transform: '+sec.name)
            for c in sec.contours:
                if c.img == None: # Don't alter image contours i.e. domain1     
                    c.points = c.transform.worldpts(c.points)
                    c.transform.dim = 0
                    c.transform.ycoef = [0,0,1,0,0,0]
                    c.transform.xcoef = [0,1,0,0,0,0]
                    c._tform = c.transform.poptform()
        print('DONE')

    def addsection(self, section):
        '''Adds a <Section> object to <Series> object'''
        self.sections.append(section)
    def popindex(self, root):
        if root == None:
            return None
        return int(root.get('index'))
    def popunits(self, root):
        if root == None:
            return None
        return str(root.get('units'))
    def poptag(self, root):
        if root == None:
            return None
        else:
            return root.tag
    def popcontours(self, root):
        if root == None:
            return None
        ret = []
        for child in root:
            if child.tag == 'Contour':
                C = Contour(child)
                ret.append(C)
            elif child.tag == 'ZContour':
                Z = ZContour(child)
                ret.append(Z)
        return ret
    def popviewport(self, root):
        if root == None:
            return None
        rawList = list(root.get('viewport').split(' '))
        tmpList = []
        for elem in rawList:
            tmpList.append( float(elem) )
        return tmpList
    def popdefborder(self, root):
        if root == None:
            return None
        tmpList = [float(elem) for elem in list(root.get('defaultBorder').split(' '))]
        return tmpList
    def popdeffill(self, root):
        if root == None:
            return None
        tmpList = [float(elem) for elem in list(root.get('defaultFill').split(' '))]
        return tmpList
    def popbordcolors(self, root):
        if root == None:
            return None
            #Split up string into a list of strings containing 3 float points 
        splitList = root.get('borderColors').replace(',','').split('   ')
            #Make a list of lists containing floating points
        refinedList = []
        for elem in splitList:
            if elem != '':
                strfloats = elem.split(' ')
                intfloats = []
                #Turn strings into floats
                for num in strfloats:
                    num = float(num)
                    intfloats.append(num)
                refinedList.append(intfloats)
        return refinedList
    def popfillcolors(self, root):
        if root == None:
            return None
            #Split up string into a list of strings containing 3 float points 
        splitList = root.get('fillColors').replace(',','').split('   ')
            #Make a list of lists containing floating points
        refinedList = []
        for elem in splitList:
            if elem != '':
                strfloats = elem.split(' ')
                intfloats = []
                #Turn strings into floats
                for num in strfloats:
                    num = float(num)
                    intfloats.append(num)
                refinedList.append(intfloats)
        return refinedList
    def popoffset3D(self, root):
        if root == None:
            return None
        tmpList = [float(elem) for elem in list(root.get('offset3D').split(' '))]
        return tmpList
    def popdim3D(self, root):
        if root == None:
            return None
        tmpList = [float(elem) for elem in list(root.get('dim3D').split(' '))]
        return tmpList
    def popgridsize(self, root):
        if root == None:
            return None
        tmpList = [float(elem) for elem in list(root.get('gridSize').split(' '))]
        return tmpList
    def popgriddistance(self, root):
        if root == None:
            return None
        tmpList = [int(elem) for elem in list(root.get('gridDistance').split(' '))]
        return tmpList
    def popgridnumber(self, root):
        if root == None:
            return None
        tmpList = [int(elem) for elem in list(root.get('gridNumber').split(' '))]
        return tmpList
    def popmvmtincrement(self, root):
        if root == None:
            return None
        tmpList = [float(elem) for elem in list(root.get('mvmtIncrement').split(' '))]
        return tmpList
    def popctrlincrement(self, root):
        if root == None:
            return None
        tmpList = [float(elem) for elem in list(root.get('ctrlIncrement').split(' '))]
        return tmpList
    def popshiftincrement(self, root):
        if root == None:
            return None
        tmpList = [float(elem) for elem in list(root.get('shiftIncrement').split(' '))]
        return tmpList
    def popautoSaveSeries(self, root):
        if root == None:
            return None
        return root.get('autoSaveSeries')
    def popautoSaveSection(self, root):
        if root == None:
            return None
        return root.get('autoSaveSection')
    def popwarnSaveSection(self, root):
        if root == None:
            return None
        return root.get('warnSaveSection')
    def popbeepDeleting(self, root):
        if root == None:
            return None
        return root.get('beepDeleting')
    def popbeepPaging(self, root):
        if root == None:
            return None
        return root.get('beepPaging')
    def pophideTraces(self, root):
        if root == None:
            return None
        return root.get('hideTraces')
    def popunhideTraces(self, root):
        if root == None:
            return None
        return root.get('unhideTraces')
    def pophideDomains(self, root):
        if root == None:
            return None
        return root.get('hideDomains')
    def popunhideDomains(self, root):
        if root == None:
            return None
        return root.get('unhideDomains')
    def popuseAbsolutePaths(self, root):
        if root == None:
            return None
        return root.get('useAbsolutePaths')
    def popdefaultThickness(self, root):
        if root == None:
            return None
        return float(root.get('defaultThickness'))
    def popzMidSection(self, root):
        if root == None:
            return None
        return root.get('zMidSection')
    def popthumbWidth(self, root):
        if root == None:
            return None
        return float(root.get('thumbWidth'))
    def popthumbHeight(self, root):
        if root == None:
            return None
        return int(root.get('thumbHeight'))
    def popfitThumbSections(self, root):
        if root == None:
            return None
        return root.get('fitThumbSections')
    def popfirstThumbSection(self, root):
        if root == None:
            return None
        return int(root.get('firstThumbSection'))
    def poplastThumbSection(self, root):
        if root == None:
            return None
        return int(root.get('lastThumbSection'))
    def popskipSections(self, root):
        if root == None:
            return None
        return int(root.get('skipSections'))
    def popdisplayThumbContours(self, root):
        if root == None:
            return None
        return root.get('displayThumbContours')
    def popuseFlipbookStyle(self, root):
        if root == None:
            return None
        return root.get('useFlipbookStyle')
    def popflipRate(self, root):
        if root == None:
            return None
        return int(root.get('flipRate'))
    def popuseProxies(self, root):
        if root == None:
            return None
        return root.get('useProxies')
    def popwidthUseProxies(self, root):
        if root == None:
            return None
        return root.get('widthUseProxies')
    def popheightUseProxies(self, root):
        if root == None:
            return None
        return int(root.get('heightUseProxies'))
    def popscaleProxies(self, root):
        if root == None:
            return None
        return float(root.get('scaleProxies'))
    def popsignificantDigits(self, root):
        if root == None:
            return None
        return int(root.get('significantDigits'))
    def popdefaultMode(self, root):
        if root == None:
            return None
        return int(root.get('defaultMode'))
    def popdefaultName(self, root):
        if root == None:
            return None
        return root.get('defaultName')
    def popdefaultComment(self, root):
        if root == None:
            return None
        return root.get('defaultComment')
    def poplistSectionThickness(self, root):
        if root == None:
            return None
        return root.get('listSectionThickness')
    def poplistDomainSource(self, root):
        if root == None:
            return None
        return root.get('listDomainSource')
    def poplistDomainPixelsize(self, root):
        if root == None:
            return None
        return root.get('listDomainPixelsize')
    def poplistDomainLength(self, root):
        if root == None:
            return None
        return root.get('listDomainLength')
    def poplistDomainArea(self, root):
        if root == None:
            return None
        return root.get('listDomainArea')
    def poplistDomainMidpoint(self, root):
        if root == None:
            return None
        return root.get('listDomainMidpoint')
    def poplistTraceComment(self, root):
        if root == None:
            return None
        return root.get('listTraceComment')
    def poplistTraceLength(self, root):
        if root == None:
            return None
        return root.get('listTraceLength')
    def poplistTraceArea(self, root):
        if root == None:
            return None
        return root.get('listTraceArea')
    def poplistTraceCentroid(self, root):
        if root == None:
            return None
        return root.get('listTraceCentroid')
    def poplistTraceExtent(self, root):
        if root == None:
            return None
        return root.get('listTraceExtent')
    def poplistTraceZ(self, root):
        if root == None:
            return None
        return root.get('listTraceZ')
    def poplistTraceThickness(self, root):
        if root == None:
            return None
        return root.get('listTraceThickness')
    def poplistObjectRange(self, root):
        if root == None:
            return None
        return root.get('listObjectRange')
    def poplistObjectCount(self, root):
        if root == None:
            return None
        return root.get('listObjectCount')
    def poplistObjectSurfarea(self, root):
        if root == None:
            return None
        return root.get('listObjectSurfarea')
    def poplistObjectFlatarea(self, root):
        if root == None:
            return None
        return root.get('listObjectFlatarea')
    def poplistObjectVolume(self, root):
        if root == None:
            return None
        return root.get('listObjectVolume')
    def poplistZTraceNote(self, root):
        if root == None:
            return None
        return root.get('listZTraceNote')
    def poplistZTraceRange(self, root):
        if root == None:
            return None
        return root.get('listZTraceRange')
    def poplistZTraceLength(self, root):
        if root == None:
            return None
        return root.get('listZTraceLength')
    def poptype3Dobject(self, root):
        if root == None:
            return None
        return int(root.get('type3Dobject'))
    def popfirst3Dsection(self, root):
        if root == None:
            return None
        return int(root.get('first3Dsection'))
    def poplast3Dsection(self, root):
        if root == None:
            return None
        return int(root.get('last3Dsection'))
    def popmax3Dconnection(self, root):
        if root == None:
            return None
        return int(root.get('max3Dconnection'))
    def popupper3Dfaces(self, root):
        if root == None:
            return None
        return root.get('upper3Dfaces')
    def poplower3Dfaces(self, root):
        if root == None:
            return None
        return root.get('lower3Dfaces')
    def popfaceNormals(self, root):
        if root == None:
            return None
        return root.get('faceNormals')
    def popvertexNormals(self, root):
        if root == None:
            return None
        return root.get('vertexNormals')
    def popfacets3D(self, root):
        if root == None:
            return None
        return int(root.get('facets3D'))
    def popgridType(self, root):
        if root == None:
            return None
        return int(root.get('gridType'))
    def pophueStopWhen(self, root):
        if root == None:
            return None
        return int(root.get('hueStopWhen'))
    def pophueStopValue(self, root):
        if root == None:
            return None
        return int(root.get('hueStopValue'))
    def popsatStopWhen(self, root):
        if root == None:
            return None
        return int(root.get('satStopWhen'))
    def popsatStopValue(self, root):
        if root == None:
            return None
        return int(root.get('satStopValue'))
    def popbrightStopWhen(self, root):
        if root == None:
            return None
        return int(root.get('brightStopWhen'))
    def popbrightStopValue(self, root):
        if root == None:
            return None
        return int(root.get('brightStopValue'))
    def poptracesStopWhen(self, root):
        if root == None:
            return None
        return root.get('tracesStopWhen')
    def popareaStopPercent(self, root):
        if root == None:
            return None
        return int(root.get('areaStopPercent'))
    def popareaStopSize(self, root):
        if root == None:
            return None
        return int(root.get('areaStopSize'))
    def popContourMaskWidth(self, root):
        if root == None:
            return None
        return int(root.get('ContourMaskWidth'))
    def popsmoothingLength(self, root):
        if root == None:
            return None
        return int(root.get('smoothingLength'))