from sqlalchemy import (Boolean, Column, ForeignKey,
    CheckConstraint, Integer, String)
from sqlalchemy.ext.declarative import declarative_base


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
