import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router

# 创建 FastAPI 应用
def create_app():
    app = FastAPI()

    # 设置日志目录
    log_dir = '/var/logs/'
    log_path = os.path.join(log_dir, 'webapi.log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # 配置日志
    handler = RotatingFileHandler(log_path, maxBytes=10 * 1024 * 1024, backupCount=10)
    handler.setLevel(logging.INFO)  # 设置日志级别
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger("uvicorn.error")  # 使用 uvicorn 的日志
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)  # 设置应用日志级别

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

    return app

# 创建应用
app = create_app()