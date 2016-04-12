"""Image."""


class Image(object):
    """Class representing a RECONSTRUCT Image."""

    def __init__(self, *args, **kwargs):
        """Apply given keyword arguments as instance attributes."""
        self.src = None
        self.mag = None
        self.contrast = None
        self.brightness = None
        self.red = None
        self.green = None
        self.blue = None
        # Non-attributes
        self.contour = None  # TODO: d1fixed
        self._path = None
        self.processArguments(args, kwargs)

    def processArguments(self, args, kwargs):
        """Apply any custom args/kwargs to the instance."""
        # 1) ARGS
        for arg in args:
            try:
                self.update(arg)
            except Exception as e:
                print "Could not process Contour arg:{}\n\t".format(
                    str(arg) + str(e))
        # 2) KWARGS
        for kwarg in kwargs:
            try:
                self.update(kwarg)
            except Exception as e:
                print "Could not process Contour kwarg:{}\n\t".format(
                    str(kwarg) + str(e))

# MUTATORS
    def update(self, *args):  # TODO: **kwargs eventually
        """Change Section data from arguments."""
        for arg in args:
            # Dictionary
            if isinstance(arg, dict):
                for key in arg:
                    # Dict:Attribute
                    if key in self.__dict__:
                        self.__dict__[key] = arg[key]
                    # Dict:Transform
                    elif arg[key].__class__.__name__ == "Contour":
                        self.contour = arg[key]
            # Transform object
            elif arg.__class__.__name__ == "Transform":
                self.contour = arg

# ACCESSORS
    def __eq__(self, other):
        """Allow use of == operator."""
        return (self.contour == other.contour and
                self.src == other.src and
                self.brightness == other.brightness and
                self.contrast == other.contrast)

    def __ne__(self, other):
        """Allow use of != operator."""
        return not self.__eq__(other)

    def attributes(self):
        """Return relevent attributes as dict."""
        return {
            "src": self.src,
            "mag": self.mag,
            "contrast": self.contrast,
            "brightness": self.brightness,
            "path": ("" if self._path is None else self._path) + self.src
        }
