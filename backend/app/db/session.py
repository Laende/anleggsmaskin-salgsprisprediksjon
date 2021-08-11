import re
from logging import getLogger
from typing import Generator

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.core.config import get_settings
from app.db.models.sales import Sales

log = getLogger("uvicorn")


def get_db() -> Generator:
    try:
        db = SESSION()
        yield db
    finally:
        db.close()


def init_db() -> None:
    settings = get_settings()
    db = SESSION()
    is_empty = db.query(Sales).first()
    if is_empty is None:

        df = pd.read_csv(
            settings.DEFAULT_DATA_PATH,
            parse_dates=["saledate"],
            sep=",",
            low_memory=False,
        )
        df.drop(["SalesID"], axis=1, inplace=True)
        log.info("Sales table is empty, filling it with dataset.")

        df.to_sql("sales", con=ENGINE, if_exists="append", index=False)


ENGINE: Engine = create_engine(get_settings().DATABASE_URL, pool_pre_ping=True)
SESSION: Session = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
