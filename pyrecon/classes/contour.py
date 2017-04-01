"""Contour."""
import numpy
from shapely.geometry import LineString, Point, Polygon


class Contour(object):
    """Class representing a RECONSTRUCT Contour."""

    def __init__(self, **kwargs):
        """Apply given keyword arguments as instance attributes."""
        self.name = kwargs.get("name")
        self.comment = kwargs.get("comment")
        self.hidden = kwargs.get("hidden")
        self.closed = kwargs.get("closed")
        self.simplified = kwargs.get("simplified")
        self.mode = kwargs.get("mode")
        self.border = kwargs.get("border")
        self.fill = kwargs.get("fill")
        self.points = list(kwargs.get("points", []))
        # Non-RECONSTRUCT attributes
        self.transform = kwargs.get("transform")

    def __repr__(self):
        """Return a string representation of this Contour's data."""
        return (
            "Contour name={name} hidden={hidden} closed={closed} "
            "simplified={simplified} border={border} fill={fill} "
            "mode={mode}\npoints={points}"
        ).format(
            name=self.name,
            hidden=self.hidden,
            closed=self.closed,
            simplified=self.simplified,
            border=self.border,
            fill=self.fill,
            mode=self.mode,
            points=self.points,
        )

    def __eq__(self, other):
        """Allow use of == between multiple contours."""
        to_compare = ["name", "closed", "simplified", "mode", "border", "fill",
                      "points", "transform"]
        for k in to_compare:
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __ne__(self, other):
        """Allow use of != between multiple contours."""
        return not self.__eq__(other)

    @property
    def shape(self):
        """Return a Shapely geometric object."""
        if not self.points:
            raise Exception("No points found: {}".format(self))

        # Normalize points
        array = numpy.asarray(list(self.points))
        normalized_points = self.transform._tform.inverse(array)
        self.normalized_points = normalized_points

        if len(normalized_points) == 1:
            return Point(*normalized_points)
        elif len(normalized_points) == 2:
            return LineString(normalized_points)
        elif self.closed is True:
            # Check for weird, invalid traces
            if (len(normalized_points) == 3 or \
                    len (normalized_points) == 4 ) and self.points[0] == self.points[2]:
                return LineString(normalized_points)
            # Closed trace
            return Polygon(normalized_points)
            # TODO: do I need to handle this?
            # If image contour, multiply pts by mag before inverting transform
            # if self.image.__class__.__name__ == 'Image':
            #     mag = self.image.mag
            #     xvals = [pt[0] * mag for pt in normalized_points]
            #     yvals = [pt[1] * mag for pt in normalized_points]
            #     pts = zip(xvals, yvals)
            # else:
        elif self.closed is False:
            return LineString(normalized_points)
        else:
            raise Exception("Could not deduce shape for: {}".format(self))
