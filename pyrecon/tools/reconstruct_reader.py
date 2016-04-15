"""Functions for reading from RECONSTRUCT XML files."""
from lxml import etree

from pyrecon.classes import Contour, Image, Transform, ZContour


def process_series_file(path):
    """Return a Series object from Series XML file."""
    tree = etree.parse(path)
    root = tree.getroot()

    data = extract_series_attributes(root)

    # Populate Series Contours & ZContours
    data["contours"] = []
    data["zcontours"] = []
    for elem in root:
        if elem.tag == "Contour":
            # TODO: no Contour import
            contour = Contour(series_contour_attributes(elem), None)
            data["contours"].append(contour)
        elif elem.tag == "ZContour":
            # TODO: no ZContour import
            zcontour = ZContour(extract_zcontour_attributes(elem))  # TODO
            data["zcontours"].append(zcontour)
    return data


def process_section_file(path):
    """Return a Section object from a Section XML file."""
    tree = etree.parse(path)
    root = tree.getroot()
    attributes = extract_section_attributes(root)

    # Process images and contours
    images = []
    contours = None
    for transform in root:
        # make Transform object
        transform_object = Transform(extract_transform_attributes(transform))
        children = [child for child in transform]

        # Image transform node
        img = [child for child in children if child.tag == "Image"]
        if len(img) > 0:
            img = img.pop()
            img = Image(extract_image_attributes(img))

            image_contour = []
            for child in children:
                if child.tag == "Contour":
                    image_contour.append(child)

            if len(image_contour) > 0:
                image_contour = image_contour.pop()
                contour = Contour(
                    section_contour_attributes(
                        image_contour), transform_object)
                # set contour"s image to the image
                contour.image = img
                # set image"s contour to the contour
                img.contour = contour
                images.append(img)
        # Non-Image Transform Node
        else:
            for child in children:
                if child.tag == "Contour":
                    cont = Contour(
                        section_contour_attributes(child), transform_object)
                    if contours is None:
                        contours = []
                    contours.append(cont)
    # section =
    return attributes, images, contours


def series_contour_attributes(node):
    """Return a dict of Series' Contour's attributes."""
    def get_points_int(points):
        return zip(
            [int(x.replace(",", "")) for x in points.split()][0::2],
            [int(x.replace(",", "")) for x in points.split()][1::2]
        )
    attributes = {
        "name": str(node.get("name")),
        "closed": node.get("closed").capitalize() == "True",
        "mode": int(node.get("mode")),
        "border": tuple(float(x) for x in node.get("border").strip().split(" ")),
        "fill": tuple(float(x) for x in node.get("fill").strip().split(" ")),
        "points": get_points_int(node.get("points")),
        "coordSys": "bio",
    }
    return attributes


def section_contour_attributes(node):
    """Return a dict of Section Contour's attributes."""
    def get_points_float(points):
        return zip(
            [float(x.replace(",", "")) for x in points.split()][0::2],
            [float(x.replace(",", "")) for x in points.split()][1::2]
        )
    attributes = {
        "name": str(node.get("name")),
        "comment": str(node.get("comment")),
        "hidden": node.get("hidden").capitalize() == "True",
        "closed": node.get("closed").capitalize() == "True",
        "simplified": node.get("simplified").capitalize() == "True",
        "mode": int(node.get("mode")),
        "border": tuple(float(x) for x in node.get("border").strip().split(" ")),
        "fill": tuple(float(x) for x in node.get("fill").strip().split(" ")),
        "points": get_points_float(node.get("points")),
        "coordSys": "bio",
    }
    return attributes


def extract_image_attributes(node):
    attributes = {
        "src": str(node.get("src")),
        "mag": float(node.get("mag")),
        "contrast": float(node.get("contrast")),
        "brightness": float(node.get("brightness")),
        "red": node.get("red").capitalize() == "True",
        "green": node.get("green").capitalize() == "True",
        "blue": node.get("blue").capitalize() == "True",
    }
    return attributes


def extract_section_attributes(node):
    attributes = {
        "index": int(node.get("index")),
        "thickness": float(node.get("thickness")),
        "alignLocked": node.get("alignLocked").capitalize() == "True",
    }
    return attributes


def extract_series_attributes(node):
    attributes = {
        "index": int(node.get("index")),
        "viewport": tuple(float(x) for x in node.get("viewport").split(" ")),
        "units": str(node.get("units")),
        "autoSaveSeries": node.get("autoSaveSeries").capitalize() == "True",
        "autoSaveSection": node.get("autoSaveSection").capitalize() == "True",
        "warnSaveSection": node.get("warnSaveSection").capitalize() == "True",
        "beepDeleting": node.get("beepDeleting").capitalize() == "True",
        "beepPaging": node.get("beepPaging").capitalize() == "True",
        "hideTraces": node.get("hideTraces").capitalize() == "True",
        "unhideTraces": node.get("unhideTraces").capitalize() == "True",
        "hideDomains": node.get("hideDomains").capitalize() == "True",
        "unhideDomains": node.get("hideDomains").capitalize() == "True",
        "useAbsolutePaths": node.get("useAbsolutePaths").capitalize() == "True",
        "defaultThickness": float(node.get("defaultThickness")),
        "zMidSection": node.get("zMidSection").capitalize() == "True",
        "thumbWidth": int(node.get("thumbWidth")),
        "thumbHeight": int(node.get("thumbHeight")),
        "fitThumbSections": node.get("fitThumbSections").capitalize() == "True",
        "firstThumbSection": int(node.get("firstThumbSection")),
        "lastThumbSection": int(node.get("lastThumbSection")),
        "skipSections": int(node.get("skipSections")),
        "displayThumbContours": node.get("displayThumbContours").capitalize() == "True",
        "useFlipbookStyle": node.get("useFlipbookStyle").capitalize()  == "True",
        "flipRate": int(node.get("flipRate")),
        "useProxies": node.get("useProxies").capitalize() == "True",
        "widthUseProxies": int(node.get("widthUseProxies")),
        "heightUseProxies": int(node.get("heightUseProxies")),
        "scaleProxies": float(node.get("scaleProxies")),
        "significantDigits": int(node.get("significantDigits")),
        "defaultBorder": tuple(float(x) for x in node.get("defaultBorder").split(" ")),
        "defaultFill": tuple(float(x) for x in node.get("defaultFill").split(" ")),
        "defaultMode": int(node.get("defaultMode")),
        "defaultName": str(node.get("defaultName")),
        "defaultComment": str(node.get("defaultComment")),
        "listSectionThickness": node.get("listSectionThickness").capitalize() == "True",
        "listDomainSource": node.get("listDomainSource").capitalize() == "True",
        "listDomainPixelsize": node.get("listDomainPixelsize").capitalize() == "True",
        "listDomainLength": node.get("listDomainLength").capitalize() == "True",
        "listDomainArea": node.get("listDomainArea").capitalize() == "True",
        "listDomainMidpoint": node.get("listDomainMidpoint").capitalize() == "True",
        "listTraceComment": node.get("listTraceComment").capitalize() == "True",
        "listTraceLength": node.get("listTraceLength").capitalize()  == "True",
        "listTraceArea": node.get("listTraceArea").capitalize() == "True",
        "listTraceCentroid": node.get("listTraceCentroid").capitalize() == "True",
        "listTraceExtent": node.get("listTraceExtent").capitalize() == "True",
        "listTraceZ": node.get("listTraceZ").capitalize() == "True",
        "listTraceThickness": node.get("listTraceThickness").capitalize() == "True",
        "listObjectRange": node.get("listObjectRange").capitalize() == "True",
        "listObjectCount": node.get("listObjectCount").capitalize() == "True",
        "listObjectSurfarea": node.get("listObjectSurfarea").capitalize() == "True",
        "listObjectFlatarea": node.get("listObjectFlatarea").capitalize() == "True",
        "listObjectVolume": node.get("listObjectVolume").capitalize() == "True",
        "listZTraceNote": node.get("listZTraceNote").capitalize() == "True",
        "listZTraceRange": node.get("listZTraceRange").capitalize() == "True",
        "listZTraceLength": node.get("listZTraceLength").capitalize() == "True",
        "borderColors": [tuple(float(x) for x in x.split(" ") if x != "") for x in [x.strip() for x in node.get("borderColors").split(",")] if len(tuple(float(x) for x in x.split(" ") if x != "")) == 3],
        "fillColors": [tuple(float(x) for x in x.split(" ") if x != "") for x in [x.strip() for x in node.get("fillColors").split(",")] if len(tuple(float(x) for x in x.split(" ") if x != "")) == 3],
        "offset3D": tuple(float(x) for x in node.get("offset3D").split(" ")),
        "type3Dobject": int(node.get("type3Dobject")),
        "first3Dsection": int(node.get("first3Dsection")),
        "last3Dsection": int(node.get("last3Dsection")),
        "max3Dconnection": int(node.get("max3Dconnection")),
        "upper3Dfaces": node.get("upper3Dfaces").capitalize() == "True",
        "lower3Dfaces": node.get("lower3Dfaces").capitalize() == "True",
        "faceNormals": node.get("faceNormals").capitalize() == "True",
        "vertexNormals": node.get("vertexNormals").capitalize() == "True",
        "facets3D": int(node.get("facets3D")),
        "dim3D": tuple(float(x) for x in node.get("dim3D").split()),
        "gridType": int(node.get("gridType")),
        "gridSize": tuple(float(x) for x in node.get("gridSize").split(" ")),
        "gridDistance": tuple(float(x) for x in node.get("gridDistance").split(" ")),
        "gridNumber": tuple(float(x) for x in node.get("gridNumber").split(" ")),
        "hueStopWhen": int(node.get("hueStopWhen")),
        "hueStopValue": int(node.get("hueStopValue")),
        "satStopWhen": int(node.get("satStopWhen")),
        "satStopValue": int(node.get("satStopValue")),
        "brightStopWhen": int(node.get("brightStopWhen")),
        "brightStopValue": int(node.get("brightStopValue")),
        "tracesStopWhen": node.get("tracesStopWhen").capitalize(),
        "areaStopPercent": int(node.get("areaStopPercent")),
        "areaStopSize": int(node.get("areaStopSize")),
        "ContourMaskWidth": int(node.get("ContourMaskWidth")),
        "smoothingLength": int(node.get("smoothingLength")),
        "mvmtIncrement": tuple(float(x) for x in node.get("mvmtIncrement").split(" ")),
        "ctrlIncrement": tuple(float(x) for x in node.get("ctrlIncrement").split(" ")),
        "shiftIncrement": tuple(float(x) for x in node.get("shiftIncrement").split(" ")),
    }
    return attributes


def extract_transform_attributes(node):
    def intorfloat(input):
        """Returns number data type from string."""
        if "." in input:
            return float(input)
        else:
            try:  # TODO
                return int(input)
            except:
                print "\n\treconstruct_reader.intorfloat():",input,"converted to float",float(input),"\n"
                return float(input)
    attributes = {
        "dim": int(node.get("dim")),
        "xcoef": [intorfloat(x) for x in node.get("xcoef").strip().split(" ")],
        "ycoef": [intorfloat(x) for x in node.get("ycoef").strip().split(" ")],
    }
    return attributes


def extract_zcontour_attributes(node):
    attributes = {
        "name": str(node.get("name")),
        "closed": node.get("closed").capitalize() == "True",
        "border": tuple(float(x) for x in node.get("border").split(" ")),
        "fill": tuple(float(x) for x in node.get("fill").split(" ")),
        "mode": int(node.get("mode")),
        "points": [(float(x.split(" ")[0]), float(x.split(" ")[1]), int(x.split(" ")[2])) for x in [x.strip() for x in node.get("points").split(",")] if len(tuple(float(x) for x in x.split(" ") if x != "")) == 3],
    }
    return attributes
