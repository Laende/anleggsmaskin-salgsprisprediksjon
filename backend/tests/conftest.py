import sys
import os
import pytest
from typing import Any
from typing import Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from app.db.base import Base
from app.db.session import get_db
from app.apis.base import api_router
from app.core.config import Settings
from app.core.regressor import SalePriceRegressor

def get_settings_override():
    return Settings(TESTING=1, DATABASE_URL=os.getenv("DATABASE_TEST_URL"))


def start_application():
    settings = get_settings_override()
    app = FastAPI()
    app.include_router(api_router, prefix=settings.PROJECT_API_PREFIX)
    
    model_path = settings.DEFAULT_MODEL_PATH
    model_instance = SalePriceRegressor(path=model_path)
    app.state.model = model_instance
    return app


settings = get_settings_override()
engine = create_engine(settings.DATABASE_URL)
SessionTesting = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
    )


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)
    # tear down


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client