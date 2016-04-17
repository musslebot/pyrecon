"""Functions for writing to RECONSTRUCT XML files."""
import os

from lxml import etree


def contourToElement(contour):
    try: # Contour in Section
        element = etree.Element(
            "Contour",
            name=str(contour.name),
            hidden=str(contour.hidden).lower(),
            closed=str(contour.closed).lower(),
            simplified=str(contour.simplified).lower(),
            border=str(contour.border[0])+" "+str(contour.border[1])+" "+str(contour.border[2]),
            fill=str(contour.fill[0])+" "+str(contour.fill[1])+" "+str(contour.fill[2]),
            mode=str(contour.mode),
            points= ", ".join([str(pt[0])+" "+str(pt[1]) for pt in contour.points])+","
        )
    except:
        try: # Contour in Series
            element = etree.Element(
                "Contour",
                name=str(contour.name),
                closed=str(contour.closed).lower(),
                border=str(contour.border[0])+" "+str(contour.border[1])+" "+str(contour.border[2]),
                fill=str(contour.fill[0])+" "+str(contour.fill[1])+" "+str(contour.fill[2]),
                mode=str(contour.mode),
                points= ", ".join([str(pt[0])+" "+str(pt[1]) for pt in contour.points])+","
            )
        except:
            print("Problem creating Contour element", contour.name)
    return element


def imageToElement(image):
    element = etree.Element(
        "Image",
        mag=str(image.mag),
        contrast=str(image.contrast),
        brightness=str(image.brightness),
        red=str(image.red).lower(),
        green=str(image.red).lower(),
        blue=str(image.blue).lower(),
        src=str(image.src)
    )
    return element


def sectionToElement(section):
    element = etree.Element(
        "Section",
        index=str(section.index),
        thickness=str(section.thickness),
        alignLocked=str(section.alignLocked).lower()
    )
    return element


def seriesToElement(series):
    element = etree.Element(
        "Series",
        index=str(series.index),
        viewport=" ".join([str(val) for val in series.viewport]),
        units=str(series.units),
        autoSaveSeries=str(series.autoSaveSeries).lower(),
        autoSaveSection=str(series.autoSaveSection).lower(),
        warnSaveSection=str(series.warnSaveSection).lower(),
        beepDeleting=str(series.beepDeleting).lower(),
        beepPaging=str(series.beepPaging).lower(),
        hideTraces=str(series.hideTraces).lower(),
        unhideTraces=str(series.unhideTraces).lower(),
        hideDomains=str(series.hideDomains).lower(),
        unhideDomains=str(series.unhideDomains).lower(),
        useAbsolutePaths=str(series.useAbsolutePaths).lower(),
        defaultThickness=str(series.defaultThickness),
        zMidSection=str(series.zMidSection).lower(),
        thumbWidth=str(series.thumbWidth),
        thumbHeight=str(series.thumbHeight),
        fitThumbSections=str(series.fitThumbSections).lower(),
        firstThumbSection=str(series.firstThumbSection),
        lastThumbSection=str(series.lastThumbSection),
        skipSections=str(series.skipSections),
        displayThumbContours=str(series.displayThumbContours).lower(),
        useFlipbookStyle=str(series.useFlipbookStyle).lower(),
        flipRate=str(series.flipRate),
        useProxies=str(series.useProxies).lower(),
        widthUseProxies=str(series.widthUseProxies),
        heightUseProxies=str(series.heightUseProxies),
        scaleProxies=str(series.scaleProxies),
        significantDigits=str(series.significantDigits),
        defaultBorder=" ".join([str(val) for val in series.defaultBorder]),
        defaultFill=" ".join([str(val) for val in series.defaultFill]),
        defaultMode=str(series.defaultMode),
        defaultName=str(series.defaultName),
        defaultComment=str(series.defaultComment),
        listSectionThickness=str(series.listSectionThickness).lower(),
        listDomainSource=str(series.listDomainSource).lower(),
        listDomainPixelsize=str(series.listDomainPixelsize).lower(),
        listDomainLength=str(series.listDomainLength).lower(),
        listDomainArea=str(series.listDomainArea).lower(),
        listDomainMidpoint=str(series.listDomainMidpoint).lower(),
        listTraceComment=str(series.listTraceComment).lower(),
        listTraceLength=str(series.listTraceLength).lower(),
        listTraceArea=str(series.listTraceArea).lower(),
        listTraceCentroid=str(series.listTraceCentroid).lower(),
        listTraceExtent=str(series.listTraceExtent).lower(),
        listTraceZ=str(series.listTraceZ).lower(),
        listTraceThickness=str(series.listTraceThickness).lower(),
        listObjectRange=str(series.listObjectRange).lower(),
        listObjectCount=str(series.listObjectCount).lower(),
        listObjectSurfarea=str(series.listObjectSurfarea).lower(),
        listObjectFlatarea=str(series.listObjectFlatarea).lower(),
        listObjectVolume=str(series.listObjectVolume).lower(),
        listZTraceNote=str(series.listZTraceNote).lower(),
        listZTraceRange=str(series.listZTraceRange).lower(),
        listZTraceLength=str(series.listZTraceLength).lower(),
        borderColors=",".join([str(val[0])+" "+str(val[1])+" "+str(val[2]) for val in series.borderColors])+",",
        fillColors=",".join([str(val[0])+" "+str(val[1])+" "+str(val[2]) for val in series.fillColors])+",",
        offset3D=" ".join([str(val) for val in series.offset3D]),
        type3Dobject=str(series.type3Dobject),
        first3Dsection=str(series.first3Dsection),
        last3Dsection=str(series.last3Dsection),
        max3Dconnection=str(series.max3Dconnection),
        upper3Dfaces=str(series.upper3Dfaces).lower(),
        lower3Dfaces=str(series.lower3Dfaces).lower(),
        faceNormals=str(series.faceNormals).lower(),
        vertexNormals=str(series.vertexNormals).lower(),
        facets3D=str(series.facets3D),
        dim3D=" ".join([str(val) for val in series.dim3D]),
        gridType=str(series.gridType),
        gridSize=" ".join([str(val) for val in series.gridSize]),
        gridDistance=" ".join([str(val) for val in series.gridDistance]),
        gridNumber=" ".join([str(val) for val in series.gridNumber]),
        hueStopWhen=str(series.hueStopWhen),
        hueStopValue=str(series.hueStopValue),
        satStopWhen=str(series.satStopWhen),
        satStopValue=str(series.satStopValue),
        brightStopWhen=str(series.brightStopWhen),
        brightStopValue=str(series.brightStopValue),
        tracesStopWhen=str(series.tracesStopWhen).lower(),
        areaStopPercent=str(series.areaStopPercent),
        areaStopSize=str(series.areaStopSize),
        ContourMaskWidth=str(series.ContourMaskWidth),
        smoothingLength=str(series.smoothingLength),
        mvmtIncrement=" ".join([str(val) for val in series.mvmtIncrement]),
        ctrlIncrement=" ".join([str(val) for val in series.ctrlIncrement]),
        shiftIncrement=" ".join([str(val) for val in series.shiftIncrement])
    )
    return element


def transformToElement(transform):
    element = etree.Element(
        "Transform",
        dim=str(transform.dim),
        xcoef=" "+" ".join([str(item) for item in transform.xcoef]),
        ycoef=" "+" ".join([str(item) for item in transform.ycoef])
    )
    return element


def zcontourToElement(zcontour):
    element = etree.Element(
        "ZContour",
        name=str(zcontour.name),
        closed=str(zcontour.closed).lower(),
        border=" ".join([str(val) for val in zcontour.border]),
        fill=" ".join([str(val) for val in zcontour.fill]),
        mode=str(zcontour.mode),
        points=", ".join([str(pt[0])+" "+str(pt[1])+" "+str(pt[2]) for pt in zcontour.points])+","
    )
    return element


def objectToElement(object):
    """Returns an ElementTree Element for <object> that is appropriate for writing to an XML file."""
    if object.__class__.__name__ == "Contour":
        return contourToElement(object)
    elif object.__class__.__name__ == "Image":
        return imageToElement(object)
    elif object.__class__.__name__ == "Section":
        return sectionToElement(object)
    elif object.__class__.__name__ == "Series":
        return seriesToElement(object)
    elif object.__class__.__name__ == "Transform":
        return transformToElement(object)
    elif object.__class__.__name__ == "ZContour":
        return zcontourToElement(object)


def writeSection(section, directory, outpath=None, overwrite=False):
    """Writes <section> to an XML file in directory"""
    print "Writing section:",section.name
    if not outpath: # Will write to file with sections name
        if str(directory[-1]) != "/":
            directory += "/"
        outpath = str(directory)+str(section.name)

    # Make root (Section attributes: index, thickness, alignLocked)
    root = objectToElement(section)

    # Add Transform nodes for images (assumes they can all have different tform)
    for image in section.images:
        trnsfrm = objectToElement(image.transform)
        img = objectToElement(image)
        # RECONSTRUCT has a Contour for Images
        cntr = contourToElement(image)
        trnsfrm.append(img)
        trnsfrm.append(cntr)
        root.append(trnsfrm) # append images transform node to XML file

    # Non-Image Contours
    # - Build list of unique Transform objects
    uniqueTransforms = []
    for contour in section.contours:
        unique = True
        for tform in uniqueTransforms:
            if tform == contour.transform:
                unique = False
                break
        if unique:
            uniqueTransforms.append(contour.transform)

    # - Add contours to their equivalent Transform objects
    for transform in uniqueTransforms:
        transformElement = objectToElement(transform)
        for contour in section.contours:
            if contour.transform == transform:
                cont = objectToElement(contour)
                transformElement.append(cont)
        root.append(transformElement)

    # Make tree and write
    elemtree = etree.ElementTree(root)
    if os.path.exists(outpath) and not overwrite:
        print("Section write aborted (%s) due to overwrite conflict."%(section.name))
        return
    elemtree.write(outpath, pretty_print=True, xml_declaration=True, encoding="UTF-8")


def writeSeries(series, directory, outpath=None, sections=False, overwrite=False):
    """Writes <series> to an XML file in directory"""
    print "Writing series:",series.name
    # Pre-writing checks
    # - Make sure directory is correctly input
    if directory[-1] != "/":
        directory += "/"
    # - Check if directory exists, make if does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not outpath:
        outpath = directory+series.name+".ser"
    # - Raise error if this file already exists to prevent overwrite
    if not overwrite and os.path.exists(outpath):
        msg = "CAUTION: Files already exist in ths directory: Do you want to overwrite them?"
        try: # Graphical
            from PySide.QtGui import QApplication, QMessageBox
            app = QApplication.instance()
            if app == None:
                app = QApplication([])
            msgBox = QMessageBox()
            msgBox.setText(msg)
            msgBox.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel)
            response = msgBox.exec_()
            if response == QMessageBox.Ok:
                a = "yes"
            else:
                a = "no"
        except: # StdOut
            a = raw_input(msg+" (y/n)")
        overwrite = str(a).lower() in ["y","yes"]
        if not overwrite:
            raise IOError("\nFilename %s already exists.\nQuiting write command to avoid overwrite"%outpath)
        print ("!!! OVERWRITE ENABLED !!!")
    # Build series root element
    root = objectToElement( series )
    # Add Contours/ZContours to root
    if series.contours is not None:
        for contour in series.contours:
            root.append( objectToElement(contour) )
    else:
        print "No contours in", series.name
    if series.zcontours is not None:
        for zcontour in series.zcontours:
            root.append( objectToElement(zcontour) )
    else:
        print "No zcontours in", series.name
    # Make tree and write
    elemtree = etree.ElementTree(root)
    elemtree.write(outpath, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    # Write all sections if <sections> == True
    if sections == True:
        for section in series.sections:
            writeSection(section, directory, overwrite=overwrite)
