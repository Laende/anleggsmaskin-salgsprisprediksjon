from typing import List
from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from sqlalchemy.orm import Session

from app.db.models.sales import Sales
from app.db.repository.sales import create_new_sales, list_sales, retrieve_sales_by_new, delete_sales_by_id, get_sale_by_id
from app.schemas.sales import SalesCreate, SalesShow
from app.schemas.prediction import SalePricePredictionResult
from app.core.regressor import SalePriceRegressor
from app.db.session import get_db


router = APIRouter()
log = getLogger("uvicorn")


@router.post("/create-sale", response_model=SalesShow, name="Create sale", status_code=200)
async def create_sale(sale: SalesCreate, db: Session = Depends(get_db)) -> Sales:
    sale: Sales = create_new_sales(sale=sale, db=db)
    return sale


@router.get("/all/{limit}/{order_by}", response_model=List[SalesShow], name="List sales", status_code=200)
async def retrieve_sales(limit: int, order_by: str = "saledate", db: Session = Depends(get_db)):
    MAX_LIMIT = 100
    if limit >= MAX_LIMIT:
        limit = 100
    sales = list_sales(limit=limit, order_by=order_by, db=db)
    if not sales:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sales ordered by {order_by} do not exist")
    return sales


@router.get("/get-new/{is_new}", response_model=List[SalesShow], name="List sales by new", status_code=200)
async def retrieve_sales_by_new_filter(is_new: bool, db: Session = Depends(get_db)):
    sales = retrieve_sales_by_new(is_new=is_new, db=db)
    if not sales:
        message = f"No new sales are added yet, try doing some predictions and try again."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return sales


@router.get("/get/{id}", name="Get sale by id", status_code=200)
async def get_sale(id: int, db: Session = Depends(get_db)):
    sale = get_sale_by_id(id=id, db=db)
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale with id {id} does not exist.")
    return sale


@router.delete("/delete/{id}", name="Delete sale by id", status_code=200)
async def delete_sale(id: int, db: Session = Depends(get_db)):
    sales = delete_sales_by_id(id=id, db=db)
    if not sales:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sale with id {id} does not exist.")
    return sales

