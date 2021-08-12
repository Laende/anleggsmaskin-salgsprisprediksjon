from logging import getLogger

from fastapi import APIRouter
from fastapi.requests import Request

from app.core.regressor import SalePriceRegressor
from app.schemas.prediction import SalePricePredictionResult
from app.schemas.prediction import SalepricePredictionInput
from app.apis.utils.utils import replace_none_with_empty_str

router = APIRouter()
log = getLogger("uvicorn")

@router.post("/saleprice", response_model=SalePricePredictionResult, name="predict saleprice", status_code=200)
def predict_price(request: Request, data: SalepricePredictionInput) -> SalePricePredictionResult:
    data = dict(data)
    data = replace_none_with_empty_str(data)
    model: SalePriceRegressor = request.app.state.model
    prediction: SalePricePredictionResult = model.predict(data)
    return prediction


