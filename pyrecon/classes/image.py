"""Image."""


class Image(object):
    """Class representing a RECONSTRUCT Image."""

    def __init__(self):
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
