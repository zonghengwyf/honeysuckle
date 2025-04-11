from fastapi import APIRouter

from .separator.views import separator_router

audio_router = APIRouter()
audio_router.include_router(separator_router, prefix="/separator")
