import os, re, math
import numpy as np
from shapely.geometry import Polygon, LineString, box
from lxml import etree as ET
from skimage import transform as tf
from collections import OrderedDict

def loadSeries(path_to_series):
    '''Create a series object, fully populated.'''
    if path_to_series.find('/') < 0:
        path_to_series = './' + path_to_series
    series = loadSeriesXML(path_to_series)
    series.getSectionsXML(path_to_series)
    return series
    
def loadSeriesXML(path_to_series):
    '''Creates a series object representation from a .ser XML file in path_to_series'''
    print('Creating series object from ' + path_to_series + '...'),
    #Parse series
    tree = ET.parse( path_to_series )
    
    root = tree.getroot() #Series
    #Create series object
    serName = path_to_series.split('/')[len(path_to_series.split('/'))-1].replace('.ser','')
    series = Series(root, serName)
    print('DONE')
    print('\tSeries: '+series.name)
    return series

class Contour:
# Python Functions
    # INITIALIZE
    def __init__(self, node=None, imgflag=None, transform=None):
        '''Initializes the Contour object. Two different Contour objects: Image Contours and Contours \
        delineated by the imgflag parameter.'''
        self.tag = 'Contour'
        self.name = self.popname(node)
        self.img = imgflag
        self.comment = self.popcomment(node)
        self.hidden = self.s2b(str(self.pophidden(node)))
        self.closed = self.s2b(str(self.popclosed(node)))
        self.simplified = self.s2b(str(self.popsimplified(node)))
        self.mode = self.popmode(node)
        self.transform = transform
        self.border = self.popborder(node)
        self.fill = self.popfill(node)
        self.points = self.poppoints(node)
        # Private
        self._shape = None # Shapely. Populated when necessary for computation (e.g. reconstructmergetool.py)
        self._attribs = ['name','comment','hidden','closed','simplified','mode','border','fill','points'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))

    # print(<Contour>) function output
    def __str__(self):
        '''Allows user to use print(<Contour>) function'''
        #################### Added for rmtgui tooltip output
        ptstr = '\n'
        count = 0
        for elem in self.points:
            count += 1
            if count == 3:
                ptstr += '\n'
                count = 0
            else:
                ptstr += ' '+str(elem)
        #####################
        return 'Contour object:\n-name: '+str(self.getname())+'\n-hidden: ' \
               +str(self.gethidden())+'\n-closed: '+str(self.getclosed()) \
               +'\n-simplified: '+str(self.getsimp())+'\n-mode: '+str(self.getmode()) \
               +'\n-border: '+str(self.getbord())+'\n-fill: '+str(self.getfill()) \
               +'\n-points: '+ptstr+'\n'
    def __eq__(self, other):
        '''Allows use of == between multiple contours.'''
        return self.output() == other.output()
    def __ne__(self, other):
        '''Allows use of != between multiple contours.'''
        return self.output() != other.output()
# Helper Functions
    def overlaps(self, other, threshold=(1+2**(-17))):
        '''Return 0 if no overlap.
        For closed traces: return 1 if AoU/AoI < threshold, return AoU/AoI if not < threshold
        For open traces: return 0 if # pts differs or distance between parallel pts > threshold
                         return 1 otherwise'''
        if self._shape == None:self.popshape()
        if other._shape == None:other.popshape()
        # Check bounding box
        if (not self.box().intersects(other.box()) and
            not self.box().touches(other.box()) ):
            return 0
        # Check if both same class of contours
        if self.closed != other.closed:
            return 0
        # Closed contours
        if self.closed:
            AoU = self._shape.union( other._shape ).area
            AoI = self._shape.intersection( other._shape ).area
            if AoI == 0:
                return 0
            elif AoU/AoI > threshold:
                return AoU/AoI # Returns actual value, not 0 or 1
            elif AoU/AoI < threshold:
                return 1
        # Open contours
        if not self.closed:
            if len( self.points ) != len( other.points ):
                return 0
            def distance(pt0, pt1):
                return math.sqrt( (pt0[0] - pt1[0])**2 + (pt0[1] - pt1[1])**2 )
            # Lists of world coords to compare
            a = self.transform.worldpts(self.points)
            b = other.transform.worldpts(other.points)
            distlist = [distance(a[i],b[i]) for i in range(len(self.points))] 
            for elem in distlist:
                if elem > threshold:
                    return 0
        return 1
    def s2b(self, string):
        '''Converts string to bool'''
        if string == 'None':
            return None
        else:
            return string.lower() in ('true')
    def popname(self, node):
        if node == None:
            return 'Empty Contour'
        else:
            return str( node.get('name') )
    def popshape(self):
        '''Adds polygon object (shapely) to self._shape'''
        # Closed trace
        if self.closed == True:
            # If image contour, multiply pts by mag before inverting transform
            if self.img != None:
                mag = self.img.mag
                xvals = [pt[0]*mag for pt in self.points]
                yvals = [pt[1]*mag for pt in self.points]
                pts = zip(xvals,yvals)
            else:
                if len(self.points) < 3:
                    return None
                pts = self.points
            self._shape = Polygon( self.transform.worldpts(pts) )
        # Open trace
        elif self.closed == False and len(self.points)>1:
            self._shape = LineString( self.transform.worldpts(self.points) )
        else:
            print('\nInvalid shape characteristics: '+self.name)
            print('Quit for debug')
            quit() # for dbugging
    def box(self):
        '''Returns bounding box of shape (shapely) library'''
        if self._shape != None:
            minx, miny, maxx, maxy = self._shape.bounds
            return box(minx, miny, maxx, maxy)
        else:
            print('NoneType for shape: '+self.name)
    def popcomment(self, node):
        '''Searches xml node for comments.'''
        if node == None:
            return None
        else:
            return node.get('comment', None)
    def pophidden(self, node):
        '''Searches xml node for hidden.'''
        if node == None:
            return None
        elif str(node.get('hidden', None)).capitalize() == 'True':
            return True
        else:
            return False
    def popclosed(self, node):
        '''Searches xml node for closed.'''
        if node == None:
            return None
        elif str(node.get('closed', None)).capitalize() == 'True':
            return True
        else:
            return False
    def popsimplified(self, node):
        '''Searches xml node for closed.'''
        if node == None:
            return None
        elif str(node.get('simplified', None)).capitalize() == 'True':
            return True
        else:
            return False
    def popmode(self, node):
        '''Searches xml node for mode.'''
        if node == None:
            return None
        else:
            return int( node.get('mode') )
    def popborder(self, node):
        '''Searches xml node for border. Creates a list of floats.'''
        if node == None:
            return []
        bord = [float(elem) for elem in list(node.get('border').split(' '))]
        return bord
    def popfill(self, node):
        '''Searches xml node for fill. Creates a list of floats.'''
        if node == None:
            return []
        fill = [float(elem) for elem in list(node.get('fill').split(' '))]
        return fill
    def poppoints(self, node):
        '''Searches xml node for points. List of points tuples (x,y), \
        int or float depends on type in the xml node.'''
        if node == None:
            return []
        partPoints = list(node.get('points').lstrip(' ').split(','))
        #make a new list of clean points, to be added to object
        ptList = []
        for i in range( len(partPoints) ):
            ptList.append( partPoints[i].strip() )
        #remove empty spots in list
        for i in range( len(ptList) ):
            if ptList[i] == '':
                ptList.remove('')
        #convert strings into tuples
        strTupList = []
        for elem in ptList:
            strTupList.append(tuple(elem.split(' ')))
        tupList = []
        for elem in strTupList:
            if '.' in elem[0]: #Float
                a=float(elem[0]) 
            if '.' in elem[1]: #Float
                b=float(elem[1])
            if '.' not in elem[0] and '.' not in elem[1]: #Int
                a=int(elem[0])
                b=int(elem[1])
            if '.' not in elem[0] and '.' in elem[1]:
                a = int(elem[0])
                b = float(elem[1])
            if '.' in elem[0] and '.' not in elem[1]:
                a = float(elem[0])
                b = int(elem[1])
            tup = (a,b)
            tupList.append(tup)
        return tupList
# Accessors
    def getLength(self): #===
        '''Returns the sum of all line segments in the contour object'''
        length = 0
        for index in range( len(self.points) ):
            if index+1 >= len(self.points): # stop when outside index range
                break
            pt = self.points[index]
            nextPt = self.points[index+1]
            length += (((nextPt[0]-pt[0])**2)+((nextPt[1]-pt[1])**2))**(0.5)
        if self.closed: # If closed object, add distance between 1st and last pt too
            length += (((self.points[0][0]-self.points[-1][0])**2)+((self.points[0][1]-self.points[-1][1])**2))**(0.5)
        return length #=== sqrt is taxing computation; reimplement with 1 sqrt at end?
    def getStartEndCount(self, series):
        '''Returns the start, end, and count values for this contour in given series. Determined by self.name only'''
        return series.getStartEndCount(self.name)
    def getVolume(self, series):
        return series.getVolume(self.name)
    def getSurfaceArea(self, series):
        return series.getSurfaceArea(self.name)
    def getFlatArea(self, series):
        return series.getFlatArea(self.name)
    def gettracepts(self):
        '''Returns trace space coordinates as [ (x,y), ... ]'''
        return self.points
    def getworldpts(self):
        '''Returns world space coordinates as [ (x,y), ... ]'''
        # transform.worlpts(pts) is in the form of nparray
        ptlist = [tuple(elem) for elem in self.transform.worldpts(self.points)]
        return ptlist # List of tuples
    def getimagepts(self): 
        '''Returns pixel space coordinates as [ (x,y), ... ]'''
        return self.transform.imgpts() 
    def gettag(self):
        '''Returns Tag (str)'''
        return self.tag
    def getname(self):
        '''Returns Name attribute (str)'''
        return self.name
    def gethidden(self):
        '''Returns Hidden attribute (bool)'''
        return self.hidden
    def getclosed(self):
        '''Returns Closed attribute (bool)'''
        return self.closed
    def getsimp(self):
        '''Returns Simplified attribute (bool)'''
        return self.simplified
    def getmode(self):
        '''Returns Mode attribute (int)'''
        return self.mode
    def getbord(self):
        '''Returns Border attribute'''
        ret = str(self.border[0])+' '+str(self.border[1])+' '+str(self.border[2])
        return ret
    def getfill(self):
        '''Returns Fill attribute'''
        ret = str(self.fill[0])+' '+str(self.fill[1])+' '+str(self.fill[2])
        return ret
    def getxbord(self):
        '''Returns border attribute in xml output format'''
        bord = ''
        for elem in self.border:
            bord += str(elem)+' '
        return str(bord).rstrip()
    def getxfill(self):
        '''Returns fill attribute in xml output format'''
        fill = ''
        for elem in self.fill:
            fill += str(elem)+' '
        return str(fill).rstrip()
    def getxpoints(self):
        '''Returns Points attribute (list of strings, each consisting of two numbers \
separated by a single space)'''
        ret = ''
        for tup in self.points:
            ret += str(tup[0])+' '+str(tup[1])+', '
        return ret.rstrip()
    def getattribs(self):
        '''Returns all attributes'''
        return self.name, \
        self.comment, \
        self.hidden, \
        self.closed, \
        self.simplified, \
        self.mode, \
        self.border, \
        self.fill, \
        self.points
    def xgetattribs(self):
        '''Returns all attributes as list of strings in xml output format'''
        return str(self.name), \
        str(self.comment), \
        str(self.hidden).lower(), \
        str(self.closed).lower(), \
        str(self.simplified).lower(), \
        str(self.mode), \
        str(self.getxbord()), \
        str(self.getxfill()), \
        str(self.getxpoints()) 
    def output(self):
        '''Returns a dictionary of attributes'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for value in values:
            if value not in [None, 'None', 'none']:
                attributes[keys[count]] = value
            count += 1
        return attributes

class Image:
    '''Abstract data type to store data associated with images. Image classes exist in <Section>.imgs as 
    well as in contour.img if contour == 'domain1'. Be aware of this when making changes to image classes
    as they will have to be applied to both locations.'''
# Python functions
    # INITIALIZE
    def __init__(self, node=None, transform=None):
        self.tag = 'Image'
        self.name = self.popname(node) # same as self.src
        self.src = self.popname(node)
        self.mag = self.popmag(node) #float
        self.contrast = self.popcontrast(node) #float 
        self.brightness = self.popbrightness(node) #float
        self.red = self.popred(node)
        self.green = self.popgreen(node)
        self.blue = self.popblue(node)
        self.transform = transform
        # Private
        self._attribs = ['mag','contrast','brightness','red','green','blue','src'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))
    # print(<Image>) function output
    def __str__(self):
        '''Allows print( <image> ) function. Returns attributes as string.'''
        return '\nImage Object:\n-src: %s\n-mag: %f\n-contrast: %f\n-brightness: %f\n\
-red: %s\n-green: %s\n-blue: %s'%(self.getattribs())
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        if other == None:
            return False
#         return self.output() == other.output()
        return (self.transform == other.transform or
                self.src == other.src)
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        if other == None:
            return True
#         return self.output() != other.output()
        return (self.transform != other.transform or
                self.src != other.src)
# Accessors
    def output(self):
        '''Returns a dictionary of attributes'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for value in values:
            attributes[keys[count]] = value
            count += 1
        return attributes      
    def gettag(self):
        '''tag ---> string'''
        return self.tag
    def getsrc(self):
        '''src ---> string'''
        return self.src
    def getmag(self):
        '''mag ---> float'''
        return self.mag
    def getcontrast(self):
        '''contrast ---> float'''
        return self.contrast
    def getbrightness(self):
        '''brightness ---> float'''
        return self.brightness
    def getred(self):
        '''red ---> bool'''
        return self.red
    def getgreen(self):
        '''green ---> bool'''
        return self.green
    def getblue(self):
        '''blue ---> bool'''
        return self.blue
    def gettransform(self):
        '''transform ---> object'''
        return self.transform
    def xgetattribs(self):
        '''Returns all attributes for <image> (as strings)'''
        return str(self.mag), str(self.contrast), str(self.brightness), \
            str(self.red).lower(), str(self.green).lower(), str(self.blue).lower(), str(self.src)
    def getattribs(self):
        return self.src, self.mag, self.contrast, self.brightness, self.red, self.green, self.blue

# Mutators
    def popred(self, node):
        '''Searches xml node for red attribute'''
        if node == None:
            return None
        elif node.get('red', None) == None:
            return True
        elif node.get('red').capitalize() == 'True':
            return True
        else:
            return False
    def popgreen(self, node):
        '''Searches xml node for green attribute'''
        if node == None:
            return None
        elif node.get('green', None) == None:
            return True
        elif node.get('green').capitalize() == 'True':
            return True
        else:
            return False
    def popblue(self, node):
        '''Searches xml node for blue attribute'''
        if node == None:
            return None
        elif node.get('blue', None) == None:
            return True
        elif node.get('blue').capitalize() == 'True':
            return True
        else:
            return False
    def popname(self, node):
        if node == None:
            return None
        return node.get('src')
    def popmag(self, node):
        if node == None:
            return None
        return float( node.get('mag') )
    def popcontrast(self, node):
        if node == None:
            return None
        return float( node.get('contrast') )
    def popbrightness(self, node):
        if node == None:
            return None
        return float( node.get('brightness') )

class rObject:
    def __init__(self, name=None, series=None, verbose=False):
        self.name = name
        self.series = self.chkSeries(series)
        
        self.protrusion = self.getProtNumber() # Protrusion number (stored as 'p##')
        self.dendrite = self.getDendNumber() # Parent dendrite number (stored as 'd##')
        
        self.rType = self.getrType()
        self.data = {} # updated in makeSpecific
        self.start = self.series.getStartEndCount(self.name)[0]
        self.end = self.series.getStartEndCount(self.name)[1]
        self.count = self.series.getStartEndCount(self.name)[2]
        
        self.makeSpecific()
    
        if verbose:
            print   
            print('=== rObject Created ===')
            print('name: '+self.name)
            print('den: '+self.dendrite)
            try:print('prot: '+self.protrusion)
            except:print('No prot')
            try:print('type: '+self.rType)
            except:print('No type')
    
    def getDendNumber(self):
        dend = re.compile('d[0-9]{1,}')
        try:
            return self.name[:dend.match(self.name).end()]
        except:
            return None
    
    def getProtNumber(self): 
        dend = re.compile('d[0-9]{1,}')
        tmpName = self.name[dend.match(self.name).end():] # remove dendrite portion of name
        try:
            prot = re.compile('[0-9]{1,}')
            protNum = tmpName[prot.search(tmpName).start():prot.search(tmpName).end()]
            return 'p'+str(protNum)
        except:
            return None
            
    def makeSpecific(self):
        '''Creates unique data for this rObject (depends on type)'''
        if self.rType != None:
            rType = self.rType.lower()
            if rType == 'p': # Protrusion
                importantData = ['start', 'end', 'count']
                self.children = self.findChildren()
            elif rType == 'c': # C
                importantData = ['start', 'end', 'count']
            elif 'cfa' in rType: # CFA
                importantData = ['start', 'end', 'count', 'surface area', 'flat area']
            elif 'endo' in rType: # Endosome
                importantData = ['start', 'end', 'count']
            elif rType[0:3] == 'ser': # SER #===
                importantData = ['start', 'end', 'count']
            elif rType[0:2] == 'sp': # Spine #===
                importantData = ['start', 'end', 'count', 'surface area', 'flat area', 'volume']
            elif rType[0:2] == 'ax': # Axon #===
                importantData = ['start', 'end', 'count']
            else:
                importantData = ['start', 'end', 'count']
        else:
            importantData = ['start', 'end', 'count']
        self.getData( importantData )
    
    def getData(self, list_of_desired_data=None):
        data = OrderedDict()
        for item in list_of_desired_data:
            data[item] = self.series.getData(self.name, item)
        self.data = data
        self.numColumns = len(list_of_desired_data)
             
    def getrType(self):
        '''Returns type of character'''
        if self.protrusion != None:
            prot = re.compile(self.protrusion[1:]) # dont include the 'p' in self.protrusion
            dend = re.compile(self.dendrite)
            tmpName = self.name[dend.match(self.name).end():] # remove dendrite from name
            return tmpName[:prot.search(tmpName).start()]
        return None
        
    def findChildren(self):
        '''Finds children of this protrusion and puts in self.children dict under trace type'''
        children = {}
        child_exp = re.compile(self.dendrite+'.{0,}'+self.protrusion[1:]) # dont include 'p' in self.protrusion
        dend_exp = re.compile(self.dendrite)
        for child in self.series.getObjectLists()[2]:
            if child_exp.match(child) != None:
                # Extract from name what is in between dend and prot
                endOfDendrite = dend_exp.match(child).end()
                beginOfProtrusion = child.rfind(self.protrusion[1:])
                try: # Try to add to existing entry in dictionary
                    children[str(child[endOfDendrite:beginOfProtrusion])].append(child)
                except: # Make entry and then add to it
                    children[str(child[endOfDendrite:beginOfProtrusion])] = []
                    children[str(child[endOfDendrite:beginOfProtrusion])].append(child)            
        return children
    
    def getSpacing(self):
        '''Returns number of spaces to add after excel sheet'''
        try:
            return max([len(self.children[child]) for child in self.children])-1
        except:
            return 0
        
    def chkSeries(self, series):
        '''Checks if series is str, if so: try to load as series object'''
        if type(series) == str:
            try:
                return loadSeries(series)
            except:
                print('Could not create series from string: '+series)
        else:
            return series

class Section:
# Python Functions
    # INITIALIZE
    def __init__(self, root=None, name='Unknown'): #root is xml tree
        # Create <section>
        self.name = name
        self.tag = 'Section'
        # Contours/Images
        self.contours = self.poplists(root)[0] # List of contours 
        self.imgs = self.poplists(root)[1] # list of images
        # Attributes
        self.index = self.popindex(root) #int
        self.thickness = self.popthickness(root) #float
        self.alignLocked = self.popalignLocked(root)
        # Private
        self._attribs = ['index','thickness','alignLocked'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))
        
        self.checkMultImgs() # Deletes all but the first image in self.imgs
        
    # LENGTH
    def __len__(self):
        '''Allows use of len(<Section>) function. Returns length of contours'''
        return len(self.contours)
    # allows indexing of Section object
    def __getitem__(self,x):
        '''Allows use of <Section>[x] to return xth elements in list'''
        return self.contours[x]
    # print(<Section>) output
    def __str__(self):
        '''Allows use of print(<section>) function.'''
        return 'Index: %d\nThickness: %f\nAlign Locked: %s'%(self.index, \
                                                                 self.thickness, \
                                                                 self.alignLocked)   
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        return self.output() == other.output()
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return self.output() != other.output() 
# Accessors
    def popshapes(self):
        for contour in self.contours:
            contour.popshape()
    def checkMultImgs(self):
        if len(self.imgs) > 1:
            print(self.name+': Multiple images found. Only last one kept.')
            # Last img in list is the top image in the reconstruct window
            self.imgs = [self.imgs.pop()]
    def output(self):
        '''Returns a dictionary of attributes and a list of contours for building xml'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for value in values:
            attributes[keys[count]] = value
            count += 1
        return attributes
    def getattribs(self):
        '''Returns attributes'''
        return self.index, self.thickness, self.alignLocked
    def xgetattribs(self):
        '''Returns attributes in xml output format'''
        return str(self.index), str(self.thickness), str(self.alignLocked).lower()
# Mutators
    def s2b(self, string):
        '''Converts string to bool'''
        if string == 'None':
            return None
        else:
            return string.lower() in ('true')       
    def poplists(self, root):
        '''Populates section object with Contours/Images/etc.'''
        contours = []
        images = []
        if root == None:
            return contours, images # Empty if no root
        for transform in root:
            imgflag = None
            for child in transform:
                if child.tag == 'Image':
                    imgflag = True
                    I = Image(child, Transform(transform))
                    images.append(I)
                elif child.tag == 'Contour':
                    C = Contour(child, imgflag, Transform(transform))
                    if imgflag: # Contour has an image, create pointer to image
                        C.img = I
                    if len(C.points) != 1: #=== invalid contour
                        contours.append(C)
                    imgflag = None     
        
        return contours, images
    def popindex(self, root):
        if root == None:
            return None
        return int(root.get('index'))
    def popthickness(self, root):
        if root == None:
            return None
        return float(root.get('thickness'))
    def popalignLocked(self, root):
        if root == None:
            return None
        return root.get('alignLocked')

class Series:
# Python functions
    # INITIALIZE
    def __init__(self, root=None, name='No Name'):
        self.name = name
        self.tag = 'Series'
        
        self.contours = self.popcontours(root)
        self.sections = [] #Sorted in self.getSectionsXML()
        
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
        return (self.output()[0] == other.output()[0] and
                self.output()[1] == other.output()[1])
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return (self.output()[0] != other.output()[0] and
                self.output()[1] != other.output()[1])
# Accessors
    def getData(self, object_name, data_string):
        string = str(data_string).lower()
        if string == 'volume':
            return self.getVolume(object_name)
        elif string == 'total volume':
            return self.getTotalVolume(object_name)
        elif string == 'surface area':
            return self.getSurfaceArea(object_name)
        elif string == 'flat area':
            return self.getFlatArea(object_name)
        elif string == 'start':
            return self.getStartEndCount(object_name)[0]
        elif string == 'end':
            return self.getStartEndCount(object_name)[1]
        elif string == 'count':    
            return self.getStartEndCount(object_name)[2]
    def getObjectLists(self): #=== added ',' to {2}
        '''Returns sorted lists of dendrite names, protrusion names, trace names, and a list of other objects in series'''
        dendrite_expression = 'd[0-9]{2,}' # represents base dendrite name (d##)
        protrusion_expression = 'd[0-9]{2,}p[0-9]{2,}$' # represents base protrusion name (d##p##)
        trace_expression = 'd[0-9]{2,}.{1,}[0-9]{2,}' # represents trace name (d##<tracetype>##)
        
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
                    dendrites.append(contour.name[0:dendrite_expression.match(contour.name).end()]) #===
                # Protrusion
                if protrusion_expression.match(contour.name) != None:
                    protrusions.append(contour.name)
                # Trace === expand to > 2 digits!
                if (trace_expression.match(contour.name) != None and
                    protrusion_expression.match(contour.name) == None):
                    traces.append(contour.name)
                    # Make sure a d##p## exists for this trace
                    thisProt = contour.name[0:3]+'p'+contour.name[4:6]
                    if (protrusion_expression.match(thisProt) and
                        thisProt not in protrusions):
                        protrusions.append(thisProt)
                # Everything else (other)
                if (dendrite_expression.match(contour.name) == None and
                    protrusion_expression.match(contour.name) == None and
                    trace_expression.match(contour.name) == None):
                    others.append(contour.name)
        return sorted(list(set(dendrites))), sorted(list(set(protrusions))), sorted(list(set(traces))), sorted(list(set(others)))
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
        if outpath[-1] != '/':
            outpath += '/'
        print('Creating output directory...'),
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        print('DONE')
        print('\tCreated: '+outpath)
        print('Writing series file...'),
        seriesoutpath = outpath+self.name+'.ser'
        if os.path.exists(seriesoutpath):
            raise IOError('\nFilename %s already exists.\nPlease delete to avoid overwrite'%seriesoutpath)
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
        if outpath[-1] != '/':
            outpath += '/'
        print('Writing section file(s)...'),
        count = 0
        for section in self.sections:
            sectionoutpath = outpath+section.name
            if os.path.exists(sectionoutpath):
                raise IOError('\nFilename %s already exists.\nPlease delete to avoid overwrite'%sectionoutpath)
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

class Transform:
# Python functions
    # INITIALIZE
    def __init__(self, node=None): # node is xml tree node
        '''Initializes the Transform object'''
        # Attributes
        self.tag = 'Transform'
        self.name = 'Transform'
        self.dim = self.popdim(node) #int
        self.ycoef = self.popyxcoef(node)[0]
        self.xcoef = self.popyxcoef(node)[1]
        self.tospace = '' #===
        self.fromspace = '' #===
        # Private
        self._tform = self.poptform()
        self._attribs = ['dim','xcoef','ycoef'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows user to use print( <Transform> ) function'''
        return 'Transform object:\n-dim: '+str(self.dim)+'\n-ycoef: ' \
               +str(self.getycoef())+'\n-xcoef: '+str(self.getxcoef())
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        return self.output() == other.output()
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return self.output() != other.output()
# Accessors
    def worldpts(self, points):
        '''Returns inverse points'''
        newpts = self._tform.inverse(np.asarray(points))
        return list(map(tuple,newpts))
    def imgpts(self, points): #===
        '''Returns imgpts'''
        return
    def getycoef(self):
        '''Returns ycoefs'''
        ret = ''
        for elem in self.ycoef:
            ret += ' '+str(elem)
        return ret
    def getxcoef(self):
        '''Returns xcoefs'''
        ret = ''
        for elem in self.xcoef:
            ret += ' '+str(elem)
        return ret
    def getattribs(self):
        '''Returns Dim, xcoefs, and ycoefs as they are stored in memory'''
        return self.dim, self.xcoef, self.ycoef
    def xgetattribs(self):
        '''Returns dim, xcoefs, and ycoefs as strings (for XML generation)'''
        return str(self.dim), str(self.getxcoef()), str(self.getycoef())
    def output(self):
        '''Returns a dictionary of attributes and a list of contours for building xml'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for val in values:
            attributes[keys[count]] = val
            count += 1
        return attributes
    def isAffine(self):
        '''Returns true if the transform is affine i.e. if a[3,4,5] and b[3,4,5] are 0'''
        xcheck = self.xcoef[3:6]
        ycheck = self.ycoef[3:6]
        for elem in xcheck:
            if elem != 0:
                return False
        for elem in ycheck:
            if elem != 0:
                return False
        return True
# Mutators              
    def popdim(self, node):
        if node == None:
            return None
        return int(node.get('dim'))  
    def poptform(self): # v for verbosity
        '''Creates self._tform variable which represents the transform'''
        if self.xcoef == [] or self.ycoef == [] or self.dim == []:
            return None
        a = self.xcoef
        b = self.ycoef
        # Affine transform
        if self.dim in range(0,4):
            if self.dim == 0: 
                tmatrix = np.array( [1,0,0,0,1,0,0,0,1] ).reshape((3,3))
            elif self.dim == 1:
                tmatrix = np.array( [1,0,a[0],0,1,b[0],0,0,1] ).reshape((3,3))
            elif self.dim == 2: # Special case, swap b[1] and b[2] (look at original Reconstruct code: nform.cpp)
                tmatrix = np.array( [a[1],0,a[0],0,b[1],b[0],0,0,1] ).reshape((3,3))
            elif self.dim == 3:
                tmatrix = np.array( [a[1],a[2],a[0],b[1],b[2],b[0],0,0,1] ).reshape((3,3))
            return tf.AffineTransform(tmatrix)
        # Polynomial transform
        elif self.dim in range(4,7):
            tmatrix = np.array( [a[0],a[1],a[2],a[4],a[3],a[5],b[0],b[1],b[2],b[4],b[3],b[5]] ).reshape((2,6))
            # create matrix of coefficients 
            tforward = tf.PolynomialTransform(tmatrix)
            def getrevt(pts): # pts are a np.array
                newpts = [] # list of final estimates of (x,y)
                for i in range( len(pts) ):
                    # (u,v) for which we want (x,y)
                    u, v = pts[i,0], pts[i,1] # input pts
                    # initial guess of (x,y)
                    x0, y0 = 0.0, 0.0
                    # get forward tform of initial guess
                    uv0 = tforward(np.array([x0,y0]).reshape([1, 2]))[0]
                    u0 = uv0[0]
                    v0 = uv0[1]
                    e = 1.0 # reduce error to this limit 
                    epsilon = 5e-10
                    i = 0
                    while e > epsilon and i < 100: #=== 10 -> 100
                        i+=1
                        # compute Jacobian
                        l = a[1] + a[3]*y0 + 2.0*a[4]*x0
                        m = a[2] + a[3]*x0 + 2.0*a[5]*y0
                        n = b[1] + b[3]*y0 + 2.0*b[4]*x0
                        o = b[2] + b[3]*x0 + 2.0*b[5]*y0
                        p = l*o - m*n # determinant for inverse
                        if abs(p) > epsilon:
                            # increment x0,y0 by inverse of Jacobian
                            x0 = x0 + ((o*(u-u0) - m*(v-v0))/p)
                            y0 = y0 + ((l*(v-v0) - n*(u-u0))/p)
                        else:
                            # try Jacobian transpose instead
                            x0 = x0 + (l*(u-u0) + n*(v-v0))        
                            y0 = y0 + (m*(u-u0) + o*(v-v0))
                        # get forward tform of current guess       
                        uv0 = tforward(np.array([x0,y0]).reshape([1, 2]))[0]
                        u0 = uv0[0]
                        v0 = uv0[1]
                        # compute closeness to goal
                        e = abs(u-u0) + abs(v-v0)
                    # append final estimate of (x,y) to newpts list
                    newpts.append((x0,y0))     
                newpts = np.asarray(newpts)           
                return newpts
            tforward.inverse = getrevt
            
            return tforward
    def popyxcoef(self, node):
        '''Populates self.ycoef and self.xcoef'''
        if node == None:
            return [], []
        # digits added as int, everything else float
        y = []
        for elem in node.get('ycoef').split(' '):
            if elem.isdigit():
                y.append( int(elem) )
            elif elem != '':
                y.append( float(elem) )
        x = []
        for elem in node.get('xcoef').split(' '):
            if elem.isdigit(): 
                x.append( int(elem) )
            elif elem != '':
                x.append( float(elem) )
        return y,x

class ZContour:
# Python Functions
    # INITIALIZE
    def __init__(self, node=None):
        self.tag = 'ZContour'
        self.name = self.popname(node)
        self.closed = self.s2b(self.popclosed(node))
        self.mode = self.popmode(node)
        self.border = self.popborder(node)
        self.fill = self.popfill(node)
        self.points = self.poppts(node) #list of pts [ (x,y,z), ... ]
        # Private
        self._attribs = ['name','closed','border','fill','mode','points'] # List of all attributes, used for creating an attribute dictionary for output (see output(self))
    # STRING REPRESENTATION
    def __str__(self):
        '''Allows user to use print( <ZContour> ) function'''
        return 'ZContour object:\n-name: '+str(self.name)+'\n-closed: ' \
               +str(self.closed)+'\n-mode: '+str(self.mode) \
               +'\n-border: '+str(self.border)+'\n-fill: '+str(self.fill) \
               +'\n-points: '+str(self.points)+'\n'
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        return self.output() == other.output()
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return self.output() != other.output()
# Accessors
    def overlaps(self, other):
        threshold = (1+2**(-17))
    
        def distance(pt0, pt1):
            return math.sqrt( (pt0[0] - pt1[0])**2 + (pt0[1] - pt1[1])**2 )
        
        # Check equal # pts
        if len(self.points) != len(other.points):
            return 0
        
        # Build list of min distance between pts
        distlist = []
        for elem in self.points:
            ptdistances = []
            for elem2 in other.points:
                if elem[2] == elem2[2]: # if in same section
                    dist = distance(elem[0:2],elem2[0:2])
                    ptdistances.append( dist )
            if len(ptdistances) != 0:
                distlist.append( min(ptdistances) )
        
        # check for any distances above threshold
        for elem in distlist:
            if elem > threshold: # no matching point
                return 0
        return 1        
    def getpoints(self):
        return self.points
    def getxbord(self):
        bord = ''
        for elem in self.border:
            bord += str(elem)+' '
        return str(bord).rstrip()
    def getxfill(self):
        fill = ''
        for elem in self.fill:
            fill += str(elem)+' '
        return str(fill).rstrip()
    def getxpoints(self):
        ret = ''
        for tup in self.points:
            ret += str(tup[0])+' '+str(tup[1])+' '+str(tup[2])+', '
        return ret.rstrip()
    def getattribs(self):
        '''Returns all zcontour attributes'''
        return self.name, self.closed, self.border, self.fill, \
               self.mode, self.points
    def xgetattribs(self):
        '''Returns all zcontour attributes, xml formatting (strings)'''
        return str(self.name), str(self.closed).lower(), self.getxbord(), self.getxfill(), \
            str(self.mode), str(self.getxpoints())
    def output(self):
        '''Returns a dictionary of attributes'''
        attributes = {}
        keys = self._attribs
        values = list(self.xgetattribs())
        count = 0
        for value in values:
            if value not in [None, 'None', 'none']:
                attributes[keys[count]] = value
            count += 1
        return attributes
# Mutators
    def s2b(self, string):
        '''Converts string to bool'''
        if str(string) == 'None':
            return None
        return str(string).lower() in ('true')
    def popmode(self, node):
        if node.get('mode', None) == None or node == None:
            return None
        else:
            return int( node.get('mode') )
    def popborder(self, node):
        '''Populates self.border'''
        if node.get('border', None) == None or node == None:
            return None
        else:
            bord = [float(elem) for elem in list(node.get('border').split(' '))]
            return bord
    def popfill(self, node):
        '''Populates self.fill'''
        if node.get('fill', None) == None or node == None:
            return None
        fill = [float(elem) for elem in list(node.get('fill').split(' '))]
        return fill
    def poppts(self, node):
        if node.get('points', None) == None or node == None:
            return None
        #partition points into a list of messy crap
        partPoints = list(node.get('points').lstrip(' ').split(','))
            #example: ['5.93694 3.75884 156', '  5.46795 4.10569 144',
            #'  4.82797 4.41347 139', '  4.77912 4.64308 124', '  4.63744 4.97528 99', '  ']

        #make a new list of clean points, to be added to object
        ptList = []
        for i in range( len(partPoints) ):
            ptList.append( partPoints[i].strip() )
                #example: ['5.93694 3.75884 156', '5.46795 4.10569 144', '4.82797 4.41347 139',
                #'4.77912 4.64308 124', '4.63744 4.97528 99', '']

        #remove empty points
        while '' in ptList:
            ptList.remove('')
                #example: ['5.93694 3.75884 156', '5.46795 4.10569 144', '4.82797 4.41347 139',
                #'4.77912 4.64308 124', '4.63744 4.97528 99']
                
        #turn into tuples of 3-space pts
        finalList = []
        for elem in ptList:
            elsplit = elem.split(' ')
            tup = ( float(elsplit[0]), float(elsplit[1]), int(elsplit[2]) )
            finalList.append(tup)
        return finalList   
    def popname(self, node):
        if node == None:
            return None
        return str( node.get('name') )
    def popclosed(self, node):
        if node == None:
            return None
        return node.get('closed')