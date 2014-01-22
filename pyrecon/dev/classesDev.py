import os, re, math
import numpy as np
from pyrecon.dev import handleXML as xml
from shapely.geometry import Polygon, LineString, box, LinearRing
from skimage import transform as tf
from collections import OrderedDict

class Image:
    def __init__(self, *args, **kwargs):
        self.attributes = {
            'src':None,
            'mag':None,
            'contrast':None, 
            'brightness':None,
            'red':None,
            'green':None,
            'blue':None
        }
        self.transform = None

        self.processArguments(args, kwargs)
    
    def processArguments(self, args, kwargs):
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
            except:
                print('Could not process arguments. Empty Image returned.')
        # 2) KWARGS #===
        return
     
    def update(self, *args, **kwargs): #===
        '''Changes Section data from arguments.'''
        for arg in args:
            # Attribute dictionary
            if type(arg) == type({}):
                for key in arg:
                    if key in self.attributes:
                        self.attributes[key] = arg[key]
            # Transform object #===
            elif arg.__class__.__name__ == 'Transform':
                self.transform = arg
            else:
                print('Non dict argument Image.update()')
        #=== MANAGE KWARGS

    # ACCESSORS
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        return (self.transform == other.transform or
                self.src == other.src)
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return (self.transform != other.transform or
                self.src != other.src)   

    # MUTATORS

class Section:
    '''Object representing a Section.'''
    # CONSTRUCTOR - Construct Section object from arguments
    def __init__(self, *args, **kwargs):
        '''First creates an empty Section. Next, processes *args and **kwargs to determine best method for populating data (more detail in processArguments().'''
        # Create empty Section
        self.attributes = {
            'index':None,
            'thickness':None, #===
            'alignLocked':None
        }
        self.image = None #===
        self.contours = None #===
        
        # Process arguments to update Section data
        self.processArguments(args, kwargs)

    def processArguments(self, args, kwargs): #===
        '''Populates data from the *args and **kwargs arguments. If a path to an XML file is given, it will take precedence and ignore other arguments. If all of the data is not present in the XML file, the other arguments will then be processed to locate the missing data. Any data not found will result in None for that data label.'''
        # 1) ARGS
        for arg in args:
            if type(arg) == type(''): # Possible path?
                try:
                    self.update(*xml.process(arg)) #=== only option for now
                except:
                    print('Could not process arguments. Empty Section returned.')
        # 2) KWARGS
    
    def update(self, *args, **kwargs): #===
        '''Changes Section data from arguments.'''
        for arg in args:
            print('Arg: '+str(arg)) #===
            if type(arg) == type({}):
                print('--> dictionary') #===
                for key in arg:
                    if key in self.attributes:
                        self.attributes[key] = arg[key]
            # elif type(arg) == type(Image()): #===?
                # return
            elif type(arg) == type([]): # List arguments: contours
                self.contours = arg #=== temporary, check for Contours 
        #=== MANAGE KWARGS

    # ACCESSORS - Make accessing data in object easier      
    def __len__(self):
        '''Return number of contours in Section object'''
        return len(self.contours)
    def __getitem__(self,x):
        '''Return <x> associated with Section object'''
        if type(x) == type(''): # If string
            try: #... return attribute of name 'x'
                return self.attributes[x]
            except:
                try: #... return contour with name 'x'
                    return self.contours[x] #=== should be name, not index
                except:
                    print ('Unable to find '+x+ ' (str)')
        elif type(x) == type(int(0)):
            try: #... return xth index in contours
                return self.contours[x]
            except:
                print ('Unable to find '+x+' (int)')
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        return self.output() == other.output()
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return self.output() != other.output()

class Transform:
    def __init__(self, *args, **kwargs):
        self.attributes = {
            'dim':None,
            'xcoef':None,
            'ycoef':None
        }
        self._tform = None # skimage.transform._geometric.AffineTransform
        self.processArguments(args, kwargs)

    def processArguments(self, args, kwargs):
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
                break #=== if no Nones, else try other stuff?
            except:
                print('Could not process arguments. Empty Transform returned.')
        # 2) KWARGS #===

    def update(self, *args, **kwargs):
        for arg in args:
            if type(arg) == type({}):
                for key in arg:
                    if key in self.attributes:
                        self.attributes[key] = arg[key]
            # Other argument types: transform object? image? contour? zcontour? #===
        self._tform = self.tform()

    # ACCESSORS
    def __eq__(self, other):
        '''Allows use of == between multiple objects'''
        return self.output() == other.output()
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        return self.output() != other.output()
    def worldpts(self, points):
        '''Returns inverse points'''
        newpts = self._tform.inverse(np.asarray(points))
        return list(map(tuple,newpts))
    def imgpts(self, points): #===
        '''Returns imgpts'''
        return
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
        xcoef = self.attributes['xcoef']
        ycoef = self.attributes['ycoef']
        dim = self.attributes['dim']
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