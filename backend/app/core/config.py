import os
import logging
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    ### General project settings
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")
    PROJECT_API_PREFIX: str = os.getenv("PROJECT_API_PREFIX")

    ### Environment and development settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")
    TESTING: bool = os.getenv("TESTING")

    ### Database settings
    DATABASE_URL: AnyUrl = os.getenv("DATABASE_URL")
    DATABASE_TEST_URL: AnyUrl = os.getenv("DATABASE_TEST_URL")

    # Model related stuff
    DEFAULT_MODEL_PATH: str = os.getenv("DEFAULT_MODEL_PATH")


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
