from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from rt import config


Base = declarative_base()

main_engine = create_engine(
    "{db_type}:///{db_location}".format(
        db_type=config.DB_TYPE, db_location=config.DB_PATH), echo=True)

Session = sessionmaker(bind=main_engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
