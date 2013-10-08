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
        return self.transform == other.transform or self.src == other.src
    def __ne__(self, other):
        '''Allows use of != between multiple objects'''
        if other == None:
            return True
#         return self.output() != other.output()
        return self.transform != other.transform or self.src != other.src
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