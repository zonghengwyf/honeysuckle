import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from logger import logger
from app.api import api_router
from app.base.db import init_db
from app.data.init_data import init_directory

# 创建 FastAPI 应用
def create_app():
    app = FastAPI()

    # 初始化数据库
    init_db()

    # 注册中间件
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    # 注册路由
    app.include_router(api_router, prefix="/v1/honeysuckle")

    # 捕获全局异常
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Request exception: {exc}")
        if isinstance(exc, HTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"detail": "服务器内部错误"}
            )

    @app.on_event("startup")
    async def startup_event():
        init_directory()

    return app

# 创建应用
app = create_app()