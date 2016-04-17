"""ZContour."""
import math


class ZContour(object):
    """Class representing a RECONSTRUCT ZContour."""

    def __init__(self, **kwargs):
        """Assign instance attributes from args/kwargs."""
        self.name = kwargs.get("name")
        self.closed = kwargs.get("closed")
        self.border = kwargs.get("border")
        self.fill = kwargs.get("fill")
        self.mode = kwargs.get("mode")
        self.points = kwargs.get("points", [])

    def __eq__(self, other):
        """Allow use of == operator."""
        to_compare = ["name", "points", "closed"]
        for k in to_compare:
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __ne__(self, other):
        """Allow use of != operator."""
        return not self.__eq__(other)

    # mergeTool Functions
    def overlaps(self, other, threshold=(1 + 2**(-17))):
        """Return 1 or 0 of whether ZContour overlaps other."""
        def distance(pt0, pt1):
            """Distance formula: return distance between two points."""
            x0, y0 = pt0
            x1, y1 = pt1
            return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
        # Check equal # pts
        if len(self.points) != len(other.points):
            return 0
        # Build list of min distance between pts
        distlist = []
        for pt in self.points:
            ptdistances = []
            for pt2 in other.points:
                if pt[2] == pt2[2]:  # if in same section
                    dist = distance(pt[0:2], pt[0:2])
                    ptdistances.append(dist)
            if len(ptdistances) != 0:
                distlist.append(min(ptdistances))
        # check for any distances above threshold
        for dist in distlist:
            if dist > threshold:  # no matching point
                return 0
        return 1
