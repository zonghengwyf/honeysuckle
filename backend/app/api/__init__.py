from fastapi import APIRouter

from .audio import audio_router
from .home import home_router_v1
from .user import user_router_v1

api_router = APIRouter()
api_router.include_router(audio_router, prefix="/audio")
api_router.include_router(home_router_v1)
api_router.include_router(user_router_v1, prefix="/user")