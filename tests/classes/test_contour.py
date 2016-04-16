from unittest import TestCase

from pyrecon.classes import Contour, Transform


class ContourTests(TestCase):

    def test_popShape_polygon(self):
        transform = Transform(
            dim=0,
            xcoef=[0, 1, 0, 0, 0, 0],
            ycoef=[0, 0, 1, 0, 0, 0],
        )
        poly_contour = Contour(
            closed=True,
            points=[
                (19.2342, 15.115),
                (19.2826, 15.115),
                (19.2584, 15.1593),
            ],
            transform=transform,
        )
        poly_contour.popShape()
        self.assertEqual(poly_contour.shape.type, "Polygon")

    def test_popShape_line(self):
        transform = Transform(
            dim=0,
            xcoef=[0, 1, 0, 0, 0, 0],
            ycoef=[0, 0, 1, 0, 0, 0],
        )
        line_contour = Contour(
            closed=False,
            points=[
                (24.6589, 17.3004),
                (24.7018, 17.3489),
                (24.7634, 17.3917),
                (24.8174, 17.4197),
            ],
            transform=transform,
        )
        line_contour.popShape()
        self.assertEqual(line_contour.shape.type, "LineString")

    def test_popShape_point(self):
        transform = Transform(
            dim=0,
            xcoef=[0, 1, 0, 0, 0, 0],
            ycoef=[0, 0, 1, 0, 0, 0],
        )
        point_contour = Contour(
            closed=False,
            points=[(13.5904, 16.6472)],
            transform=transform,
        )
        point_contour.popShape()
        self.assertEqual(point_contour.shape.type, "Point")

    def test_overlaps_polygon(self):
        transform = Transform(
            dim=0,
            xcoef=[0, 1, 0, 0, 0, 0],
            ycoef=[0, 0, 1, 0, 0, 0],
        )
        poly_contour = Contour(
            closed=True,
            points=[
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
            ],
            transform=transform,
        )

        # Test 100% overlap
        overlap = poly_contour.overlaps(poly_contour)
        self.assertEqual(overlap, 1)

        # Not even close
        different_poly_contour = Contour(
            closed=True,
            points=[
                (9.2342, 5.115),
                (9.2826, 5.115),
                (9.2584, 5.1593),
            ],
            transform=transform,
        )
        overlap = poly_contour.overlaps(different_poly_contour)
        self.assertEqual(overlap, 0)

        # Potential duplicate -> needs resolution
        close_poly_contour = Contour(
            closed=True,
            points=[
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
            ],
            transform=transform,
        )
        overlap = poly_contour.overlaps(close_poly_contour)
        self.assertTrue(overlap > 1)

    def test_overlaps_line(self):
        transform = Transform(
            dim=0,
            xcoef=[0, 1, 0, 0, 0, 0],
            ycoef=[0, 0, 1, 0, 0, 0],
        )
        line_contour = Contour(
            closed=False,
            points=[
                (24.6589, 17.3004),
                (24.7018, 17.3489),
                (24.7634, 17.3917),
                (24.8174, 17.4197),
            ],
            transform=transform,
        )

        # Test 100% overlap
        overlap = line_contour.overlaps(line_contour)
        self.assertEqual(overlap, 1)

        # Not even close
        different_line_contour = Contour(
            closed=False,
            points=[
                (14.6589, 7.3004),
                (14.7018, 7.3489),
                (14.7634, 7.3917),
                (14.8174, 7.4197),
            ],
            transform=transform,
        )
        overlap = line_contour.overlaps(different_line_contour)
        self.assertEqual(overlap, 0)

    def test_overlaps_point(self):
        transform = Transform(
            dim=0,
            xcoef=[0, 1, 0, 0, 0, 0],
            ycoef=[0, 0, 1, 0, 0, 0],
        )
        point_contour = Contour(
            closed=False,
            points=[(13.5904, 16.6472)],
            transform=transform,
        )

        # Test 100% overlap
        overlap = point_contour.overlaps(point_contour)
        self.assertEqual(overlap, 1)

        # Not even close
        different_point_contour = Contour(
            closed=False,
            points=[(14.5904, 16.6472)],
            transform=transform,
        )
        overlap = point_contour.overlaps(different_point_contour)
        self.assertEqual(overlap, 0)
