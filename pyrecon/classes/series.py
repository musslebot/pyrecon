"""Series."""
import re


class Series(object):
    """Class representing a RECONSTRUCT Series."""

    def __init__(self, **kwargs):
        """Set instance attributes with args and kwargs."""
        self.index = kwargs.get("index")
        self.viewport = kwargs.get("viewport")
        self.units = kwargs.get("units")
        self.autoSaveSeries = kwargs.get("autoSaveSeries")
        self.autoSaveSection = kwargs.get("autoSaveSection")
        self.warnSaveSection = kwargs.get("warnSaveSection")
        self.beepDeleting = kwargs.get("beepDeleting")
        self.beepPaging = kwargs.get("beepPaging")
        self.hideTraces = kwargs.get("hideTraces")
        self.unhideTraces = kwargs.get("unhideTraces")
        self.hideDomains = kwargs.get("hideDomains")
        self.unhideDomains = kwargs.get("unhideDomains")
        self.useAbsolutePaths = kwargs.get("useAbsolutePaths")
        self.defaultThickness = kwargs.get("defaultThickness")
        self.zMidSection = kwargs.get("zMidSection")
        self.thumbWidth = kwargs.get("thumbWidth")
        self.thumbHeight = kwargs.get("thumbHeight")
        self.fitThumbSections = kwargs.get("fitThumbSections")
        self.firstThumbSection = kwargs.get("firstThumbSection")
        self.lastThumbSection = kwargs.get("lastThumbSection")
        self.skipSections = kwargs.get("skipSections")
        self.displayThumbContours = kwargs.get("displayThumbContours")
        self.useFlipbookStyle = kwargs.get("useFlipbookStyle")
        self.flipRate = kwargs.get("flipRate")
        self.useProxies = kwargs.get("useProxies")
        self.widthUseProxies = kwargs.get("widthUseProxies")
        self.heightUseProxies = kwargs.get("heightUseProxies")
        self.scaleProxies = kwargs.get("scaleProxies")
        self.significantDigits = kwargs.get("significantDigits")
        self.defaultBorder = kwargs.get("defaultBorder")
        self.defaultFill = kwargs.get("defaultFill")
        self.defaultMode = kwargs.get("defaultMode")
        self.defaultName = kwargs.get("defaultName")
        self.defaultComment = kwargs.get("defaultComment")
        self.listSectionThickness = kwargs.get("listSectionThickness")
        self.listDomainSource = kwargs.get("listDomainSource")
        self.listDomainPixelsize = kwargs.get("listDomainPixelsize")
        self.listDomainLength = kwargs.get("listDomainLength")
        self.listDomainArea = kwargs.get("listDomainArea")
        self.listDomainMidpoint = kwargs.get("listDomainMidpoint")
        self.listTraceComment = kwargs.get("listTraceComment")
        self.listTraceLength = kwargs.get("listTraceLength")
        self.listTraceArea = kwargs.get("listTraceArea")
        self.listTraceCentroid = kwargs.get("listTraceCentroid")
        self.listTraceExtent = kwargs.get("listTraceExtent")
        self.listTraceZ = kwargs.get("listTraceZ")
        self.listTraceThickness = kwargs.get("listTraceThickness")
        self.listObjectRange = kwargs.get("listObjectRange")
        self.listObjectCount = kwargs.get("listObjectCount")
        self.listObjectSurfarea = kwargs.get("listObjectSurfarea")
        self.listObjectFlatarea = kwargs.get("listObjectFlatarea")
        self.listObjectVolume = kwargs.get("listObjectVolume")
        self.listZTraceNote = kwargs.get("listZTraceNote")
        self.listZTraceRange = kwargs.get("listZTraceRange")
        self.listZTraceLength = kwargs.get("listZTraceLength")
        self.borderColors = kwargs.get("borderColors")
        self.fillColors = kwargs.get("fillColors")
        self.offset3D = kwargs.get("offset3D")
        self.type3Dobject = kwargs.get("type3Dobject")
        self.first3Dsection = kwargs.get("first3Dsection")
        self.last3Dsection = kwargs.get("last3Dsection")
        self.max3Dconnection = kwargs.get("max3Dconnection")
        self.upper3Dfaces = kwargs.get("upper3Dfaces")
        self.lower3Dfaces = kwargs.get("lower3Dfaces")
        self.faceNormals = kwargs.get("faceNormals")
        self.vertexNormals = kwargs.get("vertexNormals")
        self.facets3D = kwargs.get("facets3D")
        self.dim3D = kwargs.get("dim3D")
        self.gridType = kwargs.get("gridType")
        self.gridSize = kwargs.get("gridSize")
        self.gridDistance = kwargs.get("gridDistance")
        self.gridNumber = kwargs.get("gridNumber")
        self.hueStopWhen = kwargs.get("hueStopWhen")
        self.hueStopValue = kwargs.get("hueStopValue")
        self.satStopWhen = kwargs.get("satStopWhen")
        self.satStopValue = kwargs.get("satStopValue")
        self.brightStopWhen = kwargs.get("brightStopWhen")
        self.brightStopValue = kwargs.get("brightStopValue")
        self.tracesStopWhen = kwargs.get("tracesStopWhen")
        self.areaStopPercent = kwargs.get("areaStopPercent")
        self.areaStopSize = kwargs.get("areaStopSize")
        self.ContourMaskWidth = kwargs.get("ContourMaskWidth")
        self.smoothingLength = kwargs.get("smoothingLength")
        self.mvmtIncrement = kwargs.get("mvmtIncrement")
        self.ctrlIncrement = kwargs.get("ctrlIncrement")
        self.shiftIncrement = kwargs.get("shiftIncrement")
        # Non-attributes
        self.name = kwargs.get("name")
        self.path = kwargs.get("path")
        self.contours = kwargs.get("contours", [])
        self.zcontours = kwargs.get("zcontours", [])
        self.sections = kwargs.get("sectons", [])

    def attributes(self):
        """Return a dict of this Series" attributes."""
        ignore = ["name", "path", "contours", "zcontours", "sections"]
        attributes = {}
        for att in self.__dict__:
            if att not in ignore:  # if att is considered a desired attribute
                attributes[att] = self.__dict__[att]
        return attributes

    def deleteTraces(self, exceptions=None):
        """Delete all traces except the regex found in exceptions list"""
        if not exceptions:
            exceptions = []
        for section in self.sections:
            for contour in section.contours:
                for regex in exceptions:
                    if re.compile(regex).match(contour.name):
                        pass
                    else:
                        print "Removing: {}".format(contour.name)
                        section.contours.remove(contour)

# curationTool functions
    def locateInvalidTraces(self, delete=False):
        """Return a map of invalid traces in this Series."""
        invalid_dict = {}
        for section in self.sections:
            invalids = []
            for contour in section.contours:
                if contour.isInvalid():
                    invalids.append(contour.name)
                    if delete:
                        print "deleted: {} in Section: {}".format(
                            contour.name, section.index)
                        section.contours.remove(contour)
            if len(invalids) != 0:
                invalid_dict[section.index] = invalids
        return invalid_dict

    def locateReverseTraces(self):
        """Return a map of reverse traces in this Series."""
        reverse_dict = {}
        for section in self.sections:
            reverse_traces = []
            for contour in section.contours:
                try:
                    if contour.isReverse():
                        reverse_traces.append(contour)
                except:
                    print "Invalid! {} on section {}) was ignored".format(
                        contour.name, section.index)
                    print("\t check coordinates in XML file")
            if len(reverse_traces) != 0:
                reverse_dict[section.index] = reverse_traces
        return reverse_dict

    def locateDistantTraces(self, threshold=7):
        """Return a map of indexes containing traces that have Section gaps.

        Number of Sections determined by threshold kwarg
        """
        # Build a list of lists for all the contours in each section
        all_section_contours = []
        for section in self.sections:
            contours = list(set([cont.name for cont in section.contours]))
            all_section_contours.append(contours)
        # Go through list of contours and check for distances
        index = int(self.sections[0].index)  # correct starting index (can be 0 or 1)
        distant_traces = {}
        for sec in range(len(all_section_contours)):
            traces = []
            for contour in all_section_contours[sec]:
                # Check above
                if sec + threshold + 1 <= len(self.sections):
                    # Check and ignore if in section:section+threshold
                    section_to_threshold_countours = []
                    for contList in all_section_contours[sec + 1:sec + threshold + 1]:
                        section_to_threshold_countours.extend(contList)
                    if contour not in section_to_threshold_countours:
                        # Check if contour is in section+threshold and up
                        threshold_to_end_contours = []
                        for contList in all_section_contours[sec + threshold + 1:]:
                            threshold_to_end_contours.extend(contList)
                        if contour in threshold_to_end_contours:
                            traces.append(contour)
                # Check below
                if sec - threshold - 1 >= 0:
                    # Check and ignore if in section-threshold:section
                    minus_threshold_to_section_contours = []
                    for contList in all_section_contours[sec - threshold:sec]:
                        minus_threshold_to_section_contours.extend(contList)
                    if contour not in minus_threshold_to_section_contours:
                        # Check if contour is in section-threshold and down
                        begin_to_minus_threshold_contours = []
                        for contList in all_section_contours[:sec - threshold]:
                            begin_to_minus_threshold_contours.extend(contList)
                        if contour in begin_to_minus_threshold_contours:
                            traces.append(contour)
                # Add traces to distant_traces dictionary
                if len(traces) != 0:
                    distant_traces[index] = traces
            index += 1
        return distant_traces

    def locateDuplicates(self):
        """Return a map of section numbers to duplicates.

        Locate overlapping traces of the same name in a section.
        """
        # Build dictionary of sections w/ contours whose name appear more than
        # once in that section
        dupe_names = {}
        for section in self.sections:
            duplicates = []
            # List of contour names
            contour_names = [cont.name for cont in section.contours]
            # Go through each contour, see if name appears multiple times
            for contour in section.contours:
                if contour_names.count(contour.name) > 1:
                    duplicates.append(contour)
            if len(duplicates) != 0:
                dupe_names[section.index] = duplicates

        # Go through each list of potential dupes contour names and
        # check if actually overlaps
        dupe_dict = {}
        for key in dupe_names:
            duplicates = []
            for contour in dupe_names[key]:
                # Filter contours of same memory address so that overlap isn"t tested on itself
                copy_contours = [cont for cont in dupe_names[key] if id(cont) != id(contour) and cont.name == contour.name]
                for cont in copy_contours:
                    try:
                        if contour.overlaps(cont) == 1:  # Perfect overlap (within threshold)
                            duplicates.append(cont)
                    except:
                        print("Invalid contour (%s on section %d) was ignored") % (cont.name, key)
                        print("\t check coordinates in XML file")
            if len(duplicates) != 0:
                dupe_dict[key] = duplicates
        return dupe_dict
