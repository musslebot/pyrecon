"""Series."""
import re


class Series(object):
    """Class representing a RECONSTRUCT Series."""

    def __init__(self):
        """Set instance attributes with args and kwargs."""
        self.index = None
        self.viewport = None
        self.units = None
        self.autoSaveSeries = None
        self.autoSaveSection = None
        self.warnSaveSection = None
        self.beepDeleting = None
        self.beepPaging = None
        self.hideTraces = None
        self.unhideTraces = None
        self.hideDomains = None
        self.unhideDomains = None
        self.useAbsolutePaths = None
        self.defaultThickness = None
        self.zMidSection = None
        self.thumbWidth = None
        self.thumbHeight = None
        self.fitThumbSections = None
        self.firstThumbSection = None
        self.lastThumbSection = None
        self.skipSections = None
        self.displayThumbContours = None
        self.useFlipbookStyle = None
        self.flipRate = None
        self.useProxies = None
        self.widthUseProxies = None
        self.heightUseProxies = None
        self.scaleProxies = None
        self.significantDigits = None
        self.defaultBorder = None
        self.defaultFill = None
        self.defaultMode = None
        self.defaultName = None
        self.defaultComment = None
        self.listSectionThickness = None
        self.listDomainSource = None
        self.listDomainPixelsize = None
        self.listDomainLength = None
        self.listDomainArea = None
        self.listDomainMidpoint = None
        self.listTraceComment = None
        self.listTraceLength = None
        self.listTraceArea = None
        self.listTraceCentroid = None
        self.listTraceExtent = None
        self.listTraceZ = None
        self.listTraceThickness = None
        self.listObjectRange = None
        self.listObjectCount = None
        self.listObjectSurfarea = None
        self.listObjectFlatarea = None
        self.listObjectVolume = None
        self.listZTraceNote = None
        self.listZTraceRange = None
        self.listZTraceLength = None
        self.borderColors = None
        self.fillColors = None
        self.offset3D = None
        self.type3Dobject = None
        self.first3Dsection = None
        self.last3Dsection = None
        self.max3Dconnection = None
        self.upper3Dfaces = None
        self.lower3Dfaces = None
        self.faceNormals = None
        self.vertexNormals = None
        self.facets3D = None
        self.dim3D = None
        self.gridType = None
        self.gridSize = None
        self.gridDistance = None
        self.gridNumber = None
        self.hueStopWhen = None
        self.hueStopValue = None
        self.satStopWhen = None
        self.satStopValue = None
        self.brightStopWhen = None
        self.brightStopValue = None
        self.tracesStopWhen = None
        self.areaStopPercent = None
        self.areaStopSize = None
        self.ContourMaskWidth = None
        self.smoothingLength = None
        self.mvmtIncrement = None
        self.ctrlIncrement = None
        self.shiftIncrement = None
        # Non-attributes
        self.name = None
        self.path = None
        self.contours = []
        self.zcontours = []
        self.sections = []

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
