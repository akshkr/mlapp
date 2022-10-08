"""Utility functions."""

import zipfile
from os import path

import requests

from app.config import settings
from app.constants import ModelConstants


def download_data(filename: str) -> str:
    """Download given file to data dir"""
    target_file = path.join(settings.data_dir, filename)
    if path.isfile(target_file):
        print("file already exists!")
        return target_file

    file_to_download = requests.get(
        ModelConstants.PRETRAINED_WEIGHTS.value, stream=True
    )

    with open(target_file, "wb") as file:
        for chunk in file_to_download.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    return target_file


def unzip_data(file_path: str) -> str:
    """Unzip given filename to data dir."""
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(settings.data_dir)

    return file_path[:-4]
