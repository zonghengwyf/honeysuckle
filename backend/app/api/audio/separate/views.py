from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import APIRouter

separate_router = APIRouter(prefix="/separate")

@separate_router.route('/task', methods=['POST'])
async def app_separate_task(request: Request):
    return JSONResponse({"data": {}, "message": "OK"})