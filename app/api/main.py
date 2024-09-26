from fastapi import APIRouter

from app.api.v1 import weather

api_router_v1 = APIRouter()
api_router_v1.include_router(weather.router, tags=['weather'])
