from datetime import date, datetime

from pydantic import BaseModel


class PingResult(BaseModel):
    ping: str
    environment: str
    current_day: date = datetime.now().date()
