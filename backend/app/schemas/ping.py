from datetime import datetime, date

from pydantic import BaseModel


class PingResult(BaseModel):
    ping: str
    environment: str
    current_day: date = datetime.now().date()