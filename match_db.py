from sqlalchemy import (Boolean, Column, create_engine, ForeignKey,
    CheckConstraint, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create the in-memory SQLite database
engine = create_engine("sqlite://", echo=True)

# Create a base class that allows us communicate with the DB using Python
# objects
Base = declarative_base()


class Contour(Base):
    """ Contour knows where its corresponding PyReconstruct Contour is
        within a Series, by storing the Section number and index within
        Section.contours
    """
    __tablename__ = "contours"
    id = Column(Integer, primary_key=True)
    series = Column(Integer, nullable=False)
    section = Column(Integer, nullable=False)
    index = Column(Integer, nullable=False)


class ContourMatch(Base):
    """ This relation JOINs two Contours.
    """
    __tablename__ = "matches"
    __table_args__ = (
        # This constraint makes sure we dont duplicate the bidirectional join
        # between two contours: (A, B) & (B, A)
        CheckConstraint("id1 < id2", name="check_oneway"),
    )
    id1 = Column(
        ForeignKey(Contour.id),
        nullable=False,
        primary_key=True
    )
    id2 = Column(
        ForeignKey(Contour.id),
        nullable=False,
        primary_key=True
    )
    match_type = Column(String, nullable=False)

# Create a session and bind it to the DB
session = sessionmaker(bind=engine)()
# The session allows us to query the database.
# Sessions are something very useful to learn if you want
# to dive deeper into DB stuff:
#    http://stackoverflow.com/questions/10521947/what-is-a-database-session
#
#  vvv This link is way more interesting than that link ^^^
#
# If you want to learn more about Relational Theory, i'd start with this page.
# Relational Theory is the basis for Relation Database implementations. I find it
# to be interesting:
#    https://en.wikipedia.org/wiki/Relation_(database)

# Modify the DB with all of our Python shenanigans
Base.metadata.create_all(engine)


from pyrecon.tools.reconstruct_reader import process_section_file
from pyrecon.tools.mergetool import is_contacting, is_exact_duplicate, is_potential_duplicate

# Read Reconstruct file into PyReconstruct
# We're just playing around with a single Section here
section_1 = process_section_file("/home/musslebot/Downloads/FHLTD/FHLTD.91")
section_2 = process_section_file("/home/musslebot/Downloads/FHLTD/FHLTD.91")
section_number = 91
# Go through each Contour in the Section and create a DB Contour tuple (row)
for i, cont in enumerate(section_1.contours):
    session.add(Contour(
        section=section_number,
        series=1,
        index=i
    ))
    session.commit()
for i, cont in enumerate(section_2.contours):
    session.add(Contour(
        section=section_number,
        series=2,
        index=i
    ))
    session.commit()


# Know we're going to categorize the PyReconstruct Contours by overlap
# and then store a tuple (row) in the DB relation (table).
def create_matches_from_contours(db_contours_1, db_contours_2, section_contours_a, section_contours_b):
    matches = []
    for idx, db_contour_A in enumerate(db_contours_1):
        contA = section_contours_a[db_contour_A.index]
        for idy, db_contour_B in enumerate(db_contours_2):
            contB = section_contours_b[db_contour_B.index]
            if contA.name != contB.name:
                continue
            elif contA.shape != contB.shape:
                # TODO: this could be problematic (e.g. polygon vs linestring)
                continue
            elif not is_contacting(contA.shape, contB.shape):
                continue
            elif is_exact_duplicate(contA.shape, contB.shape):
                match_type = "exact"
                matches.append(ContourMatch(
                    id1=db_contour_A.id,
                    id2=db_contour_B.id,
                    match_type=match_type
                ))
            elif is_potential_duplicate(contA.shape, contB.shape):
                match_type = "potential"
                matches.append(ContourMatch(
                    id1=db_contour_A.id,
                    id2=db_contour_B.id,
                    match_type=match_type
                ))
    return matches


def get_section_contours(series_number, section_number):
    """ Return all of the DB Contours that belong in the given section number.
    """
    return session.query(
        Contour
    ).filter(
        Contour.series == series_number,
        Contour.section == section_number
    ).all()


def get_matches():
    """ Just messing around here with queries.
    """
    return session.query(
        ContourMatch.id1,
        ContourMatch.id2,
        ContourMatch.match_type
    ).all()


db_contours_1 = get_section_contours(1, section_number)
db_contours_2 = get_section_contours(2, section_number)
section_contours_a = section_1.contours
section_contours_b = section_2.contours
matches = create_matches_from_contours(
    db_contours_1, db_contours_2,
    section_contours_a, section_contours_b)
# Commit matches to the DB
session.add_all(matches)
session.commit()

from collections import defaultdict
# Here we create an intermediate representation of our DB matches, structured
# in such a way that it will allow us to easily fill in Reconstruct data for our UI
# The data will be structured as follow:
#     {
#         <id of contour in db>: {
#             "exact": <set of matching db contours>
#             "potential": <set of matching db contours>
#         }, ...
#     }
grouped = defaultdict(lambda: defaultdict(set))

db_contour_ids = []
results = session.query(Contour.id).all()
# Results is a list of tuples: [(1), (2), (3), ...]
for res in results:
    db_contour_ids.append(res[0])

for id_ in db_contour_ids:
    matches = session.query(ContourMatch).filter(ContourMatch.id1 == id_).all()
    grouped[id_] = defaultdict(set)
    for m in matches:
        grouped[id_][m.match_type].add(m.id2)

# Fill intermediate representation with Reconstruct data relevant for the UI
# [
#     {
#         'section': 1,
#         'exacts': [[{}, {}], [{}, {}]...],
#         'potentials': [[{}, {}, {}], [{}, {}]...],
#         'uniques': [{}, {}, {}]
#     },
#     ...
# ]

section_matches = {
    'section': 91,
    'exact': [],
    'potential': [],
    'unique': []
}

already_added = []
for contour_A_id, match_dict in grouped.iteritems():
    db_contour_A = session.query(Contour).get(contour_A_id)
    if db_contour_A.series == 1:
        reconstruct_contour_a = section_1.contours[db_contour_A.index]
        image = section_1.images[0]._path + "/{}".format(section_1.images[0].src),
    elif db_contour_A.series == 2:
        reconstruct_contour_a = section_2.contours[db_contour_A.index]
        image = section_2.images[0]._path + "/{}".format(section_2.images[0].src),
    main_contour_data = {
        'name': reconstruct_contour_a.name,
        'points': reconstruct_contour_a.points,
        'image': image,
        'db_id': contour_A_id
    }
    for match_type, matches in match_dict.iteritems():
        match_list = [main_contour_data]
        for match_id in matches:
            already_added.append(match_id)
            db_contour_B = session.query(Contour).get(match_id)
            if db_contour_B.series == 1:
                reconstruct_contour_b = section_1.contours[db_contour_B.index]
                image = section_1.images[0]._path + "/{}".format(section_1.images[0].src),
            elif db_contour_B.series == 2:
                reconstruct_contour_b = section_2.contours[db_contour_B.index]
                image = section_2.images[0]._path + "/{}".format(section_2.images[0].src),
            match_list.append({
                'name': reconstruct_contour_b.name,
                'points': reconstruct_contour_b.points,
                'image': image,
                'db_id': match_id
            })
        section_matches[match_type].append(match_list)
    if not match_dict.values():
        section_matches["unique"].append(main_contour_data)
    already_added.append(contour_A_id)

