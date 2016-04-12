"""Series."""
import os
import re

from Section import Section as Section


class Series(object):
    """Class representing a RECONSTRUCT Series."""

    def __init__(self, *args, **kwargs):
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
        self.processArguments(args, kwargs)

    def processArguments(self, args, kwargs):
        """Update instance with provided args/kwargs."""
        # 1) ARGS
        try:
            self.update(*args)
        except Exception as e:
            print "Could not process Series arg: {}\n\t".format(
                str(args) + str(e))
        # 2) KWARGS
        try:
            self.update(**kwargs)
        except Exception as e:
            print "Could not process Series kwarg: {}\n\t".format(
                str(kwargs) + str(e))

# MUTATORS
    def update(self, *args, **kwargs):
        """Update instance attributes from arbitrary arguments."""
        for arg in args:
            # String argument
            if isinstance(arg, str):  # Possible path to XML?
                import pyrecon.tools.handleXML as xml
                try:  # given full path to .ser file
                    self.update(*xml.process(arg))
                    self.path = arg
                    filename = arg.split("/")[len(arg.split("/")) - 1]
                    self.name = filename.replace(".ser", "")
                except:  # given directory path instead of path to .ser file
                    path = arg
                    if path[-1] != "/":
                        path += "/"
                    path = path + str(
                        [f for f in os.listdir(path) if ".ser" in f].pop())
                    self.update(*xml.process(path))
                    self.path = path
                    filename = path.split("/")[len(path.split("/")) - 1]
                    self.name = filename.replace(".ser", "")
            # Dictionary
            elif isinstance(arg, {}):
                for key in arg:
                    if key in self.__dict__:
                        self.__dict__[key] = arg[key]
            # List
            elif isinstance(arg, list):
                for item in arg:
                    # Contour
                    if item.__class__.__name__ == "Contour":
                        self.contours.append(item)
                    # ZSection
                    elif item.__class__.__name__ == "ZContour":
                        self.zcontours.append(item)
                    # Section
                    elif item.__class__.__name__ == "Section":
                        self.sections.append(item)
            # Contour
            elif arg.__class__.__name__ == "Contour":
                self.contours.append(arg)
            # ZSection
            elif arg.__class__.__name__ == "ZContour":
                self.zcontours.append(item)
            # Section
            elif arg.__class__.__name__ == "Section":
                self.sections.append(arg)
        for kwarg in kwargs:
            # Load sections
            if "sections" in kwargs:
                if kwargs["sections"]:
                    print("Attempting to load sections..."),
                    ser = os.path.basename(self.path)
                    serfixer = re.compile(re.escape(".ser"), re.IGNORECASE)
                    sername = serfixer.sub("", ser)
                    # look for files with "seriesname"+"."+"number"
                    p = re.compile("^" + sername + "[.][0-9]*$")
                    sectionlist = [f for f in os.listdir(self.path.replace(ser, "")) if p.match(f)]
                    # create and append Sections for each section file
                    path = self.path.replace(os.path.basename(self.path), "")
                    for sec in sectionlist:
                        section = Section(path + sec)
                        if section.index is not None:  # TODO
                            self.update(section)
                    # sort sections by index
                    self.sections = sorted(
                        self.sections, key=lambda Section: Section.index)
                    print(" SUCCESS!")

# ACCESSORS
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

# calibrationTool functions
    def zeroIdentity(self):
        """Convert points for all Sections to identity transform."""
        for sec in self.sections:
            for c in sec.contours:
                if c.image is None:
                    # Don"t alter image contours i.e. domain1
                    c.points = c.transform.worldpts(c.points)
                    c.transform.dim = 0
                    c.transform.ycoef = [0, 0, 1, 0, 0, 0]
                    c.transform.xcoef = [0, 1, 0, 0, 0, 0]
                    c._tform = c.transform.tform()

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

# excelTool functions
    def getObject(self, regex):
        """Return nested list of Contours, per section, that match regex."""
        objects = []
        for section in self.sections:
            section.append(section.getObject(regex))
        return objects

    def getObjectLists(self):
        """Return sorted lists of objects in a Series, grouped by type."""
        dendrite_expression = r"d[0-9]{2,}"  # represents base dendrite name (d##)
        protrusion_expression = r"d[0-9]{2,}p[0-9]{2,}$"  # represents base protrusion name (d##p##)
        trace_expression = r"d[0-9]{2,}.{1,}[0-9]{2,}"  # represents trace name (d##<tracetype>##)

        # Convert expressions to usable regular expressions
        dendrite_expression = re.compile(dendrite_expression)
        protrusion_expression = re.compile(protrusion_expression, re.I)
        trace_expression = re.compile(trace_expression, re.I)

        # Create lists for names of dendrites, protrusions, traces, and other objects
        dendrites = []
        protrusions = []
        traces = []
        others = []
        for section in self.sections:
            for contour in section.contours:
                # Dendrite
                if dendrite_expression.match(contour.name):
                    end = dendrite_expression.match(contour.name).end()
                    dendrites.append(contour.name[0:end])
                # Protrusion
                if protrusion_expression.match(contour.name):
                    protrusions.append(contour.name)
                # Trace === expand to > 2 digits!
                if (trace_expression.match(contour.name) and
                    protrusion_expression.match(contour.name) == None):
                    traces.append(contour.name)
                    # Make sure a d##p## exists for this trace
                    this_prot = contour.name[0:3] + "p" + contour.name[4:6]
                    if (protrusion_expression.match(this_prot) and
                        this_prot not in protrusions):
                        protrusions.append(this_prot)
                # Everything else (other)
                if (dendrite_expression.match(contour.name) == None and
                    protrusion_expression.match(contour.name) == None and
                    trace_expression.match(contour.name) == None):
                    others.append(contour.name)
        return sorted(list(set(dendrites))), sorted(list(set(protrusions))), sorted(list(set(traces))), sorted(list(set(others)))

    def getData(self, object_name, data_string):
        """Return data."""
        string = str(data_string).lower()
        if string == "volume":
            return self.getVolume(object_name)
        elif string == "total volume":
            return self.getTotalVolume(object_name)
        elif string == "surface area":
            return self.getSurfaceArea(object_name)
        elif string == "flat area":
            return self.getFlatArea(object_name)
        elif string == "start":
            return self.getStartEndCount(object_name)[0]
        elif string == "end":
            return self.getStartEndCount(object_name)[1]
        elif string == "count":
            return self.getStartEndCount(object_name)[2]

    def getVolume(self, object_name):
        """Return volume of the object throughout the Series.

        Calculated by summing the value obtained by multiplying the area by
        Section thickness over all sections.
        """
        vol = 0
        for section in self.sections:
            for contour in section.contours:
                if contour.name == object_name:
                    try:
                        contour.popShape()
                        vol += (contour.shape.area * section.thickness)
                    except:
                        print "getVolume(): Invalid contour: {} in section: {}".format(
                            contour.name, section.index)
                        print "Check XML file and fix before trusting data.\n"
        return vol

    def getTotalVolume(self, object_name):
        """Return total volumne, of the given object, in this Series."""
        related_objects = []
        if object_name[-1].isalpha():
            object_name = object_name[:-1]
            # Get all related objects by base object name
            for section in self.sections:
                for contour in section.contours:
                    if object_name in contour.name:
                        related_objects.append(contour.name)
        # Find total volume by summing volume for all related objects
        total_volume = 0
        for obj in list(set(related_objects)):
            total_volume += self.getVolume(obj)
        return total_volume

    def getSurfaceArea(self, object_name):
        """Return surface area of the object throughout the Series.

        Calculated by summing the length multiplied by section thickness across
        sections.
        """
        surface_area = 0
        for section in self.sections:
            for contour in section.contours:
                if contour.name == object_name:
                    try:
                        flat_area = contour.getLength() * section.thickness
                        surface_area += flat_area
                    except:
                        print "getSurfaceArea(): Invalid contour: {} in section: {}".format(
                            contour.name, section.index)
                        print "Check XML file and fix before trusting data.\n"
        return surface_area

    def getFlatArea(self, object_name):
        """Return the flat area of the object throughout the Series.

        Calculated by summing the area of the object across all sections.
        """
        flat_area = 0
        for section in self.sections:
            for contour in section.contours:
                if contour.name == object_name:
                    try:
                        contour.popShape()
                        if contour.closed:
                            flat_area += contour.shape.area
                        else:
                            length = contour.getLength()
                            thickness = section.thickness
                            section_area = length * thickness
                            flat_area += section_area
                    except:
                        print "getFlatArea(): Invalid contour: {} in section: {}".format(
                            contour.name, section.index)
                        print "Check XML file and fix before trusting data.\n"
        return flat_area

    def getStartEndCount(self, object_name):
        """Return a tuple of start index, end index, and count of object."""
        start = 0
        end = 0
        count = 0
        # Count
        for section in self.sections:
            for contour in section.contours:
                if contour.name == object_name:
                    count += 1
            # Start/End
            if object_name in [cont.name for cont in section.contours]:
                # Start index
                if start == 0:
                    start = section.index
                # End index
                end = section.index
        return start, end, count
