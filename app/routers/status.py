"""File contains status related APIs."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schema import HistoryResponse, MetadataResponse
from app.scripts.db_scripts import get_history_records, get_model_details

status_router = APIRouter()


@status_router.get("/metadata", response_model=List[MetadataResponse])
async def get_metadata(
    db: Session = Depends(get_db),
):
    """Get details of all the model versions present."""
    return get_model_details(db)


@status_router.get("/history", response_model=List[HistoryResponse])
async def get_history(
    db: Session = Depends(get_db),
):
    """Get details of all the evaluation and prediction."""
    return get_history_records(db)
