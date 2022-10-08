from os import environ
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings


def get_env_var(key_name: str, data_type: Any, default: Optional[Any] = None):
    value = environ.get(key_name, default)
    if value is None:
        raise KeyError(f"{key_name} not set in environment variables.")
    if data_type is bool:
        if str(value).lower() in ["true", "1"]:
            return True
        elif str(value).lower() in ["false", "0"]:
            return False

    try:
        return data_type(value)

    except Exception:
        return ValueError(
            f"Invalid data type for variable {key_name}, expected {data_type}."
        )


class Settings(BaseSettings):
    app_prefix: str = "/api"
    app_base_url: str = get_env_var("APP_BASE_URL", str)
    database_url = "{dialect}://{user}:{password}@{host}/{database_name}".format(
        dialect="postgresql",
        user=environ["DB_USER"],
        password=environ["DB_PASSWORD"],
        host=environ["DB_HOST"],
        port=environ["DB_PORT"],
        database_name=environ["DB_NAME"],
    )

    data_dir = Path("data")


settings = Settings()
