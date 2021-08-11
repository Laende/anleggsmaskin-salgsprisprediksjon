from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.sales import Sales
from app.db.repository.sales import (create_new_sales, delete_sales_by_id,
                                     get_sale_by_id, list_sales,
                                     retrieve_sales_by_new)
from app.db.session import get_db
from app.schemas.sales import SalesCreate, SalesShow
from app.core.security import authenticate


router = APIRouter()
log = getLogger(__name__)


@router.post("/create-sale", response_model=SalesShow, name="Create sale", status_code=200)
def create_sale(sale: SalesCreate, db: Session = Depends(get_db)) -> Sales:
    sale: Sales = create_new_sales(sale=sale, db=db)
    return sale


@router.get("/all/{limit}",response_model=List[SalesShow],name="List sales",status_code=200)
def retrieve_sales(limit: int, db: Session = Depends(get_db)):
    sales = list_sales(limit=limit, db=db)
    if not sales:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There are no currently no sales.")
    return sales


@router.get("/get-new/{is_new}",response_model=List[SalesShow],name="List sales by new",status_code=200)
def retrieve_sales_by_new_filter(is_new: bool, db: Session = Depends(get_db)):
    sales = retrieve_sales_by_new(is_new=is_new, db=db)
    if not sales:
        message = f"No new sales are added yet, try doing some predictions and try again."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return sales


@router.get("/get/{id}", name="Get sale by id", status_code=200)
def get_sale(id: int, db: Session = Depends(get_db)):
    sale = get_sale_by_id(id=id, db=db)
    if not sale:
        message = f"Sale with id {id} does not exist."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return sale


@router.delete("/delete/{id}", name="Delete sale by id", status_code=200)
def delete_sale(id: int, authenticated: bool = Depends(authenticate), db: Session = Depends(get_db)):
    if not authenticated:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,detail=f"You are not authorized.",)
    sales = delete_sales_by_id(id=id, db=db)
    if not sales:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Sale with id {id} does not exist.")
    return sales
