from pyrecon.classes import Series, Section
from pyrecon.tools import reconstruct_writer


def createMergeSet(series1, series2):  # TODO: needs multithreading
    """This function takes in two Series objects and returns a MergeSet to be used for the mergeTool"""
    m_ser = MergeSeries(series1, series2)
    m_secs = []
    for i in range(len(series1.sections)):
        if series1.sections[i].index == series2.sections[i].index:
            m_secs.append(MergeSection(series1.sections[i], series2.sections[i]))
        else:
            raise Exception("Series do not have matching section indeces! Aborting createMergeSet()!")
            return
    return MergeSet(m_ser, m_secs)


class MergeSet(object):
    """Class for merging data Series and Section data."""

    def __init__(self, *args, **kwargs):
        self.seriesMerge = None  # MergeSeries object
        self.sectionMerges = None  # List of MergeSection objects
        self.processArguments(args, kwargs)

    # Argument processing
    def processArguments(self, args, kwargs):
        """Process given arguments."""
        for arg in args:
            if arg.__class__.__name__ == "MergeSeries":
                self.seriesMerge = arg
                self.name = arg.name
            elif isinstance(arg, list):
                self.sectionMerges = arg
            else:
                print "Cannot process argument:", arg
        for kwarg in kwargs:
            print kwarg + ":" , kwargs[kwarg] #===

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
        reconstruct_writer.writeSeries(merged_series, outpath, sections=True)
        print "Done!"  # TODO


class MergeSection(object):
    """Class for merging together 2 Sections."""

    def __init__(self, *args, **kwargs):
        # Sections to be merged
        self.section1 = None
        self.section2 = None

        # Merged stuff
        self.attributes = None
        self.images = None
        self.contours = None

        # Contours conflict resolution stuff
        self.uniqueA = None
        self.uniqueB = None
        self.compOvlps = None
        self.confOvlps = None

        # Process arguments
        self.processArguments(args, kwargs)
        self.checkConflicts()

    # Argument processing
    def processArguments(self, args, kwargs):
        """Process given arguments."""
        for arg in args:
            # Section object
            if arg.__class__.__name__ == "Section":
                if self.section1 is None:
                    self.section1 = arg
                    self.name = arg.name
                elif self.section2 is None:
                    self.section2 = arg
                else:
                    print "MergeSection already contains two Sections..."
            else:
                print "Not a section object:", arg  # TODO
        for kwarg in kwargs:
            print kwarg + ":", kwargs[kwarg]  # TODO

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
                overlap = contA.overlaps(contB, threshold)
                # If sameName: only check contours with the same name
                if (sameName and
                    contA.name == contB.name and
                    overlap != 0):
                    ovlpA.append(contA)
                    ovlpB.append(contB)
                    if overlaps:
                        if overlap == 1:
                            complete_overlaps.append([contA, contB])
                        elif overlap > 0:  # Conflicting (non-100%) overlap
                            potential_overlaps.append([contA, contB])
                # If not sameName: check all contours, regardless of same name
                elif not sameName and overlap != 0:
                    ovlpA.append(contA)
                    ovlpB.append(contB)
                    if overlaps:
                        if overlap:
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

    def __init__(self, *args, **kwargs):
        # Series to be merged
        self.series1 = None
        self.series2 = None

        # Merged stuff
        self.attributes = None
        self.contours = None
        self.zcontours = None

        # Process arguments
        self.processArguments(args, kwargs)
        self.checkConflicts()

    # Argument processing
    def processArguments(self, args, kwargs):
        """Process given arguments."""
        for arg in args:
            if arg.__class__.__name__ == "Series":
                if self.series1 is None:
                    self.series1 = arg
                    self.name = arg.name+".ser"
                elif self.series2 is None:
                    self.series2 = arg
                else:
                    print "MergeSeries already contains two Series..."
        for kwarg in kwargs:
            print kwarg + ":", kwargs[kwarg]

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
