from fastapi import FastAPI


def test_default_route(client: FastAPI) -> None:
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found"
        }
