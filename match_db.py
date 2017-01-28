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
section = process_section_file("/home/musslebot/Downloads/CLZBJ 6.13.16/CLZBJ_final_elastic_done_v2 export.20")
section_number = 20
# Go through each Contour in the Section and create a DB Contour tuple (row)
for i, cont in enumerate(section.contours):
    session.add(Contour(
        section=section_number,
        index=i
    ))
    session.commit()


# Know we're going to categorize the PyReconstruct Contours by overlap
# and then store a tuple (row) in the DB relation (table).
def create_matches_from_contours(db_contours, section_contours):
    matches = []
    for idx, db_contour_A in enumerate(db_contours):
        contA = section_contours[db_contour_A.index]
        for idy, db_contour_B in enumerate(db_contours):
            contB = section_contours[db_contour_B.index]
            if idx >= idy:  # TODO: verify logic here -- Does this make sense?
                continue
            elif contA.name != contB.name:
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
            if is_potential_duplicate(contA.shape, contB.shape):
                match_type = "potential"
                matches.append(ContourMatch(
                    id1=db_contour_A.id,
                    id2=db_contour_B.id,
                    match_type=match_type
                ))
    return matches


def get_section_contours(section_number):
    """ Return all of the DB Contours that belong in the given section number.
    """
    return session.query(
        Contour
    ).filter(
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


db_contours = get_section_contours(section_number)
section_contours = section.contours
matches = create_matches_from_contours(db_contours, section_contours)
# I set a breakpoint here and start messing around with queries and stuff.
# Eventually I'll write a query that categorizes our ContourMatches by match_type
# and pass that result into a function that combines that with information about
# its corresponding Reconstruct Contour.
import debug
