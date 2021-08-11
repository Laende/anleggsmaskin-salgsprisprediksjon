from fastapi import APIRouter

from app.apis.v1 import route_pings, route_predict, route_sales

api_router = APIRouter()


api_router.include_router(
    router=route_pings.router,
    prefix="",
    tags=["ping"])

api_router.include_router(
    router=route_sales.router,
    prefix="/sales",
    tags=["sales"])


api_router.include_router(
    router=route_predict.router,
    prefix="/predict",
    tags=["predict"]
)
