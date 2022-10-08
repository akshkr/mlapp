from typing import Generator

from sqlalchemy.orm import Session

from app.datamodel.database import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
