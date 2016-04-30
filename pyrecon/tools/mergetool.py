"""Merge two RECONSTRUCT datasets."""
from shapely.geometry import box, LinearRing, LineString, Point, Polygon

from pyrecon.classes import Series, Section
from pyrecon.tools import reconstruct_writer

TOLERANCE = 1 + 2**-17


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


def is_contacting(shape1, shape2):
    """Return True if two shapes are contacting."""
    if isinstance(shape1, Point) and isinstance(shape2, Point):
        # TODO: investigate more sophisticated comparison
        return shape1.equals(shape2)

    elif isinstance(shape1, LineString) and isinstance(shape2, LineString):
        # shape1.almost_equals(shape2)?
        return shape1.almost_equals(shape2)

    elif isinstance(shape1, Polygon) and isinstance(shape2, Polygon):
        this_box = box(*shape1.bounds)
        other_box = box(*shape2.bounds)
        if not this_box.intersects(other_box) and not this_box.touches(other_box):
            return False
        else:
            return True

    raise Exception("No support for shape type(s): {}".format(
        set([shape1.type, shape2.type])))


def is_exact_duplicate(shape1, shape2, threshold=TOLERANCE):
    """Return True if two shapes are exact duplicates (within tolerance)."""
    if isinstance(shape1, Point) and isinstance(shape2, Point):
        # TODO: investigate more sophisticated comparison
        return shape1.equals(shape2)

    elif isinstance(shape1, Polygon) and isinstance(shape2, Polygon):
        if shape1.has_z and shape2.has_z:
            return shape1.exterior.equals(shape2.exterior)
        else:
            if is_reverse(shape2) != is_reverse(shape2):
                # Reverse traces are not duplicates of non-reverse
                return False
            area_of_union = shape1.union(shape2).area
            area_of_intersection = shape1.intersection(shape2).area
            if not area_of_intersection:
                return False
            union_over_intersection = area_of_union / area_of_intersection
            if union_over_intersection >= threshold:
                # Potential duplicate
                return False
            elif union_over_intersection < threshold:
                return True

    elif isinstance(shape1, LineString) and isinstance(shape2, LineString):
        # TODO: investigate more sophisticated comparison
        return shape1.equals(shape2)

    raise Exception("No support for shape type(s): {}".format(
        set([shape1.type, shape2.type])))


# TODO: investigate way to reduce shared computation with is_duplicate
# TODO: investigate if support needed for LineString
def is_potential_duplicate(shape1, shape2, threshold=TOLERANCE):
    """Return True if two shapes are potential overlaps (exceed tolerance)."""
    if isinstance(shape1, Point) and isinstance(shape2, Point):
        # TODO: investigate more sophisticated comparison
        return shape1.almost_equals(shape2) and not shape1.equals(shape2)

    elif isinstance(shape1, Polygon) and isinstance(shape2, Polygon):
        if shape1.has_z or shape2.has_z:
            raise Exception(
                "is_potential_duplicate does not support 3D polygons")
        if is_reverse(shape2) != is_reverse(shape2):
            # Reverse traces are not duplicates of non-reverse
            return False
        area_of_union = shape1.union(shape2).area
        area_of_intersection = shape1.intersection(shape2).area
        if not area_of_intersection:
            return False
        union_over_intersection = area_of_union / area_of_intersection
        if union_over_intersection >= threshold:
            return True
        else:
            return False

    elif isinstance(shape1, LineString) and isinstance(shape2, LineString):
        # TODO: investigate more sophisticated comparison
        return shape1.almost_equals(shape2) and not shape1.equals(shape2)

    raise Exception("No support for shape type(s): {}".format(
        set([shape1.type, shape2.type])))


def createMergeSet(series1, series2):  # TODO: needs multithreading
    """Return a MergeSet from two Series."""
    if len(series1.sections) != len(series2.sections):
        raise Exception("Series do not have the same number of Sections.")

    m_ser = MergeSeries(
        name=series1.name,
        series1=series1,
        series2=series2,
    )
    m_secs = []
    for section1, section2 in zip(series1.sections, series2.sections):
        if section1.index != section2.index:
            raise Exception("Section indices do not match.")
        merge_section = MergeSection(
            name=section1.name,
            section1=section1,
            section2=section2,
        )
        m_secs.append(merge_section)

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
        self.section_1_unique_contours = None
        self.section_2_unique_contours = None
        self.definite_shared_contours = None
        self.potential_shared_contours = None

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
        separated_contours = self.getCategorizedContours(include_overlaps=True)  # TODO: thread this function
        self.section_1_unique_contours = separated_contours[0]
        self.section_2_unique_contours = separated_contours[1]
        self.definite_shared_contours = separated_contours[2]
        self.potential_shared_contours = separated_contours[3]
        if (len(self.section_1_unique_contours + self.section_2_unique_contours) == 0 and
            len(self.potential_shared_contours) == 0):
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

    def getCategorizedContours(self, threshold=(1 + 2**(-17)), sameName=True, include_overlaps=False):
        """Returns lists of mutually overlapping contours between two Section objects."""
        complete_overlaps = []
        potential_overlaps = []

        # Compute overlaps
        sec1_overlaps = []  # Section1 contours that have ovlps in section2
        sec2_overlaps = []  # Section2 contours that have ovlps in section1
        for contA in self.section1.contours:
            ovlpA = []
            ovlpB = []
            for contB in self.section2.contours:
                if sameName and contA.name != contB.name:
                    continue
                if contA.shape.type != contB.shape.type:
                    # Ignore contours with different shapes
                    continue

                if not is_contacting(contA.shape, contB.shape):
                    continue
                elif is_exact_duplicate(contA.shape, contB.shape):
                    ovlpA.append(contA)
                    ovlpB.append(contB)
                    complete_overlaps.append(contA)
                    continue
                if is_potential_duplicate(contA.shape, contB.shape):
                    ovlpA.append(contA)
                    ovlpB.append(contB)
                    potential_overlaps.append([contA, contB])
            sec1_overlaps.extend(ovlpA)
            sec2_overlaps.extend(ovlpB)

        if include_overlaps:
            # Return unique conts from section1, unique conts from section2,
            # completely overlapping contours, and incompletely overlapping
            # contours
            new_potential_overlaps = []
            for contA, contB in potential_overlaps:
                if contA in complete_overlaps and contB in complete_overlaps:
                    continue
                else:
                    new_potential_overlaps.append([contA, contB])
            potential_overlaps = new_potential_overlaps
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
        attributes = self.attributes if self.attributes is not None else self.section1.attributes()
        images = self.images if self.images is not None else self.section1.images
        contours = self.contours if self.contours is not None else self.section1.contours
        return Section(images=images, contours=contours, **attributes)


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

    def getCategorizedZContours(self, threshold=(1 + 2**(-17))):
        """Return unique Series1 ZContours, unique Series2 ZContours,
        and overlapping Contours to be merged."""
        copy_contours_1 = [cont for cont in self.series1.zcontours]
        copy_contours_2 = [cont for cont in self.series2.zcontours]
        overlapping_zcontours = []
        for contA in copy_contours_1:
            for contB in copy_contours_2:
                if contA.name == contB.name and is_exact_duplicate(contA.shape, contB.shape):
                    # If overlaps, append to overlap list and remove from unique lists
                    overlapping_zcontours.append(contA)
                    copy_contours_1.remove(contA)
                    copy_contours_2.remove(contB)
        return copy_contours_1, copy_contours_2, overlapping_zcontours

    def toSeries(self):
        """Return a Series object that resolves the merge.

        If not resolved (None), defaults to self.series1 version
        """
        attributes = self.attributes if self.attributes is not None else self.series1.attributes()
        contours = self.contours if self.contours is not None else self.series1.contours
        zcontours = self.zcontours if self.zcontours is not None else self.series1.zcontours
        return Series(contours=contours, zcontours=zcontours, **attributes)
