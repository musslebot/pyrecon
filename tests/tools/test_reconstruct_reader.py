import os
from unittest import TestCase

from lxml import etree

from pyrecon.classes import Section, Series
from pyrecon.tools import reconstruct_reader

DATA_LOC = "tests/tools/_data"


class ReconstructReaderTests(TestCase):

    def test_process_series_directory(self):
        path = DATA_LOC
        series = reconstruct_reader.process_series_directory(path)
        self.assertIsInstance(series, Series)
        self.assertIsNotNone(series.contours)

    def test_process_series_file(self):
        path = os.path.join(DATA_LOC, "_VRJXH.ser")
        series = reconstruct_reader.process_series_file(path)
        self.assertIsInstance(series, Series)
        self.assertEqual(series.name, "_VRJXH")
        self.assertEqual(series.path, DATA_LOC)
        self.assertEqual(len(series.contours), 4)
        self.assertEqual(len(series.zcontours), 6)

    def test_process_section_file(self):
        path = os.path.join(DATA_LOC, "_VRJXH.98")
        section = reconstruct_reader.process_section_file(path)
        self.assertIsInstance(section, Section)
        self.assertEqual(section.name, "_VRJXH.98")
        self.assertEqual(section.index, 98)
        self.assertEqual(len(section.contours), 7)
        self.assertEqual(len(section.images), 1)

    def test_extract_series_contour_attributes(self):
        node = etree.parse(os.path.join(DATA_LOC, "_series_contour.xml")).getroot()
        series_contour_attributes = reconstruct_reader.extract_series_contour_attributes(
            node)
        expected_attributes = {
            'name': 'D52',
            'coordSys': 'bio',
            'points': [
                (-2, 1),
                (-5, 0),
                (-2, -1),
                (-4, -4),
                (-1, -2),
                (0, -5),
                (1, -2),
                (4, -4),
                (2, -1),
                (5, 0),
                (2, 1),
                (4, 4),
                (1, 2),
                (0, 5),
                (-1, 2),
                (-4, 4),
            ],
            'mode': 11,
            'closed': False,
            'border': (0.498, 0.0, 1.0),
            'fill': (0.498, 0.0, 1.0),
        }

        self.assertTrue(series_contour_attributes, expected_attributes)

    def test_extract_section_contour_attributes(self):
        node = etree.parse(os.path.join(DATA_LOC, "_section_contour.xml")).getroot()
        section_contour_attributes = reconstruct_reader.extract_section_contour_attributes(
            node)
        expected_attributes = {
            'comment': 'None',
            'points': [
                (25.3974, 12.0386),
                (25.3225, 11.9327),
                (25.307, 11.8706),
                (25.307, 11.8112),
            ],
            'simplified': False,
            'name': 'd124_cfa_10_mac',
            'closed': False,
            'hidden': True,
            'fill': (0.0, 1.0, 0.0),
            'border': (0.0, 1.0, 0.0),
            'coordSys': 'bio',
            'mode': 11,
        }
        self.assertTrue(section_contour_attributes, expected_attributes)

    def test_extract_image_attributes(self):
        node = etree.parse(os.path.join(DATA_LOC, "_image.xml")).getroot()
        image_attributes = reconstruct_reader.extract_image_attributes(
            node)
        expected_attributes = {
            'blue': True,
            'src': 'VRJXH_097.tif',
            'brightness': 0.0,
            'green': False,
            'contrast': 1.0,
            'mag': 0.00254,
            'red': True,
        }
        self.assertTrue(image_attributes, expected_attributes)

    def test_extract_section_attributes(self):
        node = etree.parse(os.path.join(DATA_LOC, "_section.xml")).getroot()
        section_attributes = reconstruct_reader.extract_section_attributes(
            node)
        expected_attributes = {
            'index': 98,
            'alignLocked': False,
            'thickness': 0.048,
        }
        self.assertTrue(section_attributes, expected_attributes)

    def test_extract_series_attributes(self):
        node = etree.parse(os.path.join(DATA_LOC, "_series.xml")).getroot()
        series_attributes = reconstruct_reader.extract_series_attributes(
            node)
        expected_attributes = {
            'hueStopWhen': 3,
            'smoothingLength': 7,
            'useFlipbookStyle': False,
            'satStopValue': 50,
            'listObjectCount': True,
            'significantDigits': 6,
            'vertexNormals': True,
            'displayThumbContours': True,
            'borderColors': [
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
            ],
            'listZTraceNote': True,
            'defaultThickness': 0.05,
            'autoSaveSection': True,
            'listSectionThickness': True,
            'unhideTraces': True,
            'useProxies': True,
            'listTraceComment': True,
            'listObjectFlatarea': True,
            'fitThumbSections': False,
            'skipSections': 1,
            'thumbWidth': 128,
            'listTraceZ': False,
            'flipRate': 5,
            'lower3Dfaces': True,
            'unhideDomains': False,
            'listTraceCentroid': False,
            'ctrlIncrement': (0.0044, 0.01, 0.01, 1.002, 1.002, 0.004, 0.004, 0.0002, 0.0002),
            'gridDistance': (1.0, 1.0),
            'listDomainMidpoint': False,
            'upper3Dfaces': True,
            'index': 267,
            'listTraceLength': True,
            'hideTraces': False,
            'listObjectSurfarea': False,
            'hueStopValue': 50,
            'mvmtIncrement': (0.022, 1.0, 1.0, 1.01, 1.01, 0.02, 0.02, 0.001, 0.001),
            'ContourMaskWidth': 0,
            'satStopWhen': 3,
            'thumbHeight': 96,
            'fillColors': [
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
            ],
            'defaultName': 'd124_ztrace_21_up_03+',
            'faceNormals': False,
            'listTraceExtent': False,
            'max3Dconnection': -1,
            'areaStopPercent': 999,
            'lastThumbSection': 2147483647,
            'listTraceThickness': False,
            'defaultFill': (1.0, 0.0, 0.5),
            'gridType': 0,
            'useAbsolutePaths': False,
            'firstThumbSection': 1,
            'beepDeleting': True,
            'areaStopSize': 0,
            'defaultBorder': (1.0, 0.0, 0.5),
            'listZTraceLength': True,
            'type3Dobject': 1,
            'scaleProxies': 0.25,
            'hideDomains': False,
            'gridSize': (1.0, 1.0),
            'first3Dsection': 1,
            'warnSaveSection': True,
            'listObjectRange': True,
            'defaultMode': -11,
            'heightUseProxies': 1536,
            'shiftIncrement': (0.11, 100.0, 100.0, 1.05, 1.05, 0.1, 0.1, 0.005, 0.005),
            'viewport': (-1.85496, -7.74495, 0.0213713),
            'listDomainLength': False,
            'facets3D': 8,
            'listObjectVolume': True,
            'brightStopWhen': 0,
            'listDomainArea': False,
            'listDomainPixelsize': True,
            'widthUseProxies': 2048,
            'gridNumber': (1.0, 1.0),
            'units': 'microns',
            'listDomainSource': True,
            'dim3D': (-1.0, -1.0, -1.0),
            'zMidSection': False,
            'listTraceArea': True,
            'autoSaveSeries': True,
            'last3Dsection': 2147483647,
            'offset3D': (0.0, 0.0, 0.0),
            'defaultComment': '',
            'brightStopValue': 100,
            'beepPaging': True,
            'tracesStopWhen': False,
            'listZTraceRange': True,
        }
        self.assertTrue(series_attributes, expected_attributes)

    def test_extract_transform_attributes(self):
        node = etree.parse(os.path.join(DATA_LOC, "_transform.xml")).getroot()
        transform_attributes = reconstruct_reader.extract_transform_attributes(
            node)
        expected_attributes = {
            'dim': 0,
            'ycoef': [0, 0, 1, 0, 0, 0],
            'xcoef': [0, 1, 0, 0, 0, 0],
        }
        self.assertTrue(transform_attributes, expected_attributes)

    def test_extract_zcontour_attributes(self):
        node = etree.parse(os.path.join(DATA_LOC, "_zcontour.xml")).getroot()
        zcontour_attributes = reconstruct_reader.extract_zcontour_attributes(
            node)
        expected_attributes = {
            'name': 'd110_ztrace_01_down_02',
            'points': [
                (18.6537, 15.3916, 5),
                (18.6655, 15.3621, 6),
                (18.7186, 15.368, 7),
                (18.99, 15.4506, 8),
                (18.9428, 15.5627, 10),
                (18.872, 15.6217, 12),
                (18.8897, 15.5686, 14),
                (18.7776, 15.5332, 16),
                (18.7717, 15.6158, 19),
                (18.7717, 15.663, 21),
                (18.8071, 15.6276, 23),
                (18.8189, 15.5863, 25),
                (18.813, 15.545, 27),
                (18.8366, 15.4801, 29),
                (18.872, 15.3857, 31),
                (18.9428, 15.3798, 33),
                (18.9074, 15.3267, 34),
                (19.1257, 15.2736, 36),
                (19.1493, 15.3208, 39),
                (19.2554, 15.3326, 41),
                (19.397, 15.3562, 44),
                (19.5268, 15.3798, 46),
            ],
            'mode': 11,
            'closed': False,
            'border': (1.0, 0.5, 0.0),
            'fill': (1.0, 0.5, 0.0),
        }
        self.assertEqual(zcontour_attributes, expected_attributes)
