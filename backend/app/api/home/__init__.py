from fastapi import APIRouter

from .views import home_router

home_router_v1 = APIRouter()
home_router_v1.include_router(home_router)