import pyrecon.tools.handleXML as xml

class Section:
    def __init__(self, *args, **kwargs):
        self.name = None # Series name + index
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
                self.name = arg.split('/')[-1]
            
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