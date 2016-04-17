from unittest import TestCase

import numpy
from shapely.geometry import LineString, Point, Polygon

from pyrecon.tools import mergetool


class MergetoolTests(TestCase):
    polygon_points = [
        (15.1004, 17.5202),
        (15.5318, 17.4613),
        (15.5857, 17.4545),
        (15.5925, 17.4528),
        (15.6194, 17.4579),
        (15.6228, 17.4579),
        (15.8385, 17.6567),
        (15.8924, 17.7073),
        (15.9177, 17.7326),
        (15.9278, 17.7461),
        (15.9329, 17.7528),
        (15.9834, 17.9685),
        (16.007, 18.0763),
        (16.0137, 18.1033),
        (16.0171, 18.1168),
        (16.0188, 18.1235),
        (16.0137, 18.1286),
        (15.798, 18.2061),
        (15.6902, 18.2432),
        (15.6767, 18.2482),
        (15.6733, 18.2499),
        (15.242, 17.9567),
        (15.2285, 17.9483),
        (15.2234, 17.9415),
        (15.1611, 17.7258),
        (15.1291, 17.618),
        (15.1139, 17.5641),
        (15.1055, 17.5371),
        (15.1021, 17.5236),
        (15.1004, 17.5219),
    ]

    def test_get_bounding_box(self):
        polygon = Polygon(numpy.asarray(self.polygon_points))
        box = mergetool.get_bounding_box(polygon)
        self.assertEqual(box.bounds, (15.1004, 17.4528, 16.0188, 18.2499))

    def test_is_reverse(self):
        reverse_points = self.polygon_points[::-1]
        reverse_polygon = Polygon(numpy.asarray(reverse_points))
        self.assertTrue(mergetool.is_reverse(reverse_polygon))

        polygon = Polygon(numpy.asarray(self.polygon_points))
        self.assertFalse(mergetool.is_reverse(polygon))

    def test_overlaps_polygon(self):
        polygon = Polygon(numpy.asarray(self.polygon_points))

        # Test 100% overlap
        overlap = mergetool.overlaps(polygon, polygon)
        self.assertEqual(overlap, 1)

        # Not even close
        different_polygon_points = [
            (9.2342, 5.115),
            (9.2826, 5.115),
            (9.2584, 5.1593),
        ]
        different_polygon = Polygon(numpy.asarray(different_polygon_points))
        overlap = mergetool.overlaps(polygon, different_polygon)
        self.assertEqual(overlap, 0)

        # Potential duplicate -> needs resolution
        close_polygon_points = [
            (15.0988, 17.5196),
            (15.3815, 17.4754),
            (15.5229, 17.4577),
            (15.5936, 17.4489),
            (15.6289, 17.4577),
            (15.9116, 17.7228),
            (15.9381, 17.7581),
            (16.0088, 18.0408),
            (16.0265, 18.1115),
            (16.0265, 18.1292),
            (15.7437, 18.2263),
            (15.6731, 18.2529),
            (15.3904, 18.0673),
            (15.249, 17.9701),
            (15.2225, 17.9436),
            (15.143, 17.6609),
            (15.0988, 17.5284),
        ]
        close_polygon = Polygon(numpy.asarray(close_polygon_points))
        overlap = mergetool.overlaps(polygon, close_polygon)
        self.assertTrue(overlap > 1)

    def test_overlaps_line(self):
        line_points = [
            (24.6589, 17.3004),
            (24.7018, 17.3489),
            (24.7634, 17.3917),
            (24.8174, 17.4197),
        ]
        line = LineString(numpy.asarray(line_points))

        # Test 100% overlap
        overlap = mergetool.overlaps(line, line)
        self.assertEqual(overlap, 1)

        # Not even close
        different_line_points = [
            (14.6589, 7.3004),
            (14.7018, 7.3489),
            (14.7634, 7.3917),
            (14.8174, 7.4197),
        ]
        different_line = LineString(numpy.asarray(different_line_points))
        overlap = mergetool.overlaps(line, different_line)
        self.assertEqual(overlap, 0)

    def test_overlaps_point(self):
        point_points = [(13.5904, 16.6472)]
        point = Point(*numpy.asarray(point_points))

        # Test 100% overlap
        overlap = mergetool.overlaps(point, point)
        self.assertEqual(overlap, 1)

        # Not even close
        different_point_points = [(14.5904, 16.6472)]
        different_point = Point(*numpy.asarray(different_point_points))
        overlap = mergetool.overlaps(point, different_point)
        self.assertEqual(overlap, 0)
