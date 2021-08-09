import os

import pytest
from fastapi.testclient import TestClient

from app.main import get_application
from app.core.config import get_settings, Settings


def get_settings_override():
    return Settings(TESTING=1, DATABASE_URL=os.getenv("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    
    app = get_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down