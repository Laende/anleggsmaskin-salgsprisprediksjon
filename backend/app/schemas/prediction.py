from pydantic import BaseModel


class SalePricePredictionResult(BaseModel):
    price: int
    currency: str = "USD"
