from PySide.QtCore import *
from PySide.QtGui import *
from pyrecon.gui import mergetool
from pyrecon import openSeries
from pyrecon.classes import Series, Section
from shapely.geometry import box, LinearRing, LineString, Point, Polygon

TOLERANCE = 1 + 2**-17

class PyreconMainWindow(QMainWindow):
    '''Main PyRECONSTRUCT window.'''
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setWindowTitle('MergeTraces')
        self.show()
        newSize = QDesktopWidget().availableGeometry().size() / 4
        self.resize( newSize )
        self.statusBar().showMessage('Ready! Welcome to PyRECONSTRUCT')
        self.loadMergeTool()
    def loadMergeTool(self):
        loadDialog = SingleSeriesLoad() # User locates 1 series
        s1 = openSeries(loadDialog.output)
        mTraces = createMergeTraces(s1)

class BrowseWidget(QWidget):
    '''Provides a QLineEdit and button for browsing through a file system. browseType can be directory, file or series but defaults to directory.'''
    def __init__(self, browseType='directory'):
        QWidget.__init__(self)
        self.loadObjects(browseType)
        self.loadFunctions(browseType)
        self.loadLayout()
    def loadObjects(self, browseType):
        # Path entry area
        self.path = QLineEdit()
        if browseType == 'directory':
            title = 'Enter or browse path to directory'
        elif browseType == 'series':
            title = 'Enter or browse path'
        else:
            title = 'Enter or browse path to file'
        self.path.setText(title)
        # Browse button
        self.browseButton = QPushButton()
        self.browseButton.setText('Browse')
    def loadFunctions(self, browseType):
        if browseType == 'directory':
            self.browseButton.clicked.connect( self.browseDir )
        elif browseType == 'series':
            self.browseButton.clicked.connect( self.browseSeries )
        else:
            self.browseButton.clicked.connect( self.browseFile )
    def loadLayout(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.path)
        hbox.addWidget(self.browseButton)
        self.setLayout(hbox)
    def browseDir(self):
        dirName = QFileDialog.getExistingDirectory(self)
        self.path.setText( str(dirName) )
    def browseFile(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", "/home/")
        self.path.setText( str(fileName[0]) )
    def browseSeries(self):
        fileName = QFileDialog.getOpenFileName(self, "Open Series", "/home/", "Series File (*.ser)")
        self.path.setText( str(fileName[0]) )

class SingleSeriesLoad(QDialog):
    '''Dialog for loading series files into memory as pyrecon.classes.Series objects'''
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.loadObjects()
        self.loadFunctions()
        self.loadLayout()
        self.exec_()
    def loadObjects(self):
        self.series1 = BrowseWidget(browseType='series')
        self.closeButton = QPushButton()
        self.closeButton.setText('Load Series')
    def loadFunctions(self):
        self.closeButton.clicked.connect( self.loadClose )
    def loadLayout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.series1)
        vbox.addWidget(self.closeButton)
        self.setLayout(vbox)
    def loadClose(self):
        # Add paths to self.output
        self.output = ( str(self.series1.path.text())
                        )
        self.close()

    if __name__ == '__main__':
        app = QApplication.instance()
        if app == None:
            app = QApplication([])
        a = PyreconMainWindow()
        app.exec_()


def start():
    """Begin GUI application (pyrecon.gui.main)"""
    app = QApplication.instance()
    if app is None:  # Create QApplication if doesn"t exist
        app = QApplication([])
    gui = PyreconMainWindow()
    app.exec_()  # Start event-loop

def createMergeTraces(series1):
  """Return a file with traces merged."""
#    m1 = MergeSeries(name=series1.name, series1=series1)

  m_secs = []
  for section in series1.sections:
    section_traces = MergeTraces(name=section.name, section1=section)
    m_secs.append(section_traces)

  
  mergedTraceSet = MergeSet(name=series1.name, merge_series=series1, section_merges=m_secs)
  if outpath != "":

    mergedTraceSet.writeMergeSet(outpath=os.path.dirname(str(self.series1.path.text())
                        ))


class MergeSet(object):
    """Class for merging data Series and Section data."""

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.seriesMerge = kwargs.get("merge_series")
        self.sectionMerges = kwargs.get("section_merges", [])


    def writeMergeSet(self, outpath):
        """Writes self.seriesMerge and self.sectionMerges to XML"""
        merged_series = self.seriesMerge.toSeries()
        merged_series.name = self.seriesMerge.name.replace(".ser", "")
        for mergeSec in self.sectionMerges:
            merged_series.sections.append(mergeSec.toSection())
        reconstruct_writer.write_series(merged_series, outpath, sections=True)
        print "Done!" 

class MergeTraces(object):

  def __init__(self, *args, **kwargs):
      self.name = kwargs.get("name")
      self.section1 = kwargs.get("section1")

      # Merged stuff
      self.attributes = self.section1.attributes()
      self.images = None
      self.contours = None

      # Contours conflict resolution stuff
      self.section_1_unique_contours = None
      self.definite_shared_contours = None
      self.potential_shared_contours = None


      self.checkConflicts()
  
  def checkConflicts(self):
    # Are contours equivalent?
    separated_contours = self.getCategorizedContours(include_overlaps=True)
    self.contours = separated_contours
      



  def getCategorizedContours(self, threshold=(1 + 2**(-17)), sameName=True, include_overlaps=False):
      """Returns list of mutually overlapping contours in a Section object."""
      complete_overlaps = []
      potential_overlaps = []

      # Compute overlaps
      overlaps = []
      for i in range (len(self.section1.contours)-1):
          print (self.section1.name)
          contA = self.section1.contours[i]
          contB = self.section1.contours[i+1]
          print (contA.name)
          print (contA.shape.type)

          print (contB.name)
          print (contB.shape.type)
        
          if contA.name != contB.name:
              continue
          if contA.shape.type != contB.shape.type:
              continue

          if not is_contacting(contA.shape, contB.shape):
              continue
          elif is_exact_duplicate(contA.shape, contB.shape):
              overlaps.append(contB)
              complete_overlaps.append(contB)
              continue
          if is_potential_duplicate(contA.shape, contB.shape):
              overlaps.append(contB)
              potential_overlaps.append([contA, contB])

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
              [cont for cont in self.section1.contours if cont not in overlaps],
              complete_overlaps,
              potential_overlaps
          )
      else:
          return (
              [cont for cont in self.section1.contours if cont not in overlaps],
              )


class MergeSeries(object):
  def __init__(self, **kwargs):
      self.name = kwargs.get("name")
      # Series to be used
      self.series1 = kwargs.get("series1")

      # Merged stuff
      self.attributes = None
      self.contours = None
      self.zcontours = None

  def toSeries(self):
      """Return a Series object that resolves the merge.
      If not resolved (None), defaults to self.series1 version
      """
      attributes = self.attributes if self.attributes is not None else self.series1.attributes()
      contours = self.contours if self.contours is not None else self.series1.contours
      zcontours = self.zcontours if self.zcontours is not None else self.series1.zcontours
      return Series(contours=contours, zcontours=zcontours, **attributes)

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
