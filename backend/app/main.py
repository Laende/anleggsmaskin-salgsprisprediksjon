import logging

from fastapi import FastAPI

from app import __version__

from .apis.base import api_router
from .core.config import Settings, get_settings
from .core.event_handlers import start_app_handler, stop_app_handler

log = logging.getLogger(__name__)


def include_routers(app: FastAPI, settings: Settings) -> None:
    app.include_router(api_router, prefix="")


def get_application() -> FastAPI:
    # Get settings
    settings = get_settings()
    
    _app = FastAPI(title="CMSPP", version="v1")

    # Include routers, see apis/base.py for list of routers
    include_routers(app=_app, settings=settings)

    # Add eventlisteners for application startup and shutdown.
    _app.add_event_handler("startup", start_app_handler(_app))
    _app.add_event_handler("shutdown", stop_app_handler(_app))
    return _app


app = get_application()
