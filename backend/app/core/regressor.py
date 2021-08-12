from logging import getLogger
from pathlib import Path
from typing import List

import joblib
import numpy as np
import pandas as pd

from app.core.config import (get_feature_codes, get_features_list,
                             get_state_list)
from app.schemas.prediction import SalePricePredictionResult
from app.schemas.sales import SalesCreate

log = getLogger(__name__)

pd.set_option("display.max.rows", None)
pd.set_option("display.max.columns", None)

class SalePriceRegressor(object):
    def __init__(self, path):
        self.path = path
        self.feature_codes = get_feature_codes()
        self.features_list = get_features_list()
        self.state_list = get_state_list()

        if Path(self.path).is_file():
            self._load_local_model()
        else:
            log.error("Model path doesnt exist.")

    def _load_local_model(self):
        self.model = joblib.load(self.path)

    def _pre_process(self, input_data: SalesCreate) -> List:
        # Create a dataframe from the input data, the input data is a dict
        df = pd.DataFrame([input_data])

        # Make sure saledate is of datetime type
        df["saledate"] = pd.to_datetime(df["saledate"], format="%Y-%m-%d")

        # Create new columns based on saledate
        df["saledate_year"] = df["saledate"].dt.year
        df["saledate_month"] = df["saledate"].dt.month
        df["saledate_day"] = df["saledate"].dt.day
        df["saledate_dayofweek"] = df["saledate"].dt.dayofweek
        df["saledate_quarter"] = df["saledate"].dt.quarter

        # Drop saleprice and saledate as it isnt part of the featureset for the model
        if "saleprice" in df.columns:
            df.drop(["saleprice"], axis=1, inplace=True)
        if "saledate" in df.columns:
            df.drop(["saledate"], axis=1, inplace=True)

        # If the dataframe doesnt have all the required features, add them and fill with zero
        for col in self.state_list:
            if col not in df.columns:
                df[col] = 0

        # One-hot encode the state column, this will fill a 1 into the correct in_state column
        if df.at[0, "state"] != "":
            df = pd.get_dummies(df, columns=["state"], prefix=["in_state"])
        else:
            df.drop(["state"], axis=1, inplace=True)

        # All features should be in df now, order them as expected by model
        df = df[self.features_list]

        df["machine_hours_current_meter"] = df["machine_hours_current_meter"].astype("int")
        # Fill string type columns with numbers. Check if string exists in feature dict, if it does return the code.
        for label, content in df.items():
            if pd.api.types.is_string_dtype(content):
                df[label] = df[label].str.lower()
                val = df.at[0, label]
    
                list_of_feature_values = list(self.feature_codes[label].values())
                list_of_feature_codes = list(self.feature_codes[label].keys())
                try:
                    result = list_of_feature_codes[list_of_feature_values.index(val)]
                    df[label] = result
                except ValueError as e:
                    df[label] = 0

        
        df = df.astype(float)
        out = np.array(list(df.to_dict(orient="records")[0].values())).reshape(1, -1)
        return out

    def _post_process(self, prediction: np.ndarray) -> SalePricePredictionResult:
        log.debug("Post-processing prediction.")
        return SalePricePredictionResult(price=prediction[0])

    def _predict(self, features: List) -> np.ndarray:
        log.debug("Predicting.")
        prediction_result = self.model.predict(features)
        return prediction_result

    def predict(self, input_data: SalesCreate):
        if input_data is None:
            raise ValueError(f"{input_data} is not valid.")

        pre_processed_payload = self._pre_process(dict(input_data))
        prediction = self._predict(pre_processed_payload)
        log.info(f"predicted saleprice: {prediction[0]}")
        post_processed_result = self._post_process(prediction)

        return post_processed_result
