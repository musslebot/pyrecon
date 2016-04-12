"""MultiSectionContour."""
from collections import defaultdict, OrderedDict
import re

from pyrecon.main import openSeries


class MultiSectionContour(object):
    """Object with data representing a Contour that spans multiple sections.

    Example data includes:
        * start, end, count,
        * surface area
        * flat area
        * volume
        * and others depending on the type of object loaded into this class
    """

    def __init__(self, name=None, series=None):
        """Apply given keyword arguments as instance attributes."""
        self.name = None  # Name of object
        self.series = None  # Series to which this object belongs

        self.start = None
        self.end = None
        self.count = None

        self.load(name, series)
        self.makeSpecific()

    def load(self, name, series):
        """From a filepath or series object, update instance attributes."""
        self.name = name
        if isinstance(series, str):
            series = openSeries(series)
        self.series = series
        # Protrusion number (stored as "p##")
        self.protrusion = self.getProtNumber()
        # Parent dendrite number (stored as "d##")
        self.dendrite = self.getDendNumber()
        self.rType = self.getrType()
        self.data = {}  # updated in makeSpecific
        self.start, self.end, self.count = self.series.getStartEndCount(
            self.name)

    def getDendNumber(self):
        """Return name of dendrite this Contour belongs to."""
        dend = re.compile(r"d[0-9]{1,}")
        try:
            return self.name[:dend.match(self.name).end()]
        except:
            return None

    def getProtNumber(self):
        """Return name of protrusion this Contour belongs to."""
        dend = re.compile(r"d[0-9]{1,}")
        temp_name = self.name[dend.match(self.name).end():]
        try:
            prot = re.compile(r"[0-9]{1,}")
            start = prot.search(temp_name).start()
            end = prot.search(temp_name).end()
            prot_num = temp_name[start:end]
            return "p" + str(prot_num)
        except:
            return None

    def makeSpecific(self):
        """Create unique data for this rObject (depends on type)."""
        if self.rType:
            r_type = self.rType.lower()
            if r_type == "p":
                # Protrusion
                important_data = ["start", "end", "count"]
                self.children = self.findChildren()
            elif r_type == "c":
                # C
                important_data = ["start", "end", "count"]
            elif "cfa" in r_type:
                # CFA
                important_data = ["start", "end", "count", "surface area",
                                  "flat area"]
            elif "endo" in r_type:
                # Endosome
                important_data = ["start", "end", "count"]
            elif r_type[0:3] == "ser":  # TODO
                # SER
                important_data = ["start", "end", "count"]
            elif r_type[0:2] == "sp":  # TODO
                # Spine
                important_data = ["start", "end", "count", "surface area",
                                  "flat area", "volume"]
            elif r_type[0:2] == "ax":  # TODO
                # Axon
                important_data = ["start", "end", "count"]
            else:
                important_data = ["start", "end", "count"]
        else:
            important_data = ["start", "end", "count"]
        self.getData(important_data)

    def getData(self, list_of_desired_data=None):
        """Populate instance with desired data."""
        data = OrderedDict()
        for item in list_of_desired_data:
            data[item] = self.series.getData(self.name, item)
        self.data = data
        self.numColumns = len(list_of_desired_data)

    def getrType(self):
        """Return type of character."""
        if self.protrusion:
            prot = re.compile(self.protrusion[1:])  # dont include the "p"
            dend = re.compile(self.dendrite)
            # remove dendrite from name
            temp_name = self.name[dend.match(self.name).end():]
            return temp_name[:prot.search(temp_name).start()]
        return None

    def findChildren(self):
        """Return children of this protrusion."""
        children = defaultdict(list)
        # dont include "p" in self.protrusion
        child_exp = re.compile(self.dendrite + ".{0,}" + self.protrusion[1:])
        dend_exp = re.compile(self.dendrite)
        for child in self.series.getObjectLists()[2]:
            if child_exp.match(child):
                # Extract from name what is in between dend and prot
                end_of_dendrite = dend_exp.match(child).end()
                beg_of_protrusion = child.rfind(self.protrusion[1:])
                # Try to add to existing entry in dictionary
                name = str(child[end_of_dendrite:beg_of_protrusion])
                children[name].append(child)
        return children

    def getSpacing(self):
        """Return number of spaces to add after excel sheet."""
        try:
            number_of_entries_per_child = [
                len(val) for val in self.children.values()
            ]
            return max(number_of_entries_per_child) - 1
        except:
            return 0


# class Dendrite(MultiSectionContour):
#     def __init__(self, name=None, series=None):
#         MultiSectionContour.__init__(self, name, series)
#         data = {}

#     def loadData(self):
#         return


# class Axon(MultiSectionContour):
#     def __init__(self, name=None, series=None):
#         MultiSectionContour.__init__(self, name, series)
#         data = {}

#     def loadData(self):
#         return


# class Spine(MultiSectionContour):
#     def __init__(self, name=None, series=None):
#         MultiSectionContour.__init__(self, name, series)
#         data = {}

#     def loadData(self):
#         return


# class SER(MultiSectionContour):
#     def __init__(self, name=None, series=None):
#         MultiSectionContour.__init__(self, name, series)
#         data = {}

#     def loadData(self):
#         return

# class CFA(MultiSectionContour):
#     def __init__(self, name=None, series=None):
#         MultiSectionContour.__init__(self, name, series)
#         data = {}

#     def loadData(self):
#         return

# class C(MultiSectionContour):
#     def __init__(self, name=None, series=None):
#         MultiSectionContour.__init__(self, name, series)
#         data = {}

#     def loadData(self):
#         return
