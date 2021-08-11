from logging import getLogger

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from sqlalchemy.orm import Session

from app.apis.v1.route_sales import create_sale
from app.core.regressor import SalePriceRegressor
from app.db.session import get_db
from app.schemas.prediction import SalePricePredictionResult
from app.schemas.sales import SalesCreate, SalesShow

router = APIRouter()
log = getLogger("uvicorn")


@router.post(
    "/saleprice",
    response_model=SalePricePredictionResult,
    name="predict saleprice",
    status_code=200,
)
async def predict_price(
    request: Request, sale: SalesCreate, db: Session = Depends(get_db)
) -> SalePricePredictionResult:

    model: SalePriceRegressor = request.app.state.model
    prediction: SalePricePredictionResult = model.predict(sale)
    sale: SalesShow = create_sale(sale=sale, db=db)
    return prediction
