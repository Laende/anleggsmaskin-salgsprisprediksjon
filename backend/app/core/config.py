from os import getenv
from logging import getLogger
from functools import lru_cache
from typing import Dict, List

from pydantic import AnyUrl, BaseSettings

from app.core.lists import COLUMN_CODES_FEATURES, ALL_FEATURES_LIST, DATETIME_LIST, STATE_LIST

log = getLogger("uvicorn")


class Settings(BaseSettings):
    ### General project settings
    PROJECT_TITLE: str = getenv("PROJECT_TITLE")
    PROJECT_VERSION: str = getenv("PROJECT_VERSION")
    PROJECT_API_PREFIX: str = getenv("PROJECT_API_PREFIX")

    ### Environment and development settings
    ENVIRONMENT: str = getenv("ENVIRONMENT")
    TESTING: bool = getenv("TESTING")

    ### Database settings
    DATABASE_URL: AnyUrl = getenv("DATABASE_URL")
    DATABASE_TEST_URL: AnyUrl = getenv("DATABASE_TEST_URL")

    # Model related stuff
    if ENVIRONMENT == "dev":
        DEFAULT_MODEL_PATH: str = getenv("DEFAULT_TEST_MODEL_PATH")
    else:
        DEFAULT_MODEL_PATH: str = getenv("DEFAULT_MODEL_PATH")
        
    DEFAULT_DATA_PATH: str = getenv("DEFAULT_DATA_PATH")


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


@lru_cache()
def get_feature_codes() -> Dict:
    return COLUMN_CODES_FEATURES


@lru_cache()
def get_features_list() -> List:
    return ALL_FEATURES_LIST


@lru_cache()
def get_datetime_list() -> List:
    return DATETIME_LIST


@lru_cache()
def get_state_list() -> List:
    return STATE_LIST