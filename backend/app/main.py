import logging

from fastapi import FastAPI

from .core.config import Settings, get_settings
from .core.event_handlers import start_app_handler, stop_app_handler
from .apis.base import api_router


log = logging.getLogger("uvicorn")


def include_routers(app: FastAPI, settings: Settings) -> None:
    app.include_router(api_router, prefix=settings.PROJECT_API_PREFIX)


def get_application() -> FastAPI:
    # Get settings
    settings = get_settings()

    _app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION
        )
    
    # Include routers, see apis/base.py for list of routers
    include_routers(app=_app, settings=settings)

    # Add eventlisteners for application startup and shutdown.
    _app.add_event_handler("startup", start_app_handler(_app))
    _app.add_event_handler("shutdown", stop_app_handler(_app))
    return _app


app = get_application()
