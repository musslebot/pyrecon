from unittest import TestCase

import numpy
from shapely.geometry import LineString, Point, Polygon

from pyrecon.tools.mergetool import utils


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

    def test_is_reverse(self):
        reverse_points = self.polygon_points[::-1]
        reverse_polygon = Polygon(numpy.asarray(reverse_points))
        self.assertTrue(utilsis_reverse(reverse_polygon))

        polygon = Polygon(numpy.asarray(self.polygon_points))
        self.assertFalse(utilsis_reverse(polygon))

    def test_is_contacting_point(self):
        point_points = [(13.5904, 16.6472)]
        point = Point(*numpy.asarray(point_points))

        # Test same point
        self.assertTrue(utilsis_contacting(point, point))

        # Not even close
        far_point_points = [(14.5904, 16.6472)]
        far_point = Point(*numpy.asarray(far_point_points))
        self.assertFalse(utilsis_contacting(point, far_point))

    def test_is_contacting_polygon(self):
        polygon = Polygon(numpy.asarray(self.polygon_points))

        # Test same polygon
        self.assertTrue(utilsis_contacting(polygon, polygon))

        # Not even close
        far_polygon_points = [
            (9.2342, 5.115),
            (9.2826, 5.115),
            (9.2584, 5.1593),
        ]
        far_polygon = Polygon(numpy.asarray(far_polygon_points))
        self.assertFalse(utilsis_contacting(polygon, far_polygon))

        # Potential duplicate
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
        self.assertTrue(utilsis_contacting(polygon, close_polygon))

        # 3D Polygon
        three_dim_polygon_points = [
            [19.5386, 15.368, 46.0],
            [19.456, 15.3857, 45.0],
            [19.3793, 15.3031, 43.0],
            [19.2731, 15.3149, 40.0],
            [19.2024, 15.3444, 39.0],
            [19.1493, 15.2913, 37.0],
            [18.9487, 15.368, 33.0],
            [18.8661, 15.3562, 31.0],
            [18.8543, 15.4152, 29.0],
            [18.8071, 15.4919, 27.0],
            [18.8071, 15.5568, 26.0],
            [18.8012, 15.6335, 20.0],
            [18.8012, 15.5804, 19.0],
            [18.7835, 15.5568, 14.0],
            [18.8779, 15.5509, 11.0],
            [18.8779, 15.4683, 8.0],
            [18.754, 15.4034, 7.0],
            [18.6419, 15.4034, 5.0],
        ]
        three_dim_polygon = Polygon(numpy.asarray(three_dim_polygon_points))
        self.assertTrue(
            utilsis_contacting(three_dim_polygon, three_dim_polygon))

    def test_is_contacting_line(self):
        line_points = [
            (24.6589, 17.3004),
            (24.7018, 17.3489),
            (24.7634, 17.3917),
            (24.8174, 17.4197),
        ]
        line = LineString(numpy.asarray(line_points))

        # Test 100% overlap
        self.assertTrue(utilsis_contacting(line, line))

        # Not even close
        different_line_points = [
            (14.6589, 7.3004),
            (14.7018, 7.3489),
            (14.7634, 7.3917),
            (14.8174, 7.4197),
        ]
        different_line = LineString(numpy.asarray(different_line_points))
        self.assertFalse(utilsis_contacting(line, different_line))

        # Simple line (no interior or exterior)
        simple_line_points = [
            (5.64847, 18.996),
            (11.7753, 18.996),
        ]
        simple_line = LineString(numpy.asarray(simple_line_points))
        self.assertTrue(utilsis_contacting(simple_line, simple_line))

    def test_is_exact_duplicate_point(self):
        point_points = [(13.5904, 16.6472)]
        point = Point(*numpy.asarray(point_points))

        # Test same point
        self.assertTrue(utilsis_exact_duplicate(point, point))

        # Not even close
        far_point_points = [(14.5904, 16.6472)]
        far_point = Point(*numpy.asarray(far_point_points))
        self.assertFalse(utilsis_exact_duplicate(point, far_point))

    def test_is_exact_duplicate_polygon(self):
        polygon = Polygon(numpy.asarray(self.polygon_points))

        # Test same polygon
        self.assertTrue(utilsis_exact_duplicate(polygon, polygon))

        # Not even close
        far_polygon_points = [
            (9.2342, 5.115),
            (9.2826, 5.115),
            (9.2584, 5.1593),
        ]
        far_polygon = Polygon(numpy.asarray(far_polygon_points))
        self.assertFalse(utilsis_exact_duplicate(polygon, far_polygon))

        # Potential duplicate
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
        # Potential is not exact
        self.assertFalse(utilsis_exact_duplicate(polygon, close_polygon))

        # 3D Polygon
        three_dim_polygon_points = [
            [19.5386, 15.368, 46.0],
            [19.456, 15.3857, 45.0],
            [19.3793, 15.3031, 43.0],
            [19.2731, 15.3149, 40.0],
            [19.2024, 15.3444, 39.0],
            [19.1493, 15.2913, 37.0],
            [18.9487, 15.368, 33.0],
            [18.8661, 15.3562, 31.0],
            [18.8543, 15.4152, 29.0],
            [18.8071, 15.4919, 27.0],
            [18.8071, 15.5568, 26.0],
            [18.8012, 15.6335, 20.0],
            [18.8012, 15.5804, 19.0],
            [18.7835, 15.5568, 14.0],
            [18.8779, 15.5509, 11.0],
            [18.8779, 15.4683, 8.0],
            [18.754, 15.4034, 7.0],
            [18.6419, 15.4034, 5.0],
        ]
        three_dim_polygon = Polygon(numpy.asarray(three_dim_polygon_points))
        self.assertTrue(
            utilsis_exact_duplicate(three_dim_polygon, three_dim_polygon))

        # Close 3D Polygon
        close_three_dim_polygon_points = [
            [19.4386, 15.368, 46.0],
            [19.456, 15.3857, 45.0],
            [19.3793, 15.3031, 43.0],
            [19.2731, 15.3149, 40.0],
            [19.2024, 15.3444, 39.0],
            [19.1493, 15.2913, 37.0],
            [18.9487, 15.368, 33.0],
            [18.8661, 15.3562, 31.0],
            [18.8543, 15.4152, 29.0],
            [18.8071, 15.4919, 27.0],
            [18.8071, 15.5568, 26.0],
            [18.8012, 15.6335, 20.0],
            [18.8012, 15.5804, 19.0],
            [18.7835, 15.5568, 14.0],
            [18.8779, 15.5509, 11.0],
            [18.8779, 15.4683, 8.0],
            [18.754, 15.4034, 7.0],
            [18.6419, 15.4034, 5.0],
        ]
        close_three_dim_polygon = Polygon(
            numpy.asarray(close_three_dim_polygon_points))
        self.assertFalse(utilsis_exact_duplicate(
            three_dim_polygon, close_three_dim_polygon))

    def test_is_exact_duplicate_line(self):
        line_points = [
            (24.6589, 17.3004),
            (24.7018, 17.3489),
            (24.7634, 17.3917),
            (24.8174, 17.4197),
        ]
        line = LineString(numpy.asarray(line_points))

        # Test 100% overlap
        self.assertTrue(utilsis_exact_duplicate(line, line))

        # Not even close
        different_line_points = [
            (14.6589, 7.3004),
            (14.7018, 7.3489),
            (14.7634, 7.3917),
            (14.8174, 7.4197),
        ]
        different_line = LineString(numpy.asarray(different_line_points))
        self.assertFalse(utilsis_exact_duplicate(line, different_line))

        # 3D line
        three_dim_line_points = [
            (23.2919, 16.2786, 52),
            (23.3781, 17.6027, 19),
        ]
        three_dim_line = LineString(numpy.asarray(three_dim_line_points))
        self.assertTrue(
            utilsis_exact_duplicate(three_dim_line, three_dim_line))

        # Close 3D line
        close_three_dim_line_points = [
            (23.3919, 16.2786, 52),
            (23.3781, 17.6027, 19),
        ]
        close_three_dim_line = LineString(
            numpy.asarray(close_three_dim_line_points))
        self.assertFalse(utilsis_exact_duplicate(
            three_dim_line, close_three_dim_line))

    def test_is_potential_duplicate_point(self):
        point_points = [(13.5904, 16.6472)]
        point = Point(*numpy.asarray(point_points))

        # Exact is not potential
        self.assertFalse(utilsis_potential_duplicate(point, point))

        # Not even close
        far_point_points = [(14.5904, 16.6472)]
        far_point = Point(*numpy.asarray(far_point_points))
        self.assertFalse(utilsis_potential_duplicate(point, far_point))

    def test_is_potential_duplicate_polygon(self):
        polygon = Polygon(numpy.asarray(self.polygon_points))

        # Exact is not potential
        self.assertFalse(utilsis_potential_duplicate(polygon, polygon))

        # Not even close
        far_polygon_points = [
            (9.2342, 5.115),
            (9.2826, 5.115),
            (9.2584, 5.1593),
        ]
        far_polygon = Polygon(numpy.asarray(far_polygon_points))
        self.assertFalse(
            utilsis_potential_duplicate(polygon, far_polygon))

        # Potential duplicate
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
        self.assertTrue(
            utilsis_potential_duplicate(polygon, close_polygon))

    def test_is_potential_duplicate_line(self):
        line_points = [
            (24.6589, 17.3004),
            (24.7018, 17.3489),
            (24.7634, 17.3917),
            (24.8174, 17.4197),
        ]
        line = LineString(numpy.asarray(line_points))

        # Exact is not potential
        self.assertFalse(utilsis_potential_duplicate(line, line))

        # Not even close
        different_line_points = [
            (14.6589, 7.3004),
            (14.7018, 7.3489),
            (14.7634, 7.3917),
            (14.8174, 7.4197),
        ]
        different_line = LineString(numpy.asarray(different_line_points))
        self.assertFalse(
            utilsis_potential_duplicate(line, different_line))
