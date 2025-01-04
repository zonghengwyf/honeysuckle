
from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi import APIRouter

home_router = APIRouter(prefix="")

@home_router.route('/', methods=['GET'])
async def app_home(request: Request):
    return JSONResponse({"detail": "OK"})