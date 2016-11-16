import json

from sqlalchemy import (Boolean, Column, create_engine, ForeignKey,
    CheckConstraint, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///:memory:", echo=True)

Base = declarative_base()


class Contour(Base):
    __tablename__ = "contours"
    id = Column(Integer, primary_key=True)
    section = Column(Integer, nullable=False)
    index = Column(Integer, nullable=False)


class ContourMatch(Base):
    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint("id1 < id2", name="check_oneway"),
    )
    id1 = Column(ForeignKey(Contour.id), nullable=False, primary_key=True)
    id2 = Column(ForeignKey(Contour.id), nullable=False, primary_key=True)
    match_type = Column(String, nullable=False)


session = sessionmaker(bind=engine)()
Base.metadata.create_all(engine)
from pyrecon.tools.reconstruct_reader import process_section_file
from pyrecon.tools.mergetool import is_contacting, is_exact_duplicate, is_potential_duplicate


section = process_section_file("/home/musslebot/Downloads/CLZBJ 6.13.16/CLZBJ_final_elastic_done_v2 export.20")
section_number = 20
for i, cont in enumerate(section.contours):
    session.add(Contour(
        section=section_number,
        index=i
    ))
    session.commit()


def create_matches_from_contours(db_contours, section_contours):
    matches = []
    for idx, db_contour_A in enumerate(db_contours):
        contA = section_contours[db_contour_A.index]
        for idy, db_contour_B in enumerate(db_contours):
            contB = section_contours[db_contour_B.index]
            if idx >= idy:  # TODO: logic check
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
                matches.append(ContourMatch(id1=db_contour_A.id, id2=db_contour_B.id, match_type=match_type))
            if is_potential_duplicate(contA.shape, contB.shape):
                match_type = "potential"
                matches.append(ContourMatch(id1=db_contour_A.id, id2=db_contour_B.id, match_type=match_type))
    return matches


def get_section_contours(section_number):
    return session.query(
        Contour
    ).filter(
        Contour.section == section_number
    ).all()


def get_matches():
    return session.query(
        ContourMatch.id1,
        ContourMatch.id2,
        ContourMatch.match_type
    ).all()

db_contours = get_section_contours(section_number)
section_contours = section.contours
matches = create_matches_from_contours(db_contours, section_contours)
import debug
