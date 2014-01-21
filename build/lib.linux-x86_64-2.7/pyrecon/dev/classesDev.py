from pyrecon.dev import handleXML as xml
class Section:
    '''Object representing a Section.'''
# CONSTRUCTOR - Construct Section object from arguments
    def __init__(self, *args, **kwargs): #=== start with path to xml file as only input option
        # Create empty Section
        self.attributes = None
        self.image = None
        self.contours = None
        # Process arguments to create populated Section
        self.processArguments(args, kwargs)

    def processArguments(self, args, kwargs): #===
        '''Process input from __init__()'''
        try: #===
            self.popFromPath(args[0]) #=== only option for now
        except: #===
            print('Could not process arguments. Empty Section returned.')

    def popFromPath(self, path):
        '''Update the sections data via supplied path to XML file'''
        self.attributes, self.image, self.contours = xml.process(path)

# MUTATORS - Change data in object

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

