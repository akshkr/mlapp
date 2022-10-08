"""File contains model training and test related APIs."""

import json
from os import path
from uuid import uuid4

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.config import settings
from app.constants import APIConstants, Operations, ResponseMessage
from app.datamodel import crud, models
from app.dependencies import get_db
from app.scripts.db_scripts import get_model_class_map, get_model_id
from app.scripts.learning import (
    create_model,
    evaluate_model,
    load_model,
    make_prediction,
    save_model,
    train_model,
)
from app.utils import unzip_data

model_route = APIRouter()


@model_route.post("/train")
async def train(
    model_version: str,
    file: UploadFile = File(
        alias="training-file",
        title="Training image dataset",
    ),
    db: Session = Depends(get_db),
):
    """Model training api."""
    model_id = uuid4()
    target_zip_filepath = path.join(settings.data_dir, path.basename(file.filename))

    # Upload the file
    try:
        async with aiofiles.open(target_zip_filepath, "wb") as f:
            while chunk := await file.read(APIConstants.UPLOAD_CHUNK_SIZE.value):
                await f.write(chunk)

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Uploading file! {ex}",
        )

    finally:
        await file.close()

    extracted_data_dir = unzip_data(target_zip_filepath)

    # Training
    model = create_model()
    model, class_indices = train_model(model, extracted_data_dir)
    save_model(model, model_id)

    # Save the model and training details in DB
    model_record = crud.get_or_create(
        db,
        models.ImageModel,
        dict(
            image_model_uuid=model_id,
            version=model_version,
            class_map=json.dumps(class_indices),
        ),
        commit=False,
    )
    crud.create(
        db,
        models.Operation,
        dict(name=Operations.TRAIN, model_uuid=model_record.image_model_uuid),
    )

    return {"message": ResponseMessage.TRAINING_SUCCESS.value}


@model_route.post("/evaluate")
async def evaluate(
    model_version: str,
    file: UploadFile = File(
        alias="evaluation-file",
        title="Evaluation image dataset",
    ),
    db: Session = Depends(get_db),
):
    """Evaluate api."""
    model_query = get_model_id(db, model_version)

    if not model_query:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ResponseMessage.MODEL_DOESNT_EXIST.value.format(model_version=model_version),
        )
    model_id = model_query[0]

    target_zip_filepath = path.join(settings.data_dir, path.basename(file.filename))

    # Upload the file
    try:
        async with aiofiles.open(target_zip_filepath, "wb") as f:
            while chunk := await file.read(APIConstants.UPLOAD_CHUNK_SIZE.value):
                await f.write(chunk)

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Uploading file! {ex}",
        )

    finally:
        await file.close()

    extracted_data_dir = unzip_data(target_zip_filepath)

    # Evaluation
    model = load_model(model_id)
    score = evaluate_model(model, extracted_data_dir)

    # Update evaluation statistics
    operation_record = crud.create(
        db,
        models.Operation,
        dict(name=Operations.EVALUATE, model_uuid=model_id),
        commit=False,
    )
    crud.create(
        db,
        models.Evaluate,
        dict(
            data=file.filename,
            output=str(score[1]),
            metrics=str(score[0]),
            operation_uuid=operation_record.operation_uuid,
        ),
    )

    return {"Accuracy": score[1], "Loss": score[0]}


@model_route.post("/predict")
async def predict(
    model_version: str,
    file: UploadFile = File(
        alias="test-file",
        title="Prediction image",
    ),
    db: Session = Depends(get_db),
):
    """Predict api."""
    model_query = get_model_id(db, model_version)
    if not model_query:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=ResponseMessage.MODEL_DOESNT_EXIST.value.format(
                model_version=model_version
            ),
        )
    model_id = model_query[0]
    target_file = path.join(settings.data_dir, path.basename(file.filename))

    # Upload file
    try:
        async with aiofiles.open(target_file, "wb") as f:
            while chunk := await file.read(APIConstants.UPLOAD_CHUNK_SIZE.value):
                await f.write(chunk)

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Uploading file! {ex}",
        )

    finally:
        await file.close()

    # Prediction
    class_indices = get_model_class_map(db, model_id)
    model = load_model(model_id)
    target = make_prediction(model, target_file)
    idx = target[0].argmax()
    predict_dict = {v: k for k, v in json.loads(class_indices).items()}

    # Save the prediction result in DB
    operation_record = crud.create(
        db,
        models.Operation,
        dict(name=Operations.PREDICT, model_uuid=model_id),
        commit=False,
    )
    crud.create(
        db,
        models.Predict,
        dict(
            data=target_file,
            output=str(predict_dict[idx]),
            operation_uuid=operation_record.operation_uuid,
        ),
    )

    return {"Prediction": str(predict_dict[idx])}
