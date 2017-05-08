""" Module containing backend methods for PyRECONSTRUCT's mergetool.
"""
from collections import defaultdict
from copy import deepcopy
import itertools

import numpy
from PIL import Image

from .models import Base, Contour, ContourMatch
from .utils import is_contacting, is_exact_duplicate, is_potential_duplicate


def create_database(engine):
    """ Uses the provided engine to create the database.
    """
    Base.metadata.create_all(engine)


def query_all_contours_in_section(session, section_number):
    return session.query(
        Contour
    ).filter(
        Contour.section == section_number
    )


def _create_db_contours_from_pyrecon_section(section, series_number):
    """ Returns db.Contour objects for contours in a pyrecon.Section.
    """
    db_contours = []
    # TODO: multithread this
    for i, pyrecon_contour in enumerate(section.contours):
        db_contour = Contour(
            section=section.index,
            index=i,
            series=series_number
        )
        db_contours.append(db_contour)
    return db_contours


def load_db_contours_from_pyrecon_section(session, section, series_number):
    """ From a pyrecon.Section object, inster db.Contour entities into the db.
    """
    db_contours = _create_db_contours_from_pyrecon_section(section, series_number)
    session.add_all(db_contours)
    session.commit()
    return db_contours


def _create_db_contourmatch_from_db_contours_and_pyrecon_series_list(db_contour_A,
                                                                     db_contour_B,
                                                                     series_list):
    """ Returns a db.ContourMatch from 2 db.Contours and a pyrecon.section, or None.
    """
    pyrecon_contour_a = series_list[
        db_contour_A.series
    ].sections[
        db_contour_A.section
    ].contours[
        db_contour_A.index
    ]
    pyrecon_contour_b = series_list[
        db_contour_B.series
    ].sections[
        db_contour_B.section
    ].contours[
        db_contour_B.index
    ]
    if pyrecon_contour_a.name != pyrecon_contour_b.name:
        return None
    elif pyrecon_contour_a.shape.type != pyrecon_contour_b.shape.type:
        return None

    shape_a = pyrecon_contour_a.shape
    shape_b = pyrecon_contour_b.shape
    try:
        if (pyrecon_contour_a.points == pyrecon_contour_b.points) and \
           (pyrecon_contour_a.transform != pyrecon_contour_b.transform):
            match_type = "potential_realigned"
            return ContourMatch(
                id1=db_contour_A.id,
                id2=db_contour_B.id,
                match_type=match_type
            )
        elif not is_contacting(shape_a, shape_b):
            return None
        elif is_exact_duplicate(shape_a, shape_b):
            match_type = "exact"
            return ContourMatch(
                id1=db_contour_A.id,
                id2=db_contour_B.id,
                match_type=match_type
            )
        elif is_potential_duplicate(shape_a, shape_b):
            match_type = "potential"
            return ContourMatch(
                id1=db_contour_A.id,
                id2=db_contour_B.id,
                match_type=match_type
            )
    except Exception as e:
        # This is here because if an Exception is raised, we need to figure out
        # wtf happened
        import pdb; pdb.set_trace()
        print("{}".format(e))
    return None


def _create_db_contourmatches_from_db_contours_and_pyrecon_series_list(db_contours, series_list):
    """ Returns db.ContourMatch objects for contours in a pyrecon.Section.
    """
    matches = []
    # TODO: multithread this?
    for idx, db_contour_A in enumerate(db_contours):
        for idy, db_contour_B in enumerate(db_contours):
            if idx >= idy:
                continue
            match = _create_db_contourmatch_from_db_contours_and_pyrecon_series_list(
                db_contour_A, db_contour_B, series_list)
            if match:
                matches.append(match)
    return matches


def load_db_contourmatches_from_db_contours_and_pyrecon_series_list(session, db_contours,
                                                                    series_list):
    """ From a pyrecon.Section object, insert db.ContourMatch entities into the db.
    """
    db_contourmatches = _create_db_contourmatches_from_db_contours_and_pyrecon_series_list(
        db_contours, series_list)
    session.add_all(db_contourmatches)
    session.commit()
    return db_contourmatches


def get_exact_matches_for_db_id(session, db_id):
    query = session.query(
        ContourMatch.id1,
        ContourMatch.id2
    ).filter(
        ((ContourMatch.id1 == db_id) | (ContourMatch.id2 == db_id)) &
        (ContourMatch.match_type == "exact")
    )
    matches = []
    for m in query:
        match_id = m[0] if m[0] != db_id else m[1]
        matches.append(match_id)
    return matches


# =======================
# TODO: cleanup below vvv
# =======================
def cleanup_redundant_matches(session):
    """ Removes redundant ContourMatch objects that occur when:
        1) There are potentials in one series, that also exist in other series.
           This is exists because each of these contourmatches have unique ids,
           masked by different exacts.
    """
    potential_query = session.query(
        ContourMatch
    ).filter(
        (ContourMatch.match_type == "potential") |
        (ContourMatch.match_type == "potential_realigned")
    )
    for match in potential_query:
        id_ = match.id1
        id_matches = get_exact_matches_for_db_id(session, id_)
        for id_exact in id_matches:
            if id_exact > id_:
                for thing in session.query(ContourMatch).filter(
                        (ContourMatch.id1 == id_exact) |
                        (ContourMatch.id2 == id_exact) &
                        (ContourMatch.match_type == "potential")
                    ):
                    session.delete(thing)
    session.commit()


def _retrieve_matches_for_db_contour_id(session, db_contour_id):
    """ Returns all ContourMatch objects that match the provided db_contour_id.
    """
    return session.query(
        ContourMatch
    ).filter(
        ContourMatch.id1 == db_contour_id
    ).all()


def group_section_matches(session, section_number):
    grouped = defaultdict(lambda: defaultdict(set))
    query = session.query(
        Contour.id
    ).filter(
        Contour.section==section_number
    )
    for id_ in query:
        id_ = id_[0]
        matches = _retrieve_matches_for_db_contour_id(session, id_)
        grouped[id_] = defaultdict(set)
        for m in matches:
            grouped[m.id1][m.match_type].add(m.id2)
    return grouped


def transform_contour_for_frontend(contour, db_id, section, series_name, keep=True):
    """ Converts a contour to a dict expected by the frontend.
    """
    #converting to pixels
    contour_copy = deepcopy(contour)
    contour_copy.points = list(map(tuple, contour_copy.transform._tform.inverse(
        numpy.asarray(contour_copy.points)/section.images[0].mag)))
    nullPoints = contour_copy.shape.bounds

    flipVector = numpy.array([1, -1])
    im = Image.open(section.images[0]._path + "/{}".format(section.images[0].src))
    imWidth, imHeight = im.size
    translationVector = numpy.array([0, imHeight])

    if contour_copy.shape.type == "Polygon":
        transformedPoints = list(map(tuple, translationVector+(numpy.array(list(contour_copy.shape.exterior.coords))*flipVector)))

    else:
        x, y = contour_copy.shape.xy
        x = list(x)
        y = list(y)
        coords = zip(x,y)
        transformedPoints = list(map(tuple, translationVector+(numpy.array(list(coords))*flipVector)))
    contour_copy.points = transformedPoints

    #cropping
    minx, miny, maxx, maxy = contour_copy.shape.bounds
    x = minx-100
    y = miny - 100
    width = maxx-x+100
    height = maxy-y+100
    rect = [x, y, width, height]
    cropVector = numpy.array([x,y])
    croppedPoints = list(map(tuple, numpy.array(contour_copy.points)-cropVector))

    return {
        'name': contour.name,
        'points': contour.points,
        'image': section.images[0]._path + "/{}".format(section.images[0].src),
        'db_id': db_id,
        'series': series_name,
        'nullpoints': nullPoints,
        'rect': rect,
        'croppedPoints': croppedPoints,
        'keepBool': keep,
        'section': section.index
    }


def prepare_unique_query(session, section_index):
    """ Return a query for unique db contour ids in a section.
    """
    id1_matches_query = session.query(
        ContourMatch.id1
    ).filter(
        ContourMatch.id1.in_(
            session.query(
                Contour.id
            ).filter(
                Contour.section == section_index
            )
        )
    )
    id2_matches_query = session.query(
        ContourMatch.id2
    ).filter(
        ContourMatch.id2.in_(
            session.query(
                Contour.id
            ).filter(
                Contour.section == section_index
            )
        )
    )
    matched_ids_union = id1_matches_query.union(id2_matches_query)
    return session.query(Contour.id).filter(
        Contour.id.notin_(matched_ids_union),
        Contour.section == section_index
    )


def prepare_frontend_payload(session, series_list):
    series_matches = {
        "series": [s.path for s in series_list],
        "sections": {}
    }
    section_indices = set()
    for series in series_list:
        section_indices.update(series.sections.keys())
    for section_index in section_indices:
        grouped = group_section_matches(session, section_index)
        series_matches["sections"][section_index] = _prepare_frontend_payload_for_section(
            session, series_list, section_index, grouped)
    return series_matches


def _prepare_frontend_payload_for_section(session, series_list, section_index, grouped):
    section_matches = {
        "section": section_index,
        "exact": [],
        "potential": [],
        "potential_realigned": [],
        "unique": []
    }
    def _is_already_exact(id1, id2):
        """ Returns True if there is an exact match between id1 and id2.
        """
        if session.query(ContourMatch).filter(
                ((ContourMatch.id1==id1) & (ContourMatch.id2==id2)) |
                ((ContourMatch.id1==id2) & (ContourMatch.id2==id1)) &
                (ContourMatch.match_type == "exact")
            ).count():
            return True
        return False

    # TODO: clean and test this VVV
    # TODO: multithread this
    for contour_A_id, match_dict in grouped.items():
        db_contour_A = session.query(Contour).get(contour_A_id)
        series_A = series_list[db_contour_A.series]
        section_A = series_A.sections[section_index]
        reconstruct_contour_a = section_A.contours[db_contour_A.index]
        main_contour_data = transform_contour_for_frontend(
            reconstruct_contour_a,
            contour_A_id,
            section_A,
            series_A.name,
            keep=True
        )
        keep_types = ["potential", "potential_realigned"]
        for match_type, matches in match_dict.items():
            match_list = [main_contour_data]
            keep = True if match_type in keep_types else False
            # NOTE: we need to prevent matching potentials where there are already
            #       exacts whithin the same group. Dot product all matches to check
            #       for exacts.
            # e.g.
            # There exists:
            #   A0-exact-B0
            #   A1-exact`B1
            #   A0-potential-A1
            #   A0-potential-B1
            #   A1-potential-B0
            #   B0-potential-B1
            #
            # Returns:
            #   exact(A0,B0),
            #   exact(A1,B1),
            #   potential(A0,A1,B1), <-- A1 & B1 are exact > only need potential(A0,A1)
            #   potential(A1,BO), <-- B0 and A0 are exact > redundant with ^
            #   potential(B0,B1) <-- redundant with potential(A0,B1)
            if match_type in ["potential", "potential_realigned"]:
                dot_matches = itertools.combinations(matches, 2)
                for m1,m2 in dot_matches:
                    if m2 in matches and _is_already_exact(m1,m2):
                        # TODO: verify this
                        matches.remove(m2)
            for match_id in matches:
                db_contour_B = session.query(Contour).get(match_id)
                series_B = series_list[db_contour_B.series]
                section_B = series_B.sections[section_index]
                reconstruct_contour_b = section_B.contours[db_contour_B.index]
                match_dict = transform_contour_for_frontend(
                    reconstruct_contour_b,
                    match_id,
                    section_B,
                    series_B.name,
                    keep=keep
                )
                match_list.append(match_dict)
            if len(match_list) > 1:
                section_matches[match_type].append(match_list)

    # Add uniques to payload
    unique_ids_query = prepare_unique_query(session, section_index)
    for unique_id in unique_ids_query:
        unique_id = unique_id[0]
        db_contour_unique = session.query(Contour).get(unique_id)
        series_C = series_list[db_contour_unique.series]
        section_C = series_C.sections[db_contour_unique.section]
        unique_reconstruct_contour = section_C.contours[db_contour_unique.index]
        unique_dict = transform_contour_for_frontend(
            unique_reconstruct_contour,
            unique_id,
            section_C,
            series_C.name,
            keep=True
        )
        section_matches['unique'].append([unique_dict])
    return section_matches


def _get_output_contours_from_section_dict(session, section_dict):
    pop_ids = set()
    to_keep = {}
    types = [
        "exact",
        "unique"
    ]
    # TODO: multithread this
    for type_ in types:
        for type_set in section_dict[type_]:
            for contour_dict in type_set:
                if contour_dict.get("keepBool", False):
                    db_id = contour_dict["db_id"]
                    name = contour_dict["name"]
                    to_keep[db_id] = {
                        "db_id": db_id,
                        "name": name
                    }

    override_types = [
        "potential",
        "potential_realigned",
    ]
    # TODO: multithread this
    for type_ in override_types:
        for type_set in section_dict[type_]:
            for contour_dict in type_set:
                keep_bool = contour_dict.get("keepBool", False)
                db_id = contour_dict["db_id"]
                name = contour_dict["name"]
                if not keep_bool:
                    pop_ids.add(db_id)
                else:
                    to_keep[db_id] = {
                        "db_id": db_id,
                        "name": name
                    }

    for id_ in pop_ids:
        to_keep.pop(id_, None)
        exact_ids = get_exact_matches_for_db_id(session, id_)
        for exact_id in exact_ids:
            to_keep.pop(exact_id, None)

    return to_keep.values()


def get_output_contours_from_series_dict(session, series_dict):
    to_keep = []
    for section_number, section_dict in series_dict.items():
        to_keep.extend(
            _get_output_contours_from_section_dict(
                session,
                series_dict[section_number]
            )
        )
    return to_keep


def create_output_series(session, to_keep, series):
    series_copy = deepcopy(series)
    # Wipe section contours
    for section_index, section in series_copy.sections.items():
        section.contours = []

    # TODO: multithread this?
    for keep_dict in to_keep:
        db_id = keep_dict["db_id"]
        db_contour = session.query(Contour).get(db_id)
        section_index = db_contour.section
        contour_index = db_contour.index
        reconstruct_contour = series.sections[section_index].contours[contour_index]
        reconstruct_contour.name = keep_dict["name"]
        series_copy.sections[section_index].contours.append(reconstruct_contour)
    return series_copy
