"""Database model and response schemas."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class SchemaBase(BaseModel):
    """Base schema to be inherited by model schemas."""

    class Config:
        orm_mode = True


class ImageModel(SchemaBase):
    """Image model schema."""

    image_model_uuid: UUID

    version: str
    created_at: datetime
    class_map: str

    class Config:
        orm_mode = True


class Operation(SchemaBase):
    """Operation model schema."""

    operation_uuid: UUID

    name: str
    time: datetime
    model_uuid: UUID


class Predict(SchemaBase):
    """Prediction model schema."""

    predict_uuid: UUID

    data: str
    output: str

    operation_uuid: UUID


class Evaluate(SchemaBase):
    """Evaluation model schema."""

    evaluate_uuid: UUID

    data: str
    output: str
    metrics: str

    operation_uuid: UUID


class MetadataResponse(SchemaBase):
    """Response schema for metadata."""

    image_model_uuid: UUID
    version: str
    created_at: datetime


class HistoryResponse(SchemaBase):
    """Response schema for history"""

    name: str
    time: datetime
    model_uuid: UUID
    data: str
    output: Any
