from datetime import datetime

from app.apis.v1 import route_pings

def test_ping(client, monkeypatch) -> None:
    test_response = {
        "ping": "pong!",
        "environment": "dev",
        "current_day": datetime.now().date().strftime("%Y-%m-%d"),
    }

    def mock_get():
        return test_response

    monkeypatch.setattr(route_pings, "pong", mock_get)
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == test_response
