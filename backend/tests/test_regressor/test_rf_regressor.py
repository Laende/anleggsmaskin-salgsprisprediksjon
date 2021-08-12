
from pathlib import Path
import numpy as np
import pytest

from app.schemas.prediction import SalePricePredictionResult
from app.schemas.sales import SalesCreate
from tests.data import TEST_IN_DATA, TEST_PREPROCESSED_DATA
from app.core.lists import STATE_LIST, DATETIME_LIST

@pytest.fixture
def state_list():
    return STATE_LIST

@pytest.fixture
def datetime_list():
    return DATETIME_LIST

def test_is_model_path_valid(settings) -> None:
    assert Path(settings.DEFAULT_MODEL_PATH).is_file() == True

def test_add_and_remove_df_columns_when_preprocessing(input_data, state_list, datetime_list, model) -> None:
    result = model._add_and_remove_df_columns(dict(SalesCreate(**input_data)))
    assert len(result.columns) == 92
    assert set(state_list).issubset(result.columns) == True
    assert set(datetime_list).issubset(result.columns) == True
    assert ("saledate" not in result.columns) == True
    assert ("saleprice" not in result.columns) == True

def test_in_state_columns_are_added_to_df(input_data, model) -> None:
    df = model._add_and_remove_df_columns(dict(SalesCreate(**input_data)))
    result = model._fill_state_in_df(df)
    assert (result.filter(like="in_state", axis=1).sum(1).iloc[0]) == 1

@pytest.mark.parametrize("input, output",
    [
        (TEST_IN_DATA[0], TEST_PREPROCESSED_DATA[0]),
        (TEST_IN_DATA[1], TEST_PREPROCESSED_DATA[1]),
        (TEST_IN_DATA[2], TEST_PREPROCESSED_DATA[2]),
        (TEST_IN_DATA[3], TEST_PREPROCESSED_DATA[3]),
        (TEST_IN_DATA[4], TEST_PREPROCESSED_DATA[4])
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

    assert (np.allclose(np.array(result), np.array(test_out_data))) == True


def test_post_process_data(model) -> None:
    dummy_data = [100]
    post_processed_data = model._post_process(dummy_data)

    # Result from prediction should be of type array (of features)
    assert isinstance(post_processed_data, type(SalePricePredictionResult(price=100)))
    # The # of features in the list should be the same as whats expected by the model
    assert isinstance(post_processed_data.price, int)
    assert post_processed_data.currency == "USD"
    assert post_processed_data.price == 100
