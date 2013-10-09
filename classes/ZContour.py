import math
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
    def overlaps(self, other): #===
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
    def output(self): #===
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