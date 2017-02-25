""" Module containing backend methods for PyRECONSTRUCT's mergetool.
"""
from .models import Base, Contour, ContourMatch

from .utils import is_contacting, is_exact_duplicate, is_potential_duplicate


def create_database(engine):
    """ Uses the provided engine to create the database.
    """
    Base.metadata.create_all(engine)


def get_section_contours_from_database(section_number):
    """ Returns the db.Contour objects in the provided section_number.
    """
    return session.query(
        Contour
    ).filter(
        Contour.section == section_number
    ).all()


def get_matches(match_type=None):
    """ Returns db.ContourMatch objects.

        Can provide a match_type to return only those of a particular match_type.
    """
    query = session.query(
        ContourMatch.id1,
        ContourMatch.id2,
        ContourMatch.match_type
    )
    if match_type:
        query = query.filter(
            ContourMatch.match_type == match_type
        )
    return query.all()


def _create_db_contours_from_pyrecon_section(section):
    """ Returns db.Contour objects for contours in a pyrecon.Section.
    """
    db_contours = []
    for i, pyrecon_contour in enumerate(section.contours):
        db_contour = Contour(
            section=section.index,
            index=i
        )
        db_contours.append(db_contour)
    return db_contours


def load_db_contours_from_pyrecon_section(session, section):
    """ From a pyrecon.Section object, inster db.Contour entities into the db.
    """
    db_contours = _create_db_contours_from_pyrecon_section(section)
    session.add_all(db_contours)
    session.commit()
    return db_contours


def _create_db_contourmatch_from_db_contours_and_pyrecon_section(db_contour_A, db_contour_B,
                                                                 section):
    """ Returns a db.ContourMatch from 2 db.Contours and a pyrecon.section, or None.
    """
    pyrecon_contour_a = section.contours[db_contour_A.index]
    pyrecon_contour_b = section.contours[db_contour_B.index]
    if pyrecon_contour_a.name != pyrecon_contour_b.name:
        db_match = None
    elif pyrecon_contour_a.shape != pyrecon_contour_b.shape:
        # TODO: this could be problematic (e.g. polygon vs linestring)
        db_match = None
    elif not is_contacting(pyrecon_contour_a.shape, pyrecon_contour_b.shape):
        db_match = None
    elif is_exact_duplicate(pyrecon_contour_a.shape, pyrecon_contour_b.shape):
        db_match = ContourMatch(
            id1=db_contour_A.id,
            id2=db_contour_B.id,
            match_type="exact"
        )
    elif is_potential_duplicate(pyrecon_contour_a.shape, pyrecon_contour_b.shape):
        if (pyrecon_contour_a.points == pyrecon_contour_b.points) and \
           (pyrecon_contour_a.transform != pyrecon_contour_b.transform):
            # TODO: consider better pushing this logic down into the core
            # pyrecon classes
            match_type = "potential_realigned"
        else:
            match_type = "potential"
        db_match = ContourMatch(
            id1=db_contour_A.id,
            id2=db_contour_B.id,
            match_type=match_type
        )
    return db_match


def _create_db_contourmatches_from_db_contours_and_pyrecon_section(db_contours, section):
    """ Returns db.ContourMatch objects for contours in a pyrecon.Section.
    """
    matches = []
    for idx, db_contour_A in enumerate(db_contours):
        contA = section.contours[db_contour_A.index]
        for idy, db_contour_B in enumerate(db_contours):
            contB = section.contours[db_contour_B.index]
            if idx >= idy:
                continue
            match = _create_db_contourmatch_from_db_contours_and_pyrecon_section(
                db_contour_A, db_contour_B, section)
            if match:
                matches.append(match)
    return matches


def load_db_contourmatches_from_db_contours_and_pyrecon_section(session, db_contours, section):
    """ From a pyrecon.Section object, insert db.ContourMatch entities into the db.
    """
    db_contourmatches = _create_db_contourmatches_from_db_contours_and_pyrecon_section(
        db_contours, section)
    session.add_all(db_contourmatches)
    session.commit()
    return db_contourmatches
