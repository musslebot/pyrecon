from unittest import TestCase

from pyrecon.classes import Contour, Transform


class ContourTests(TestCase):

    def test_shape_polygon(self):
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
        self.assertEqual(poly_contour.shape.type, "Polygon")

    def test_shape_line(self):
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
        self.assertEqual(line_contour.shape.type, "LineString")

    def test_shape_point(self):
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
        self.assertEqual(point_contour.shape.type, "Point")
