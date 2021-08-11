from functools import lru_cache
from logging import getLogger
from os import getenv
from typing import Dict, List

from pydantic import AnyUrl, BaseSettings

from app.core.lists import (ALL_FEATURES_LIST, COLUMN_CODES_FEATURES,
                            DATETIME_LIST, STATE_LIST)


log = getLogger(__name__)


class Settings(BaseSettings):
    PROJECT_API_PREFIX: str = ""
    
    ### Environment and development settings
    ENVIRONMENT: str = getenv("ENVIRONMENT")
    TESTING: bool = getenv("TESTING")

    DATABASE_TEST_URL: AnyUrl = getenv("DATABASE_TEST_URL")

    # Model related stuff
    DEFAULT_MODEL_PATH: str = getenv("DEFAULT_MODEL_PATH")
    DEFAULT_DATA_PATH: str = getenv("DEFAULT_DATA_PATH")

    API_KEY: str = getenv("API_KEY")

    @property
    def DATABASE_URL(self):
        ### Database settings
        url: AnyUrl = getenv("DATABASE_URL")
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

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
