import os, re, math
import numpy as np
import pyrecon.dev.handleXML as xml
from shapely.geometry import Polygon, LineString, box, LinearRing
from skimage import transform as tf
from collections import OrderedDict

def openSeries(directory):
    '''Returns a Series object with associated Sections from the directory.'''
    files = [f for f in listdir(directory) if isfile(join(path,f))]
    series = None
    sections = None

    for f in files:
        if '.ser' in f:
           series = Series(directory+f)

    #now, create sections and append to series
    # return series

class Contour:
    def __init__(self, *args, **kwargs):
        self.name = None
        self.comment = None
        self.hidden = None
        self.closed = None
        self.simplified = None
        self.mode = None
        self.border = None
        self.fill = None
        self.points = None
        #Non-attributes
        self.image = None #===
        self.transform = None
        self.shape = None #===
        self.processArguments(args, kwargs)
    def processArguments(self, args, kwargs):
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
            except:
                print('Could not process Contour arg: '+str(arg))
        # 2) KWARGS
        for kwarg in kwargs:
            try:
                self.update(kwarg)
            except:
                print('Could not process Contour kwarg: '+str(kwarg))
# MUTATORS
    def update(self, *args): #=== Kwargs eventually
        for arg in args:
            # Dictionary
            if type(arg) == type({}):
                for key in arg:
                    # Dict:attributes
                    if key in self.__dict__:
                        self.__dict__[key] = arg[key]
            # Transform
            elif arg.__class__.__name__ == 'Transform':
                self.transform = arg
            # Image
            elif arg.__class__.__name__ == 'Image':
                self.image = arg
# ACCESSORS
    def __eq__(self, other):
        '''Allows use of == between multiple contours.'''
        return (self.__dict__ == other.__dict__)
    def __ne__(self, other):
        '''Allows use of != between multiple contours.'''
        return (self.__dict__ != other.__dict__)
# mergeTool functions
    def popshape(self): #===
        '''Adds polygon object (shapely) to self._shape'''
        # Closed trace
        if self.closed == True:
            # If image contour, multiply pts by mag before inverting transform
            if self.image != None:
                mag = self.img.mag
                xvals = [pt[0]*mag for pt in self.points]
                yvals = [pt[1]*mag for pt in self.points]
                pts = zip(xvals,yvals)
            else:
                if len(self.points) < 3:
                    return None
                pts = self.points
            self.shape = Polygon( self.transform.worldpts(pts) )
        # Open trace
        elif self.closed == False and len(self.points)>1:
            self.shape = LineString( self.transform.worldpts(self.attributes['points']) )
        else:
            print('\nInvalid shape characteristics: '+self.name)
            print('Quit for debug')
            quit() # for dbugging
    def box(self):
        '''Returns bounding box of shape (shapely) library'''
        if self.shape != None:
            minx, miny, maxx, maxy = self.shape.bounds
            return box(minx, miny, maxx, maxy)
        else:
            print('NoneType for shape: '+self.name)
    def overlaps(self, other, threshold=(1+2**(-17))):
        '''Return 0 if no overlap.
        For closed traces: return 1 if AoU/AoI < threshold, return AoU/AoI if not < threshold
        For open traces: return 0 if # pts differs or distance between parallel pts > threshold
                         return 1 otherwise'''
        if self.shape == None:self.popshape()
        if other.shape == None:other.popshape()
        # Check bounding box
        if (not self.box().intersects(other.box()) and
            not self.box().touches(other.box()) ):
            return 0
        # Check if both same type of contour
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
# curationTool functions
    def getLength(self):
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
    def isReverse(self):
        '''Returns true if contour is a reverse trace (negative area)'''
        self.popshape()
        if self.closed:
            ring = LinearRing(self._shape.exterior.coords) # convert polygon to ring
            return not ring.is_ccw # For some reason, the opposite is true (image vs biological coordinate system?)
        else:
            return False

class Image:
    def __init__(self, *args, **kwargs):
        self.src = None
        self.mag = None
        self.contrast = None 
        self.brightness = None
        self.red = None
        self.green = None
        self.blue = None
        #Non-attributes
        self.transform = None
        self.processArguments(args, kwargs)
    def processArguments(self, args, kwargs):
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
            except:
                print('Could not process Image arg: '+str(arg))
        # 2) KWARGS
        for kwarg in kwargs:
            try:
                self.update(kwarg)
            except:
                print('Could not process Image kwarg: '+str(kwarg)) 
# MUTATORS  
    def update(self, *args): #=== **kwargs eventually
        '''Changes Section data from arguments.'''
        for arg in args:
            # Dictionary  
            if type(arg) == type({}):
                for key in arg:
                    # Dict:Attribute
                    if key in self.__dict__:
                        self.__dict__[key] = arg[key]
                    # Dict:Transform
                    elif arg[key].__class__.__name__ == 'Transform':
                        self.transform = arg[key]
            # Transform object
            elif arg.__class__.__name__ == 'Transform':
                self.transform = arg
# ACCESSORS
    def __eq__(self, other):
        return (self.transform == other.transform or
                self.src == other.src)
    def __ne__(self, other):
        return (self.transform != other.transform or
                self.src != other.src)   

class Section:
    def __init__(self, *args, **kwargs):
        self.index = None
        self.thickness = None
        self.alignLocked = None
        #Non-attributes
        self.image = None
        self.contours = None
        self.processArguments(args, kwargs)
    def processArguments(self, args, kwargs):
        '''Populates data from the *args and **kwargs arguments via self.update.'''
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
            except:
                print('Could not process Section arg: '+str(arg))

        # 2) KWARGS #===
        for kwarg in kwargs:
            try:
                self.update(kwarg)
            except:
                print('Could not process Section kwarg: '+str(kwarg))
# MUTATORS
    def update(self, *args): #=== **kwargs eventually, need a way to choose overwrite or append to contours
        '''Changes Section data from arguments. Assesses type of argument then determines where to place it.'''
        for arg in args: # Assess type
            # Dictionary argument
            if type(arg) == type({}):
                for key in arg:
                    # Dict:Attribute
                    if key in self.__dict__:
                        self.__dict__[key] = arg[key]
                    # Dict:List
                    elif type(arg[key]) == type([]):
                        for item in arg[key]:
                            if item.__class__.__name__ == 'Image':
                                self.image = item
                            elif item.__class__.__name__ == 'Contour':
                                if self.contours == None:
                                    self.contours == []
                                self.contours.append(item)
                    # Dict:Image
                    elif arg[key].__class__.__name__ == 'Image':
                        self.image = arg[key]
                    # Dict:Contour
                    elif arg[key].__class__.__name__ == 'Contour':
                        if self.contours == None:
                            self.contours == []
                        self.contours.append(arg[key])
            
            # String argument
            elif type(arg) == type(''): # Possible path to XML?
                self.update(*xml.process(arg))
            
            # Contour argument
            elif arg.__class__.__name__ == 'Contour':
                if self.contours == None:
                    self.contours = []
                self.contours.append(arg)
            
            # Image argument
            elif arg.__class__.__name__ == 'Image':
                self.image = arg
            
            # List argument
            elif type(arg) == type([]):
                for item in arg:
                    if item.__class__.__name__ == 'Contour':
                        if self.contours == None:
                            self.contours = []
                        self.contours.append(item)
                    elif item.__class__.__name__ == 'Image':
                        self.image = item
# ACCESSORS
    def __len__(self):
        '''Return number of contours in Section object'''
        return len(self.contours)
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        return self.__dict__ == other.__dict__
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return self.__dict__ != other.__dict__

class Series: #===
    def __init__(self, *args, **kwargs):
        self.name = None
        self.index = None
        self.viewport = None
        self.units = None
        self.autoSaveSeries = None
        self.autoSaveSection =  None
        self.warnSaveSection = None
        self.beepDeleting = None
        self.beepPaging = None
        self.hideTraces = None
        self.unhideTraces = None
        self.hideDomains = None
        self.unhideDomains = None
        self.useAbsolutePaths = None
        self.defaultThickness = None
        self.zMidSection = None
        self.thumbWidth = None
        self.thumbHeight = None
        self.fitThumbSections = None
        self.firstThumbSection = None
        self.lastThumbSection = None
        self.skipSections = None
        self.displayThumbContours = None
        self.useFlipbookStyle = None
        self.flipRate = None
        self.useProxies = None
        self.widthUseProxies = None
        self.heightUseProxies = None
        self.scaleProxies = None
        self.significantDigits = None
        self.defaultBorder = None
        self.defaultFill = None
        self.defaultMode = None
        self.defaultName = None
        self.defaultComment = None
        self.listSectionThickness = None
        self.listDomainSource = None
        self.listDomainPixelsize = None
        self.listDomainLength = None
        self.listDomainArea = None
        self.listDomainMidpoint = None
        self.listTraceComment = None
        self.listTraceLength = None
        self.listTraceArea = None
        self.listTraceCentroid = None
        self.listTraceExtent = None
        self.listTraceZ = None
        self.listTraceThickness = None
        self.listObjectRange = None
        self.listObjectCount = None
        self.listObjectSurfarea = None
        self.listObjectFlatarea = None
        self.listObjectVolume = None
        self.listZTraceNote = None
        self.listZTraceRange = None
        self.listZTraceLength = None
        self.borderColors = None
        self.fillColors = None
        self.offset3D = None
        self.type3Dobject = None
        self.first3Dsection = None
        self.last3Dsection = None
        self.max3Dconnection = None
        self.upper3Dfaces = None
        self.lower3Dfaces = None
        self.faceNormals = None
        self.vertexNormals = None
        self.facets3D = None
        self.dim3D = None
        self.gridType = None
        self.gridSize = None
        self.gridDistance = None
        self.gridNumber = None
        self.hueStopWhen = None
        self.hueStopValue = None
        self.satStopWhen = None
        self.satStopValue = None
        self.brightStopWhen = None
        self.brightStopValue = None
        self.tracesStopWhen = None
        self.areaStopPercent = None
        self.areaStopSize = None
        self.ContourMaskWidth = None
        self.smoothingLength = None
        self.mvmtIncrement = None
        self.ctrlIncrement = None
        self.shiftIncrement = None
        #Non-attributes
        self.contours = None
        self.zcontours = None
        self.sections = None
        self.processArguments(args, kwargs)
    def processArguments(self, args, kwargs):
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
            except:
                print('Could not process Series arg: '+str(arg))
        # 2) KWARGS
        for kwarg in kwargs:
            try:
                self.update(kwarg)
            except:
                print('Could not process Series kwarg: '+str(kwarg))
# MUTATORS
    def update(self, *args): #=== Kwargs eventually
        for arg in args:
            # String argument
            if type(arg) == type(''): # Possible path to XML?
                self.update(*xml.process(arg))
                self.name = arg.split('/')[len(arg.split('/'))-1].replace('.ser','')
            # Dictionary
            elif type(arg) == type({}):
                for key in arg:
                    if key in self.__dict__:
                        self.__dict__[key] = arg[key]
            # List
            elif type(arg) == type([]):
                for item in arg:
                    # Contour
                    if item.__class__.__name__ == 'Contour':
                        if self.contours == None:
                            self.contours = []
                        self.contours.append(item)
                    # ZSection
                    elif item.__class__.__name__ == 'ZContour':
                        if self.zcontours == None:
                            self.zcontours = []
                        self.zcontours.append(item)
                    # Section
                    elif item.__class__.__name__ == 'Section':
                        if self.sections == None:
                            self.sections = []
                        self.sections.append(item)
            # Contour
            elif arg.__class__.__name__ == 'Contour':
                if self.contours == None:
                    self.contours = []
                self.contours.append(arg)
            # ZSection
            elif item.__class__.__name__ == 'ZContour':
                if self.zcontours == None:
                    self.zcontours = []
                self.zcontours.append(item)         
            # Section
            elif arg.__class__.__name__ == 'Section':
                if self.sections == None:
                    self.sections = []
                self.sections.append(arg)

class Transform:
    def __init__(self, *args, **kwargs):
        self.dim = None
        self.xcoef = None
        self.ycoef = None
        self._tform = None # skimage.transform._geometric.AffineTransform
        self.processArguments(args, kwargs)
    def processArguments(self, args, kwargs):
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
            except:
                print('Could not process Transform arg: '+str(arg))
        # 2) KWARGS
        for kwarg in kwargs:
            try:
                self.update(kwarg)
            except:
                print('Could not process Transform kwarg: '+str(kwarg))
# MUTATORS
    def update(self, *args): #=== Kwargs eventually
        for arg in args:
            # Dictionary
            if type(arg) == type({}):
                for key in arg:
                    if key in self.__dict__:
                        self.__dict__[key] = arg[key]
                # Recreate self._tform everytime attributes is updated
                self._tform = self.tform()
            # self._tform (skimage.transform._geometric.AffineTransform)
            elif arg.__class__.__name__ == 'AffineTransform':
                self._tform = arg
# ACCESSORS
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __ne__(self, other):
        return self.__dict__ != other.__dict__
    def worldpts(self, points):
        '''Returns inverse points'''
        newpts = self._tform.inverse(np.asarray(points))
        return list(map(tuple,newpts))
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
    
    # MUTATORS             
    def tform(self):
        '''Creates self._tform variable which represents the transform'''
        xcoef = self.xcoef
        ycoef = self.ycoef
        dim = self.dim
        if xcoef == None or ycoef == None or dim == None:
            return None
        a = xcoef
        b = ycoef
        # Affine transform
        if dim in range(0,4):
            if dim == 0: 
                tmatrix = np.array( [1,0,0,0,1,0,0,0,1] ).reshape((3,3))
            elif dim == 1:
                tmatrix = np.array( [1,0,a[0],0,1,b[0],0,0,1] ).reshape((3,3))
            elif dim == 2: # Special case, swap b[1] and b[2] (look at original Reconstruct code: nform.cpp)
                tmatrix = np.array( [a[1],0,a[0],0,b[1],b[0],0,0,1] ).reshape((3,3))
            elif dim == 3:
                tmatrix = np.array( [a[1],a[2],a[0],b[1],b[2],b[0],0,0,1] ).reshape((3,3))
            return tf.AffineTransform(tmatrix)
        # Polynomial transform
        elif dim in range(4,7):
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

class ZContour: #===
    def __init__(self, *args, **kwargs):
        self.name = None
        self.closed = None
        self.border = None
        self.fill = None
        self.mode = None 
        self.points = None
        self.processArguments(args, kwargs)
    def processArguments(self, args, kwargs):
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
            except:
                print('Could not process ZContour arg: '+str(arg))
        # 2) KWARGS
        for kwarg in kwargs:
            try:
                self.update(kwarg)
            except:
                print('Could not process ZContour kwarg: '+str(kwarg))
    def update(self, *args): #=== KWARGS eventually
        for arg in args:
            # Dictionary
            if type(arg) == type({}):
                for key in arg:
                    # Dict:attributes
                    if key in self.__dict__:
                        self.__dict__[key] = arg[key]
