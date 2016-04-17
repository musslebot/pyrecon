"""Merge two RECONSTRUCT datasets."""
from shapely.geometry import box, LinearRing, LineString, Point, Polygon

from pyrecon.classes import Series, Section
from pyrecon.tools import reconstruct_writer


def get_bounding_box(shape):
    """Return bounding box of shapely shape."""
    minx, miny, maxx, maxy = shape.bounds
    return box(minx, miny, maxx, maxy)


def is_reverse(shape):
    """Return True if shape is a RECONSTRUCT reverse trace (negative area)."""
    if isinstance(shape, Polygon):
        ring = LinearRing(shape.exterior.coords)
        # RECONSTRUCT is opposite for some reason
        return not ring.is_ccw
    return False


def overlaps(shape1, shape2, threshold=(1 + 2**(-17))):
    """Return 0 if no overlap.

    For closed traces:
        * 1 if area_of_union/area_of_intersection < threshold,
        * area_of_union/area_of_intersection if not < threshold
    For open traces:
        * 0 if # pts differs or distance between parallel pts > threshold
        * 1 otherwise
    """
    if shape1.type != shape2.type:
        return 0

    if isinstance(shape1, Point) and shape1.equals(shape2):
        return 1

    # Check bounding box first (least expensive)
    this_box = box(*shape1.bounds)
    other_box = box(*shape2.bounds)
    if not this_box.intersects(other_box) and not this_box.touches(other_box):
        return 0

    if isinstance(shape1, Polygon):
        # CCW should not count as CW dupe
        if is_reverse(shape1) != is_reverse(shape2):
            return 0

        area_of_union = shape1.union(shape2).area
        area_of_intersection = shape1.intersection(shape2).area
        if area_of_intersection == 0:
            return 0

        elif area_of_union / area_of_intersection >= threshold:
            # TODO: try shape1.almost_equals(shape2, decimal=11.698970004)
            #     solve for x, 0.5*(10**-x) = 1*(10**-12)
            #     (11log(2)+12log(5))/(log(2)+log(5))
            # # TODO: Returns actual value, not 0 or 1 (this is dumb)
            return area_of_union / area_of_intersection

        elif area_of_union / area_of_intersection < threshold:
            return 1

    if isinstance(shape1, LineString):
        if not shape1.equals(shape2):
            return 0

    return 1


def createMergeSet(series1, series2):  # TODO: needs multithreading
    """This function takes in two Series objects and returns a MergeSet to be used for the mergeTool"""
    m_ser = MergeSeries(
        name=series1.name,
        series1=series1,
        series2=series2,
    )
    m_secs = []
    for i in range(len(series1.sections)):
        section1 = series1.sections[i]
        section2 = series2.sections[i]
        if section1.index == section2.index:
            merge_section = MergeSection(
                name=section1.name,
                section1=section1,
                section2=section2,
            )
            m_secs.append(merge_section)
        else:
            raise Exception("Series do not have matching section indices! Aborting createMergeSet()!")
    return MergeSet(
        name=m_ser.name,
        merge_series=m_ser,
        section_merges=m_secs,
    )


class MergeSet(object):
    """Class for merging data Series and Section data."""

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.seriesMerge = kwargs.get("merge_series")
        self.sectionMerges = kwargs.get("section_merges", [])

    def isDone(self):
        sections_done = True
        for section in self.sectionMerges:
            if not section.isDone():
                sections_done = False
                break
        return (self.seriesMerge.isDone() and sections_done)

    def writeMergeSet(self, outpath):  # TODO
        """Writes self.seriesMerge and self.sectionMerges to XML"""
        merged_series = self.seriesMerge.toSeries()
        merged_series.name = self.seriesMerge.name.replace(".ser", "")
        for mergeSec in self.sectionMerges:  # TODO
            merged_series.sections.append(mergeSec.toSection())
        reconstruct_writer.write_series(merged_series, outpath, sections=True)
        print "Done!"  # TODO


class MergeSection(object):
    """Class for merging together 2 Sections."""

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")

        # Sections to be merged
        self.section1 = kwargs.get("section1")
        self.section2 = kwargs.get("section2")

        # Merged stuff
        self.attributes = None
        self.images = None
        self.contours = None

        # Contours conflict resolution stuff
        self.uniqueA = None
        self.uniqueB = None
        self.compOvlps = None
        self.confOvlps = None

        self.checkConflicts()

    def checkConflicts(self):  # TODO
        """Automatically sets merged stuff if they are equivalent"""
        # Are attributes equivalent?
        if self.section1.attributes() == self.section2.attributes():
            self.attributes = self.section1.attributes()
        # Are images equivalent?
        if (len(self.section1.images) == len(self.section2.images) and
            self.section1.images[-1] == self.section2.images[-1]):
            self.images = self.section1.images  # TODO: problematic if other images are different
        # Are contours equivalent?
        separated_contours = self.getCategorizedContours(overlaps=True)  # TODO: thread this function
        self.uniqueA = separated_contours[0]
        self.uniqueB = separated_contours[1]
        self.compOvlps = separated_contours[2]
        self.confOvlps = separated_contours[3]
        if (len(self.uniqueA + self.uniqueB) == 0 and
            len(self.confOvlps) == 0):
            self.contours = self.section1.contours

    def isDone(self):
        """Boolean indicating status of merge."""
        return (self.attributes is not None and
                self.images is not None and
                self.contours is not None)

    def doneCount(self):
        """Number of resolved issues"""
        return (self.attributes is not None,
                self.images is not None,
                self.contours is not None).count(True)

    # mergeTool functions
    #=== MULTITHREAD THIS FUNCTION!!!!!!!
    def getCategorizedContours(self, threshold=(1 + 2**(-17)), sameName=True, overlaps=False):
        """Returns lists of mutually overlapping contours between two Section objects."""
        complete_overlaps = []  # Pairs of completely (within threshold) overlapping contours
        potential_overlaps = []  # Pairs of incompletely overlapping contours

        # Compute overlaps
        sec1_overlaps = []  # Section1 contours that have ovlps in section2
        sec2_overlaps = []  # Section2 contours that have ovlps in section1
        for contA in self.section1.contours:
            ovlpA = []
            ovlpB = []
            for contB in self.section2.contours:
                if sameName and contA.name != contB.name:
                    continue
                overlap = contA.overlaps(contB, threshold)
                # If sameName: only check contours with the same name
                if overlap != 0:
                    ovlpA.append(contA)
                    ovlpB.append(contB)
                    if overlaps:
                        if overlap == 1:
                            complete_overlaps.append([contA, contB])
                        elif overlap > 0:  # Conflicting (non-100%) overlap
                            potential_overlaps.append([contA, contB])
            sec1_overlaps.extend(ovlpA)
            sec2_overlaps.extend(ovlpB)

        if overlaps:
            # Return unique conts from section1, unique conts from section2,
            # completely overlapping contours, and incompletely overlapping
            # contours
            return (
                [cont for cont in self.section1.contours if cont not in sec1_overlaps],
                [cont for cont in self.section2.contours if cont not in sec2_overlaps],
                complete_overlaps,
                potential_overlaps
            )
        else:
            return (
                [cont for cont in self.section1.contours if cont not in sec1_overlaps],
                [cont for cont in self.section2.contours if cont not in sec2_overlaps]
            )

    def toSection(self):
        """Return a Section object that resolves the merge.

        If not resolved (None), defaults to the self.section1 version
        """
        return Section(
            self.attributes if self.attributes is not None else self.section1.attributes(),
            self.images if self.images is not None else self.section1.images,
            self.contours if self.contours is not None else self.section1.contours
        )


class MergeSeries(object):
    """MergeSeries contains the two series to be merged, handlers for how to
    merge the series, and functions for manipulating class data."""

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        # Series to be merged
        self.series1 = kwargs.get("series1")
        self.series2 = kwargs.get("series2")

        # Merged stuff
        self.attributes = None
        self.contours = None
        self.zcontours = None

        self.checkConflicts()

    def checkConflicts(self):
        """Automatically set merged stuff for equivalent things."""
        # Are attributes equivalent?
        if self.series1.attributes() == self.series2.attributes():
            self.attributes = self.series1.attributes()
        # Are contours equivalent?
        if self.series1.contours == self.series2.contours:
            self.contours = self.series1.contours
        # Are zcontours equivalent?
        if self.series1.zcontours == self.series2.zcontours:
            self.zcontours = self.series1.zcontours

    def isDone(self):
        """Boolean indicating status of merge."""
        return (self.attributes is not None and
                self.contours is not None and
                self.zcontours is not None)

    def doneCount(self):
        """Number of resolved issues"""
        return (self.attributes is not None,
                self.contours is not None,
                self.zcontours is not None).count(True)

    # mergeTool functions
    def getCategorizedZContours(self, threshold=(1 + 2**(-17))):
        """Return unique Series1 ZContours, unique Series2 ZContours,
        and overlapping Contours to be merged."""
        copy_contours_1 = [cont for cont in self.series1.zcontours]
        copy_contours_2 = [cont for cont in self.series2.zcontours]
        overlaps = []
        for contA in copy_contours_1:
            for contB in copy_contours_2:
                if contA.name == contB.name and contA.overlaps(contB, threshold):
                    # If overlaps, append to overlap list and remove from unique lists
                    overlaps.append(contA)
                    copy_contours_1.remove(contA)
                    copy_contours_2.remove(contB)
        return copy_contours_1, copy_contours_2, overlaps

    def toSeries(self):
        """Return a Series object that resolves the merge.

        If not resolved (None), defaults to self.series1 version
        """
        return Series(
            self.attributes if self.attributes is not None else self.series1.attributes(),
            self.contours if self.contours is not None else self.series1.contours,
            self.zcontours if self.zcontours is not None else self.series1.zcontours
        )
