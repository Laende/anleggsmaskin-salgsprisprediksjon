from pathlib import Path

import numpy as np
import pytest

from app.schemas.prediction import SalePricePredictionResult
from app.schemas.sales import SalesCreate
from tests.data import TEST_IN_DATA, TEST_PREPROCESSED_DATA



def test_is_model_path_valid(settings) -> None:
    assert Path(settings.DEFAULT_MODEL_PATH).is_file() == True

@pytest.mark.parametrize("input, output",
    [
        (TEST_IN_DATA[0], TEST_PREPROCESSED_DATA[0]),
        (TEST_IN_DATA[1], TEST_PREPROCESSED_DATA[1]),
        (TEST_IN_DATA[2], TEST_PREPROCESSED_DATA[2]),
        (TEST_IN_DATA[3], TEST_PREPROCESSED_DATA[3]),
        (TEST_IN_DATA[4], TEST_PREPROCESSED_DATA[4]),
        (TEST_IN_DATA[5], TEST_PREPROCESSED_DATA[5])
        ]
    )
def test_preprocess_data(input, output, model) -> None:
    # get the results from preproccesor
    result = model._pre_process(dict(SalesCreate(**input)))
    test_out_data = np.asarray(list(map(float, output.values()))).reshape(1, -1)

    # Result from prediction should be of type array (of features)
    assert isinstance(result, np.ndarray)
    # The # of features in the list should be the same as whats expected by the model
    assert len(result) == len(test_out_data)
    # Check if the result matches the expected output data
    assert (result == test_out_data).all()


def test_post_process_data(model) -> None:
    dummy_data = [100]
    post_processed_data = model._post_process(dummy_data)

    # Result from prediction should be of type array (of features)
    assert isinstance(post_processed_data, type(SalePricePredictionResult(price=100)))
    # The # of features in the list should be the same as whats expected by the model
    assert isinstance(post_processed_data.price, int)
    assert post_processed_data.currency == "USD"
    assert post_processed_data.price == 100
