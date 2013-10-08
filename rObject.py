import operator
class rObject:
    '''rObject contain information for reconstruct objects that requires computation over multiple sections'''
    def __init__(self, name=None, series=None, tag=None):
        self.name = name
        self.series = series
        self.tag = tag
        self.type = self.popTraceType()
        self.start, self.end, self.count = self.popStartendCount()
        self.volume = self.popVolume()
        self.totalvolume = self.popTotalVolume()
        self.surfacearea = self.popSurfaceArea()
        self.flatarea =  self.popFlatArea()
        self.children = [] # actual children rObjects
           
    def __getitem__(self, index):
        if type(index) == str:
            return self.children[operator.indexOf(self.childrenNames(),index)]
        elif type(index) == int:
            return self.children[index]
        else:
            return None
        
    def __str__(self):
        return 'rObject, from series '+self.series.name+', with the name '+str(self.name)
    
    def childrenNames(self):
        return [child.name for child in self.children]

    def returnAtts(self):
        return self.name, self.start, self.end, self.count, self.volume, self.surfacearea, self.flatarea
    
    def returnChildren(self):
        return self.children
    
    def popTraceType(self):
        '''Returns the base trace type (e.g. 'd[0-9][0-9]cfa[0-9][0-9]' to be used for regexp)'''
        trace_expression = ''
        for character in self.name:
            if character.isdigit():
                character = '[0-9]'
            trace_expression+=character
        if trace_expression[-1].isalpha():
            trace_expression = trace_expression[:-1]
        return trace_expression
    
    def popStartendCount(self):
        return self.series.getStartEndCount( self.name )
    
    def popVolume(self):
        return self.series.getVolume( self.name )

    def popTotalVolume(self):
        return self.series.getTotalVolume( self.name )

    def popSurfaceArea(self):
        return self.series.getSurfaceArea( self.name )
        
    def popFlatArea(self):
        return self.series.getFlatArea( self.name )