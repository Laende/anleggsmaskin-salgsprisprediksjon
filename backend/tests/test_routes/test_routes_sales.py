import json

import pytest
from app.core.config import get_settings
from app.apis.v1 import route_sales


@pytest.fixture(scope="module")
def create_result() -> dict:
    return {'saleprice': 58000, 'saledate': '2010-12-28', 'product_group': 'wl', 'engine_horsepower_desc': 'variable', 'undercarriage_pad_width': 30.0, 'fi_model_desc': 'hl740tm7a', 'product_group_desc': 'wheel loader', 'hydraulics': '2 valve', 'stick_length': '', 'fi_base_model': 'hl740', 'drive_system': '', 'ripper': '', 'grouser_type': '', 'data_source': 149, 'fi_secondary_desc': 'tm', 'enclosure': 'erops ac', 'blade_type': '', 'differential_type': 'standard', 'auctioneer_id': '27', 'fi_model_series': '7', 'ride_control': '', 'tire_size': 20.5, 'steering_controls': 'conventional', 'year_made': 2008, 'fi_model_descriptor': 'a', 'stick': '', 'coupler': '', 'engine_horsepower': 142.5, 'machine_hours_current_meter': 1455, 'product_size': 'medium', 'transmission': '', 'hydraulics_flow': '', 'is_new': True, 'model_id': 15461, 'state': 'north carolina', 'track_type': ''}

@pytest.fixture(scope="module")
def get_result() -> dict:
    return {'id': 1, 'saleprice': 58000, 'saledate': '2010-12-28', 'product_group': 'wl', 'engine_horsepower_desc': 'variable', 'undercarriage_pad_width': 30.0, 'fi_model_desc': 'hl740tm7a', 'product_group_desc': 'wheel loader', 'hydraulics': '2 valve', 'stick_length': '', 'fi_base_model': 'hl740', 'drive_system': '', 'ripper': '', 'grouser_type': '', 'data_source': 149, 'fi_secondary_desc': 'tm', 'enclosure': 'erops ac', 'blade_type': '', 'differential_type': 'standard', 'auctioneer_id': '27', 'fi_model_series': '7', 'ride_control': '', 'tire_size': 20.5, 'steering_controls': 'conventional', 'year_made': 2008, 'fi_model_descriptor': 'a', 'stick': '', 'coupler': '', 'engine_horsepower': 142.5, 'machine_hours_current_meter': 1455, 'product_size': 'medium', 'transmission': '', 'hydraulics_flow': '', 'is_new': True, 'model_id': 15461, 'state': 'north carolina', 'track_type': ''}


def test_create_sale(client, monkeypatch, input_data, create_result) -> None:

    async def mock_post(sale):
        return 1

    monkeypatch.setattr(route_sales, "create_sale", mock_post)
    response = client.post("/sales/create-sale", data=json.dumps(input_data))
    assert response.status_code == 200
    assert response.json() == create_result


def test_retrieve_sale_by_id(client, monkeypatch, input_data, get_result) -> None:
    
    async def mock_post(sale):
        return 1

    async def mock_get(id):
        return get_result

    monkeypatch.setattr(route_sales, "create_sale", mock_post)
    client.post("/sales/create-sale", data=json.dumps(input_data))
    # Try to retrieve the recently created sale (it will have id of 1)
    monkeypatch.setattr(route_sales, "get_sale", mock_get)
    response = client.get("/sales/get/1")

    assert response.status_code == 200
    assert response.json() == get_result


def test_retrieve_sale_by_non_existing_id(client) -> None:
    # Try to retrieve a sale that doesnt exist
    response = client.get("/sales/get/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Sale with id 1 does not exist."


def test_delete_sale_by_id(client, monkeypatch, input_data) -> None:

    async def mock_post(id):
        return 1
    
    async def mock_delete(id):
        return id

    monkeypatch.setattr(route_sales, "create_sale", mock_post)
    client.post("/sales/create-sale", data=json.dumps(input_data))

    headers = {"token": str(get_settings().API_KEY)}
    monkeypatch.setattr(route_sales, "delete_sale", mock_delete)
    response = client.delete("/sales/delete/1", headers=headers)

    assert response.status_code == 200
    assert response.json() == True


def test_delete_sale_by_non_existing_id(client) -> None:
    headers = {"token": str(get_settings().API_KEY)}
    # Try to delete a sale that doesnt exist (there should be 1 sale in the db with id 1)
    response = client.delete("/sales/delete/1", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Sale with id 1 does not exist."


def test_get_sale_by_new_filter(client, input_data) -> None:
    client.post("/sales/create-sale", data=json.dumps(input_data))

    # Try to retrieve sales filtered by get_new (bool)
    response = client.get("/sales/get-new/True")
    assert response.status_code == 200
    assert response.json()[0] == {
        "saleprice": 58000,
        "model_id": 15461,
        "data_source": 149,
        "auctioneer_id": "27",
        "year_made": 2008,
        "machine_hours_current_meter": 1455,
        "saledate": "2010-12-28",
        "fi_model_desc": "hl740tm7a",
        "fi_base_model": "hl740",
        "fi_secondary_desc": "tm",
        "fi_model_series": "7",
        "fi_model_descriptor": "a",
        "product_size": "medium",
        "state": "north carolina",
        "product_group": "wl",
        "product_group_desc": "wheel loader",
        "drive_system": "",
        "enclosure": "erops ac",
        "ride_control": "",
        "stick": "",
        "transmission": "",
        "engine_horsepower_desc": "variable",
        "hydraulics": "2 valve",
        "ripper": "",
        "tire_size": 20.5,
        "coupler": "",
        "hydraulics_flow": "",
        "track_type": "",
        "undercarriage_pad_width": 30.0,
        "stick_length": "",
        "grouser_type": "",
        "blade_type": "",
        "differential_type": "standard",
        "steering_controls": "conventional",
        "engine_horsepower": 142.5,
        "is_new": True,
    }


def test_get_sale_by_new_filter_doesnt_exist(client) -> None:
    # Try to retrieve sales filtered by get_new (bool)
    response = client.get("/sales/get-new/False")
    assert response.status_code == 404
    message = f"No new sales are added yet, try doing some predictions and try again."
    assert response.json()["detail"] == message
