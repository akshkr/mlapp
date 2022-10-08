"""Main application runner."""

import os

from fastapi import FastAPI

from app.config import settings
from app.datamodel.database import setup_db
from app.routers.modelling import model_route
from app.routers.status import status_router

app = FastAPI(title="Apple AI", docs_url=settings.app_prefix + "/docs")
setup_db()

# Make directory to dump data
if not os.path.exists(settings.data_dir):
    os.makedirs(settings.data_dir)

app.include_router(model_route)
app.include_router(status_router)
