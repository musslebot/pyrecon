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
        self._path = None
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
        return (self.transform == other.transform and
                self.src == other.src and
                self.brightness == other.brightness and
                self.contrast == other.contrast)
    def __ne__(self, other):
        return (self.transform != other.transform or
                self.src != other.src or
                self.brightness != other.brightness or
                self.contrast != other.contrast)  