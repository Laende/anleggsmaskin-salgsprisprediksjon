import json

import pytest

from app.schemas.prediction import SalePricePredictionResult
from app.apis.v1 import route_predict

@pytest.fixture(scope="function")
def prediction_result():
    return SalePricePredictionResult(price=62500)


def test_make_prediction(client, input_data, monkeypatch, prediction_result) -> None:

    def mock_post(sale):
        return 1
    
    monkeypatch.setattr(route_predict, "predict_price", mock_post)
    response = client.post("/predict/saleprice", data=json.dumps(input_data))
    assert response.status_code == 200
    assert isinstance(response.json()["price"], int)
    assert response.json() == prediction_result

def test_make_prediction_with_empty_data(client) -> None:
    response = client.post("/predict/saleprice", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "model_id"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "year_made"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "saledate"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "fi_base_model"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "state"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "product_group"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }
