"""Merge two RECONSTRUCT datasets."""
from shapely.geometry import box, LinearRing, LineString, Point, Polygon

from pyrecon.classes import Series, Section
from pyrecon.tools import reconstruct_writer

TOLERANCE = 1 + 2**-17
LIMIT = 10.0


def is_reverse(shape):
    """ Return True if shape is a RECONSTRUCT reverse trace (negative area).
    """
    if isinstance(shape, Polygon):
        ring = LinearRing(shape.exterior.coords)
        # RECONSTRUCT is opposite for some reason
        return not ring.is_ccw
    return False


def is_contacting(shape1, shape2):
    """ Return True if two shapes are contacting.
    """
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
    """ Return True if two shapes are exact duplicates (within tolerance).
    """
    if isinstance(shape1, Point) and isinstance(shape2, Point):
        # TODO: investigate more sophisticated comparison
        return shape1.equals(shape2)

    elif isinstance(shape1, Polygon) and isinstance(shape2, Polygon):
        if shape1.has_z and shape2.has_z:
            return shape1.exterior.equals(shape2.exterior)
        else:
            if is_reverse(shape1) != is_reverse(shape2):
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


# TODO: investigate way to reduce shared computation with is_duplicate
# TODO: investigate if support needed for LineString
def is_potential_duplicate(shape1, shape2, threshold=TOLERANCE, upper_bound=LIMIT):
    """ Return True if two shapes are potential overlaps (exceed tolerance).
    """
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
        if threshold <= union_over_intersection < upper_bound:
            return True
        else:
            return False

    elif isinstance(shape1, LineString) and isinstance(shape2, LineString):
        # TODO: investigate more sophisticated comparison
        return shape1.almost_equals(shape2) and not shape1.equals(shape2)

    raise Exception("No support for shape type(s): {}".format(
        set([shape1.type, shape2.type])))
