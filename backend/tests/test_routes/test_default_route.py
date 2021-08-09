from fastapi import FastAPI


def test_default_route(test_app: FastAPI) -> None:
    response = test_app.get('/')
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found"
        }
