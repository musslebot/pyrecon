"""ZContour."""
import math


class ZContour(object):
    """Class representing a RECONSTRUCT ZContour."""

    def __init__(self):
        """Assign instance attributes from args/kwargs."""
        self.name = None
        self.closed = None
        self.border = None
        self.fill = None
        self.mode = None
        self.points = None

    def __eq__(self, other):
        """Allow use of == operator."""
        return (self.name == other.name and
                self.points == other.points and
                self.closed == other.closed)

    def __ne__(self, other):
        """Allow use of != operator."""
        return not self.__eq__(other)

    # mergeTool Functions
    def overlaps(self, other, threshold=(1 + 2**(-17))):
        """Return 1 or 0 of whether ZContour overlaps other."""
        def distance(pt0, pt1):
            """Distance formula: return distance between two points."""
            return math.sqrt((pt0[0] - pt1[0])**2 + (pt0[1] - pt1[1])**2)
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
