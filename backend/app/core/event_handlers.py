from logging import getLogger
from typing import Callable

from fastapi import FastAPI

from app.db.session import init_db


log = getLogger("uvicorn")


def _startup_database(app: FastAPI) -> None:
    log.info("Initialising database.")
    init_db(app)


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        log.info("Running app start handler...")
        _startup_database(app)
    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        log.info("Running app shutdown handler.")
    return shutdown