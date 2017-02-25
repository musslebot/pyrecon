import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyrecon.tools.reconstruct_reader import process_section_file
from pyrecon.tools.mergetool import backend


if __name__ == "__main__":
    # Grab desired database location from environment variables -- default to in-memory
    DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite://")

    engine = create_engine(DATABASE_URI, echo=True)
    session = sessionmaker(bind=engine)()

    # Create database tables (if not yet exists)
    if bool(os.getenv("CREATE_DB", 1)):
        backend.create_database(engine)

    # TODO: handle multiple sections
    section_path = os.getenv("SECTION_PATH")
    if not section_path:
        raise Exception("Expecting SECTION_PATH environment variable")

    section = process_section_file(section_path)

    db_contours = backend.load_db_contours_from_pyrecon_section(session, section)
    db_contourmatches = backend.load_db_contourmatches_from_db_contours_and_pyrecon_section(
        session, db_contours, section
    )
    # TODO: db_contourmatches not working as expected
    import pdb; pdb.set_trace()
