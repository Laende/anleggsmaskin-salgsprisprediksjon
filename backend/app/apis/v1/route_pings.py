from fastapi import APIRouter, Depends

from app.schemas.ping import PingResult
from app.core.config import get_settings, Settings


router = APIRouter()


@router.get("/ping", response_model=PingResult, name="ping", status_code=200)
async def pong(settings: Settings = Depends(get_settings)) -> PingResult:
    return PingResult(ping="pong!", environment=settings.ENVIRONMENT)