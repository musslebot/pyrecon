"""Section."""
import os


class Section(object):
    """Class representing a RECONSTRUCT Section."""

    def __init__(self, *args, **kwargs):
        """Apply given keyword arguments as instance attributes."""
        self.name = None  # Series name + index
        self.index = None
        self.thickness = None
        self.alignLocked = None
        # Non-attributes
        self.images = []  # TODO: d1fixed
        self.contours = []
        self._path = None
        self.processArguments(args, kwargs)

    def processArguments(self, args, kwargs):
        """Populate instance data from args and kwargs arguments."""
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
            except Exception as e:
                print "Could not process Section arg: {}\n\t".format(
                    str(arg) + str(e))
        # 2) KWARGS  # TODO
        for kwarg in kwargs:
            try:
                self.update(kwarg)
            except Exception as e:
                print "Could not process Section kwarg: {}\n\t".format(
                    str(kwarg) + str(e))

# MUTATORS
    def update(self, *args):  # TODO: **kwargs eventually
        """Update instance attributes from arbitrary input."""
        for arg in args:  # Assess type
            # Dictionary argument
            if isinstance(arg, dict):
                for key in arg:
                    # Dict:Attribute
                    if key in self.__dict__:
                        self.__dict__[key] = arg[key]
                    # Dict:List
                    elif isinstance(arg[key], list):
                        for item in arg[key]:
                            if item.__class__.__name__ == 'Image':
                                self.images.append(item)
                            elif item.__class__.__name__ == 'Contour':
                                self.contours.append(item)
                    # Dict:Image
                    elif arg[key].__class__.__name__ == 'Image':
                        self.images.append(arg[key])  # TODO: d1fixed
                    # Dict:Contour
                    elif arg[key].__class__.__name__ == 'Contour':
                        self.contours.append(arg[key])
            # String argument
            elif isinstance(arg, str):  # Possible path to XML?
                import pyrecon.tools.handleXML as xml
                self.update(*xml.process(arg))
                self.name = arg.split('/')[-1]
                self._path = os.path.dirname(arg)
                if self._path[-1] != '/':
                    self._path += '/'
            # Contour argument
            elif arg.__class__.__name__ == 'Contour':
                self.contours.append(arg)
            # Image argument
            elif arg.__class__.__name__ == 'Image':
                self.images.append(arg)  # TODO: d1fixed
            # List argument
            elif isinstance(arg, list):
                for item in arg:
                    if item.__class__.__name__ == 'Contour':
                        self.contours.append(item)
                    elif item.__class__.__name__ == 'Image':
                        self.images.append(item)
        for img in self.images:
            img._path = self._path

    def popShapes(self):
        """Populate each Contour, in this Section, with a shape object."""
        for contour in self.contours:
            contour.popShape()

# ACCESSORS
    def __len__(self):
        """Return number of contours in Section object."""
        return len(self.contours)

    def __eq__(self, other):  # TODO: images eval correctly?
        """Allow use of == between multiple objects."""
        return (self.thickness == other.thickness and
                self.index == other.thickness and
                self.alignLocked == other.alignLocked and
                self.images == other.images and  # TODO: d1fixed
                self.contours == other.contours)

    def __ne__(self, other):
        """Allow use of != between multiple objects."""
        return not self.__eq__(other)

    def eq(self, other, eq_type=None):  # TODO
        """
        Check equivalency with the option for type of attributes to compare.

        Default: __eq__
        """
        if not eq_type:
            return self.__eq__(other)
        elif eq_type.lower() == 'attributes':
            return (self.thickness == other.thickness and
                    self.index == other.index and
                    self.alignLocked == other.alignLocked)
        elif eq_type.lower() in ['images', 'image', 'img']:
            return (self.images == other.images)  # TODO: d1fixed
        elif eq_type.lower() in ['contours', 'contour']:
            return (self.contours == other.contours)

    def attributes(self):
        """Return a dict of this Section's attributes."""
        return {
            "name": self.name,
            "index": self.index,
            "thickness": self.thickness,
            "alignLocked": self.alignLocked
        }
