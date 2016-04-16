"""Image."""


class Image(object):
    """Class representing a RECONSTRUCT Image."""

    def __init__(self, **kwargs):
        """Apply given keyword arguments as instance attributes."""
        self.src = kwargs.get("src")
        self.mag = kwargs.get("mag")
        self.contrast = kwargs.get("contrast")
        self.brightness = kwargs.get("brightness")
        self.red = kwargs.get("red")
        self.green = kwargs.get("green")
        self.blue = kwargs.get("blue")
        # Non-attributes
        self.contour = kwargs.get("contour")  # TODO: d1fixe
        self._path = kwargs.get("_path")

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
