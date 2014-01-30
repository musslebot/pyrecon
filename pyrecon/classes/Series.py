class Series: #===
    def __init__(self, *args, **kwargs):
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
        self.name = None
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
                import pyrecon.tools.handleXML as xml
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
            elif arg.__class__.__name__ == 'ZContour':
                if self.zcontours == None:
                    self.zcontours = []
                self.zcontours.append(item)         
            # Section
            elif arg.__class__.__name__ == 'Section':
                if self.sections == None:
                    self.sections = []
                self.sections.append(arg)
# ACCESSORS