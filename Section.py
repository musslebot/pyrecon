from Transform import *
from Image import *
from Contour import *
from ZContour import *
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
        
        self.checkMultImgs()
        
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
            