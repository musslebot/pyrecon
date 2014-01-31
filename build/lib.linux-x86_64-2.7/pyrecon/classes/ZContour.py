class ZContour:
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