from os import environ

import uvicorn


def load_env_variables() -> None:
    environ["APP_BASE_URL"] = "http://localhost:8000"
    environ["DB_USER"] = "postgres"
    environ["DB_PASSWORD"] = "12345678"
    environ["DB_HOST"] = "localhost"
    environ["DB_PORT"] = "5432"
    environ["DB_NAME"] = "mlapp"


if __name__ == "__main__":
    load_env_variables()

    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        debug=True,
    )
