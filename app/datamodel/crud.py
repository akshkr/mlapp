from typing import Any

from sqlalchemy.orm import Session

from app.datamodel import models


def create(
    db: Session,
    model: Any,
    data_dict: Any,
    commit: bool = True,
) -> models.Base:
    db_record = model(**data_dict)
    db.add(db_record)
    db.flush()

    if commit:
        db.commit()
        db.refresh(db_record)

    return db_record


def get_or_create(
    db: Session,
    model: Any,
    data_dict: Any,
    commit: bool = True,
) -> models.Base:

    db_record = db.query(model).filter_by(**data_dict).first()

    if db_record:
        return db_record

    return create(db, model, data_dict, commit)


def get_all(db: Session, model: Any, **filters: Any) -> Any:
    query = db.query(model)
    if filters:
        query = query.filter_by(**filters)

    return query.all()
