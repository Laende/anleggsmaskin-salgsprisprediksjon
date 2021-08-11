from logging import getLogger

from sqlalchemy.orm import Session

from app.db.models.sales import Sales
from app.schemas.sales import SalesCreate

log = getLogger("uvicorn")


def create_new_sales(sale: SalesCreate, db: Session):
    log.info("Creating new sales")
    sale = Sales(**sale.__dict__)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale


def retrieve_sales_by_new(is_new: bool, db: Session):
    sales = db.query(Sales).filter(Sales.is_new == is_new).all()
    return sales


def list_sales(limit: int, db: Session):
    MAX_LIMIT = 100
    if limit >= MAX_LIMIT:
        limit = 100
    sales = db.query(Sales).limit(limit).all()
    return sales


def delete_sales_by_id(id: int, db: Session):
    sales_to_delete = db.query(Sales).filter(Sales.id == id)
    if not sales_to_delete.first():
        return False
    sales_to_delete.delete(synchronize_session=False)
    db.commit()
    return True


def get_sale_by_id(id: int, db: Session):
    sale = db.query(Sales).filter(Sales.id == id).first()
    return sale
