from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi import APIRouter

user_router = APIRouter(prefix="")

@user_router.route('/login', methods=['POST'])
async def app_login(request: Request):
    return JSONResponse({"data": {"id":1, "displayName": "admin", "email": "example@gmail.com",
                         "created_at": "2024-11-23 20:00:20",
                         "updated_at": "2024-11-23 21:00:20"}})