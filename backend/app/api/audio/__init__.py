from fastapi import APIRouter

from .separate.views import separate_router

audio_router = APIRouter()
audio_router.include_router(separate_router, prefix="/separate")
