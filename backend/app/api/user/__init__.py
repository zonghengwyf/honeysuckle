from fastapi import APIRouter

from .views import user_router

user_router_v1 = APIRouter()
user_router_v1.include_router(user_router)