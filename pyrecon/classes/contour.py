"""Contour."""
import math

from shapely.geometry import box, LinearRing, LineString, Point, Polygon


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
        self.points = kwargs.get("points", [])
        # Non-attributes
        self.coordSys = kwargs.get("coordSys")
        self.image = kwargs.get("image")  # Only used if image contour
        self.transform = kwargs.get("transform")
        self.shape = kwargs.get("shape")

    def __eq__(self, other):
        """Allow use of == between multiple contours."""
        ignore = ['shape', 'comment', 'hidden', 'image']

        comparison_dict1 = {}
        for key in self.__dict__:
            if key not in ignore:
                comparison_dict1[key] = self.__dict__[key]

        comparison_dict2 = {}
        for key in other.__dict__:
            if key not in ignore:
                comparison_dict2[key] = other.__dict__[key]
        return (comparison_dict1 == comparison_dict2)

    def __ne__(self, other):
        """Allow use of != between multiple contours."""
        return not self.__eq__(other)

# transform/shape operations
    def convertToBioCoords(self, mag):
        """Convert points to biological coordinate system and update shape."""
        if self.coordSys == 'bio':
            return 'Already in biological coordinate system -- abort.'
        self.points = self.transform.worldpts(self.points, mag)
        self.coordSys = 'bio'
        self.popShape()  # repopulate shape

    def convertToPixCoords(self, mag):
        """Convert points to pixel coordinate system and update shape."""
        if self.coordSys == 'pix':
            return 'Already in pixel coordinate system -- abort.'
        self.points = self.transform.imagepts(self.points, mag)
        self.coordSys = 'pix'
        self.popShape()  # repopulate shape

    def popShape(self):
        """Add a Shapely geometric object to self._shape."""
        # Closed trace
        if self.closed is True:
            # If image contour, multiply pts by mag before inverting transform
            if self.image.__class__.__name__ == 'Image':
                mag = self.image.mag
                xvals = [pt[0] * mag for pt in self.points]
                yvals = [pt[1] * mag for pt in self.points]
                pts = zip(xvals, yvals)
            else:
                if len(self.points) < 3:
                    return None
                pts = self.points
            self.shape = Polygon(self.transform.worldpts(pts))  # TODO
        # Open trace
        elif self.closed is False and len(self.points) > 1:
            self.shape = LineString(
                self.transform.worldpts(self.points))  # TODO
        elif self.closed is False and len(self.points) == 1:
            self.shape = Point(
                self.transform.worldpts(self.points))
        else:
            # TODO: raise Exception
            print("\nInvalid shape characteristics: {}".format(self.name))
            print ("Quit for debug")
            quit()  # for dbugging

    def bounding_box(self):
        """Return bounding box of shape (shapely) library."""
        if self.shape:
            minx, miny, maxx, maxy = self.shape.bounds
            return box(minx, miny, maxx, maxy)
        else:
            print "NoneType for shape: ".format(self.name)

# mergeTool functions
    def overlaps(self, other, threshold=(1 + 2**(-17))):
        """Return 0 if no overlap.

        For closed traces:
            * 1 if area_of_union/area_of_intersection < threshold,
            * area_of_union/area_of_intersection if not < threshold
        For open traces:
            * 0 if # pts differs or distance between parallel pts > threshold
            * 1 otherwise
        """
        if not self.shape:
            self.popShape()
        if not other.shape:
            other.popShape()
        # Check bounding box (reduces comp. time for non-overlapping contours)
        this_box = self.bounding_box()
        other_box = other.bounding_box()
        if not this_box.intersects(other_box) and \
                not this_box.touches(other_box):
            return 0
        # Check if both same type of contour
        if self.closed != other.closed:
            return 0
        # Closed contours
        if self.closed:
            # check if both are consistent directions (cw/ccw) to prevent
            # reverse contours from conflicting with normal ones
            if self.isReverse() != other.isReverse():
                return 0
            area_of_union = self.shape.union(other.shape).area
            area_of_intersection = self.shape.intersection(other.shape).area
            if area_of_intersection == 0:
                return 0
            elif area_of_union / area_of_intersection >= threshold:  # TODO
                # Returns actual value, not 0 or 1
                return area_of_union / area_of_intersection
            elif area_of_union / area_of_intersection < threshold:
                return 1
        # Open contours
        if not self.closed:
            if len(self.points) != len(other.points):
                return 0

            def distance(pt0, pt1):
                return math.sqrt((pt0[0] - pt1[0])**2 + (pt0[1] - pt1[1])**2)

            # Lists of world coords to compare
            a = self.transform.worldpts(self.points)
            b = other.transform.worldpts(other.points)
            distlist = [distance(a[i], b[i]) for i in range(len(self.points))]
            for elem in distlist:
                if elem > threshold:
                    return 0
        return 1

# curationTool functions
    def getLength(self):
        """Return the sum of all line segments in the contour object."""
        length = 0
        for index in range(len(self.points)):
            if index + 1 >= len(self.points):
                # stop when outside index range
                break
            pt = self.points[index]
            next_pt = self.points[index + 1]
            length += (((next_pt[0] - pt[0])**2) + ((next_pt[1] - pt[1])**2))**(0.5)
        if self.closed:
            # If closed object, add distance between 1st and last pt too
            length += (((self.points[0][0] - self.points[-1][0])**2) + ((self.points[0][1] - self.points[-1][1])**2))**(0.5)
        # TODO: sqrt is taxing computation; reimplement with 1 sqrt at end?
        return length

    def isReverse(self):
        """Return true if contour is a reverse trace (negative area).

        * Uses name to determine same Contour in different Sections
        """
        if not self.shape:
            self.popShape()
        if self.closed:
            # convert polygon to ring
            # For some reason, the opposite is true (image vs biological
            # coordinate system?)
            ring = LinearRing(self.shape.exterior.coords)
            return not ring.is_ccw
        else:
            return False

    def isInvalid(self):
        """Return true if this is an invalid Contour."""
        if self.closed and len(self.points) < 3:
            return True
