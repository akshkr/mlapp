"""Utility functions for database connections."""

from logging import getLogger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from app.config import settings
from app.datamodel.models import Base

logger = getLogger(__name__)

engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)


def setup_db() -> None:
    with sessionmaker(engine)() as session:
        try:
            if not database_exists(settings.database_url):
                logger.info("Creating Database!")
                create_database(settings.database_url)
            session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            session.commit()
        except Exception as e:
            logger.error("Failed to execute the queries", e)
            session.rollback()
            raise e
        finally:
            session.close()

        logger.info("The DB is ready to use.")
        Base.metadata.create_all(bind=engine)
