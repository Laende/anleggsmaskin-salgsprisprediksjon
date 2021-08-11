from typing import List
from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from sqlalchemy.orm import Session

from app.apis.v1.route_sales import create_sale
from app.db.models.sales import Sales
from app.db.repository.sales import create_new_sales
from app.schemas.sales import SalesCreate, SalesShow
from app.schemas.prediction import SalePricePredictionResult
from app.core.regressor import SalePriceRegressor
from app.db.session import get_db


router = APIRouter()
log = getLogger("uvicorn")


@router.post("/saleprice", response_model=SalePricePredictionResult, name="predict saleprice", status_code=200)
async def predict_price(request: Request, sale: SalesCreate, db: Session = Depends(get_db)) -> SalePricePredictionResult:
    model: SalePriceRegressor = request.app.state.model
    prediction: SalePricePredictionResult = model.predict(sale)
    sale: SalesShow = create_sale(sale=sale, db=db)
    return prediction