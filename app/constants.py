from enum import Enum


class Operations:
    TRAIN = "train"
    EVALUATE = "evaluate"
    PREDICT = "predict"


class ResponseMessage(Enum):
    TRAINING_SUCCESS = "Training Successful"
    MODEL_DOESNT_EXIST = "The model version: {model_version} doesn't exist. Please use an available model version."


class APIConstants(Enum):
    UPLOAD_CHUNK_SIZE = 1024 * 1024


class ModelConstants(Enum):
    INPUT_IMAGE_SHAPE = (150, 150, 3)
    PRETRAINED_WEIGHTS = "https://storage.googleapis.com/mledu-datasets/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5"
    BATCH_SIZE = 40


DATA_GENERATOR_PARAMS = dict(
    rescale=1 / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
)
