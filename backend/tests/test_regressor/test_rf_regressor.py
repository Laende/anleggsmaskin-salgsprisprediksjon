from pathlib import Path

import numpy as np

from app.core.config import get_settings
from app.core.regressor import SalePriceRegressor
from app.schemas.prediction import SalePricePredictionResult
from app.schemas.sales import SalesCreate
from tests.data import TEST_IN_DATA, TEST_PREPROCESSED_DATA


def test_is_model_path_valid() -> None:
    settings = get_settings()
    assert Path(settings.DEFAULT_MODEL_PATH).is_file() == True


def test_preprocess_data() -> None:
    settings = get_settings()
    # Create the model
    model = SalePriceRegressor(path=settings.DEFAULT_MODEL_PATH)
    # Create a SalesCreate with test_in_data
    sales_create_data = SalesCreate(**TEST_IN_DATA)
    # get the results from preproccesor
    result = model._pre_process(dict(sales_create_data))
    test_out_data = np.asarray(
        list(map(float, TEST_PREPROCESSED_DATA.values()))
    ).reshape(1, -1)

    # Result from prediction should be of type array (of features)
    assert isinstance(result, np.ndarray)
    # The # of features in the list should be the same as whats expected by the model
    assert len(result) == len(test_out_data)
    # Check if the result matches the expected output data
    assert (result == test_out_data).all()


def test_post_process_data() -> None:
    settings = get_settings()
    model = SalePriceRegressor(path=settings.DEFAULT_MODEL_PATH)

    dummy_data = [100]
    post_processed_data = model._post_process(dummy_data)

    # Result from prediction should be of type array (of features)
    assert isinstance(post_processed_data, type(SalePricePredictionResult(price=100)))
    # The # of features in the list should be the same as whats expected by the model
    assert isinstance(post_processed_data.price, int)
    assert post_processed_data.currency == "USD"
    assert post_processed_data.price == 100
