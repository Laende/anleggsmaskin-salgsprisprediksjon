import json


def test_make_prediction(client, input_data) -> None:
    response = client.post("/predict/saleprice", data=json.dumps(input_data))
    assert response.status_code == 200
    assert isinstance(response.json()["price"], int)
    assert response.json()["currency"] == "USD"
    assert response.json()["price"] == 62500

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
