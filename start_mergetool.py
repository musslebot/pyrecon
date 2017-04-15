import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyrecon.tools.reconstruct_reader import process_series_directory
from pyrecon.tools.mergetool import backend


if __name__ == "__main__":
    # Grab desired database location from environment variables -- default to in-memory
    DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite://")

    engine = create_engine(DATABASE_URI, echo=False)
    session = sessionmaker(bind=engine)()

    # Create database tables (if not yet exists)
    if bool(os.getenv("CREATE_DB", 1)):
        backend.create_database(engine)

    # TODO: handle multiple series
    series_path = os.getenv("SERIES_PATH")
    if not series_path:
        raise Exception("Expecting SERIES_PATH environment variable")

    series = process_series_directory(series_path)

    series_matches = {}
    for section in series.sections:
        # Load Section contours into database and determine matches
        db_contours = backend.load_db_contours_from_pyrecon_section(session, section)
        db_contourmatches = backend.load_db_contourmatches_from_db_contours_and_pyrecon_section(
            session, db_contours, section
        )

        # group all matches together by match_type
        grouped = backend.group_section_matches(session, section.index)
        # prepare payload for frontend
        section_matches = backend.prepare_frontend_payload(session, section, grouped)
        series_matches[section.index] = section_matches

    with open("test_dump.json", "w") as f:
        json.dump(series_matches, f)
