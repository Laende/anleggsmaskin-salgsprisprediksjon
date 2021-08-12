import json

from app.core.config import get_settings


def test_create_sale(client, input_data) -> None:

    response = client.post("/sales/create-sale", data=json.dumps(input_data))
    assert response.status_code == 200
    assert response.json()["model_id"] == input_data["model_id"]
    assert response.json()["saledate"] == input_data["saledate"]
    assert response.json()["engine_horsepower"] == input_data["engine_horsepower"]
    assert response.json()["year_made"] == input_data["year_made"]
    assert response.json()["data_source"] == input_data["data_source"]
    assert response.json()["auctioneer_id"] == input_data["auctioneer_id"]


def test_retrieve_sale_by_id(client, input_data) -> None:
    client.post("/sales/create-sale", data=json.dumps(input_data))

    # Try to retrieve the recently created sale (it will have id of 1)
    response = client.get("/sales/get/1")
    assert response.status_code == 200
    assert response.json()["model_id"] == input_data["model_id"]
    assert response.json()["saledate"] == input_data["saledate"]
    assert response.json()["engine_horsepower"] == input_data["engine_horsepower"]
    assert response.json()["year_made"] == input_data["year_made"]
    assert response.json()["data_source"] == input_data["data_source"]
    assert response.json()["auctioneer_id"] == input_data["auctioneer_id"]


def test_retrieve_sale_by_non_existing_id(client, input_data) -> None:
    # Do a prediction, this will also create a row with given data in DB
    client.post("/sales/create-sale", data=json.dumps(input_data))

    # Try to retrieve a sale that doesnt exist (there should be 1 sale in the db with id 1)
    response = client.get("/sales/get/2")
    assert response.status_code == 404
    assert response.json()["detail"] == "Sale with id 2 does not exist."


def test_delete_sale_by_id(client, input_data) -> None:
    client.post("/sales/create-sale", data=json.dumps(input_data))
    headers = {"token": str(get_settings().API_KEY)}

    # Try to delete the recently created sale (it will have id of 1)
    response = client.delete("/sales/delete/1", headers=headers)
    assert response.status_code == 200
    assert response.json() == True


def test_delete_sale_by_non_existing_id(client, input_data) -> None:
    headers = {"token": str(get_settings().API_KEY)}
    client.post("/sales/create-sale", data=json.dumps(input_data))

    # Try to delete a sale that doesnt exist (there should be 1 sale in the db with id 1)
    response = client.delete("/sales/delete/2", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Sale with id 2 does not exist."


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


def test_get_sale_by_new_filter_doesnt_exist(client, input_data) -> None:
    # Do a prediction, this will also create a row with given data in DB with is_new = False
    client.post("/sales/create-sale", data=json.dumps(input_data))

    # Try to retrieve sales filtered by get_new (bool)
    response = client.get("/sales/get-new/False")
    assert response.status_code == 404
    message = f"No new sales are added yet, try doing some predictions and try again."
    assert response.json()["detail"] == message
