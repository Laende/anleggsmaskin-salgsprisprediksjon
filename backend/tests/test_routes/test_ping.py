from datetime import datetime

from fastapi import FastAPI


def test_ping(test_app: FastAPI) -> None:
    response = test_app.get("/api/ping")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "ping": "pong!",
        "environment": "dev",
        "current_day": datetime.now().date().strftime('%Y-%m-%d')
        }
