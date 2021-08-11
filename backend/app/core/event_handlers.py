from logging import getLogger
from typing import Callable

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.regressor import SalePriceRegressor
from app.db.base import Base
from app.db.session import ENGINE, init_db

log = getLogger("uvicorn")


def _create_tables():
    Base.metadata.create_all(bind=ENGINE)


def _startup_model(app: FastAPI) -> None:
    settings = get_settings()
    model_path = settings.DEFAULT_MODEL_PATH
    log.info("Initialising Regression model.")
    model_instance = SalePriceRegressor(path=model_path)
    app.state.model = model_instance


def _shutdown_model(app: FastAPI) -> None:
    log.info("Shutting down regressor.")
    app.state.model = None


def _startup_database(app: FastAPI) -> None:
    log.info("Initialising database.")
    _create_tables()
    init_db()


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        log.info("Running app start handler...")
        _startup_database(app)
        _startup_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        log.info("Running app shutdown handler.")
        _shutdown_model(app)

    return shutdown
