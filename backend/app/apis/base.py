from fastapi import APIRouter

from app.apis.v1 import route_pings


api_router = APIRouter()

api_router.include_router(
    router=route_pings.router,
    prefix="",
    tags=["ping"])

