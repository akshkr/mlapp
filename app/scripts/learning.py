"""File to store model training and test functions."""

from os import path
from typing import Any, Dict, Tuple
from uuid import UUID

import keras
from keras import layers, models, optimizers
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.image_utils import img_to_array, load_img

from app.config import settings
from app.constants import DATA_GENERATOR_PARAMS, ModelConstants
from app.utils import download_data

filename = path.basename(ModelConstants.PRETRAINED_WEIGHTS.value)


def create_model() -> Any:
    """Create a InceptionV3 model."""
    weights = download_data(filename)
    pre_trained_model = InceptionV3(
        input_shape=ModelConstants.INPUT_IMAGE_SHAPE.value,
        include_top=False,
        weights=None,
    )
    pre_trained_model.load_weights(weights)

    for layer in pre_trained_model.layers:
        layer.trainable = False

    last_layer = pre_trained_model.get_layer("mixed7")
    last_layer_output = last_layer.output

    x = layers.Flatten()(last_layer_output)
    x = layers.Dense(1024, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(2, activation="softmax")(x)

    model = keras.Model(pre_trained_model.input, x)

    model.compile(
        optimizer=optimizers.RMSprop(lr=0.01),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


def train_model(model: Any, train_data_dir: str) -> Tuple[Any, Dict]:
    """Train model and return model and class mapping."""
    train_datagen = ImageDataGenerator(**DATA_GENERATOR_PARAMS)
    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=tuple(ModelConstants.INPUT_IMAGE_SHAPE.value[:2]),
        batch_size=ModelConstants.BATCH_SIZE.value,
        class_mode="categorical",
    )

    model.fit(
        train_generator,
        steps_per_epoch=10,
        epochs=4,
        verbose=1,
    )

    return model, train_generator.class_indices


def evaluate_model(model: Any, test_data_dir: str) -> Dict:
    """Evaluate model and return scores."""
    evaluation_datagen = ImageDataGenerator(**DATA_GENERATOR_PARAMS)
    eval_generator = evaluation_datagen.flow_from_directory(
        test_data_dir,
        target_size=tuple(ModelConstants.INPUT_IMAGE_SHAPE.value[:2]),
        batch_size=ModelConstants.BATCH_SIZE.value,
        class_mode="categorical",
    )

    score = model.evaluate_generator(eval_generator, steps=10)
    return score


def preprocess_img(img_path: str) -> Any:
    """Preprocess image for prediction."""
    img = load_img(
        img_path, target_size=tuple(ModelConstants.INPUT_IMAGE_SHAPE.value[:2])
    )
    img = img_to_array(img)
    img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
    img = img / 255

    return img


def make_prediction(model: Any, img_path: str) -> Any:
    """Make prediction for given image path."""
    img = preprocess_img(img_path)
    return model.predict(img)


def save_model(model: Any, model_id: UUID):
    """Save model to data dir"""
    model.save(path.join(settings.data_dir, str(model_id)))


def load_model(model_id: UUID):
    """Load model."""
    return models.load_model(path.join(settings.data_dir, str(model_id)))
