from datetime import datetime

from fastapi import FastAPI


def test_ping(client) -> None:
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {
        "ping": "pong!",
        "environment": "dev",
        "current_day": datetime.now().date().strftime("%Y-%m-%d"),
    }
