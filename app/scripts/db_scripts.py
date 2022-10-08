"""File to store database operation functions"""

from sqlalchemy.orm import Session

from app.datamodel.models import Evaluate, ImageModel, Operation, Predict


def get_model_id(db: Session, model_version: str):
    """Get image model id."""
    return (
        db.query(ImageModel.image_model_uuid)
        .filter_by(version=model_version)
        .one_or_none()[0]
    )


def get_model_class_map(db: Session, model_uuid: str):
    """Get target to index map for a model."""
    return (
        db.query(ImageModel.class_map).filter_by(image_model_uuid=model_uuid).one()[0]
    )


def get_model_details(db: Session):
    """Get model details."""
    return db.query(
        ImageModel.image_model_uuid, ImageModel.version, ImageModel.created_at
    ).all()


def get_history_records(db: Session):
    """Get details of prediction and evaluation."""
    evaluate_data = (
        db.query(
            Operation.name,
            Operation.time,
            Operation.model_uuid,
            Evaluate.data,
            Evaluate.output,
        )
        .join(Evaluate)
        .all()
    )
    predict_data = (
        db.query(
            Operation.name,
            Operation.time,
            Operation.model_uuid,
            Predict.data,
            Predict.output,
        )
        .join(Predict)
        .all()
    )

    return evaluate_data + predict_data
