from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, ForeignKey, MetaData, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base: Any = declarative_base(metadata=metadata)


class ImageModel(Base):
    """Database table for model versions."""

    __tablename__ = "image_model"

    image_model_uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    version = Column(String, nullable=False, unique=True)
    class_map = Column(String, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.timezone("UTC", func.current_timestamp()),
        nullable=False,
    )


class Operation(Base):

    __tablename__ = "operation"

    operation_uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    name = Column(String, nullable=False)
    time = Column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.timezone("UTC", func.current_timestamp()),
        nullable=False,
    )
    model_uuid = Column(
        UUID(as_uuid=True), ForeignKey("image_model.image_model_uuid"), nullable=False
    )


class Predict(Base):

    __tablename__ = "predict"

    predict_uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    data = Column(String)
    output = Column(String, nullable=False)

    operation_uuid = Column(
        UUID(as_uuid=True), ForeignKey("operation.operation_uuid"), nullable=False
    )


class Evaluate(Base):

    __tablename__ = "evaluate"

    evaluate_uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    data = Column(String)
    output = Column(String, nullable=False)
    metrics = Column(String)

    operation_uuid = Column(
        UUID(as_uuid=True), ForeignKey("operation.operation_uuid"), nullable=False
    )
