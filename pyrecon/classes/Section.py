"""Section."""


class Section(object):
    """Class representing a RECONSTRUCT Section."""

    def __init__(self):
        """Apply given keyword arguments as instance attributes."""
        self.name = None  # Series name + index
        self.index = None
        self.thickness = None
        self.alignLocked = None
        # Non-attributes
        self.images = []  # TODO: d1fixed
        self.contours = []
        self._path = None

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
