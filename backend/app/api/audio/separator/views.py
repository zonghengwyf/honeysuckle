import os
import uuid
from pathlib import Path
from typing import List

from fastapi import Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from logger import logger
from app.base.db import DbBase, get_db
from app.base.response import BaseResponse
from .models import AudioSeparatorFile, AudioSeparatorTrack, AudioSeparatorTask
from .main import SeparatorCRUD
from app.api.tasks.separators import create_separator_voices
from app.utils.util import write_file
from app.utils.audio_util import get_audio_duration
from config import SeparatorConfig

separator_router = APIRouter()

@separator_router.post("/voices")
async def view_create_separator_voices(file: UploadFile):
    try:
        db = DbBase()
        file_name = f"{uuid.uuid4()}{Path(file.filename).suffix}"
        file_path = os.path.join(SeparatorConfig.UPLOAD_DIR, file_name)
        await write_file(file, file_path)
        file_size = os.path.getsize(file_path)
        if file_size > SeparatorConfig.AUDIO_SIZE_LIMIT:
            if os.path.exists(file_path): os.remove(file_path)
            return BaseResponse(data={}, message=f"创建音频分离任务失败: 文件大小不能超过{SeparatorConfig.AUDIO_SIZE_LIMIT/1024/1024}M",
                                status_code=400)
        duration = get_audio_duration(file_path)
        created_file = db.add(AudioSeparatorFile, {"file_path": file_path,
                                                   "file_name": file.filename,
                                                   "size": file_size,
                                                   "duration": duration
                                                   })
        separator_task = db.add(AudioSeparatorTask, {"audio_file_id": created_file.id})
        task = create_separator_voices.delay(separator_task.id)
        separator_task.celery_id = task.id
        db.update(separator_task)

        return BaseResponse(data={}, message="创建音频分离任务成功")
    except Exception as err:
        logger.exception(err)
        return BaseResponse(data={}, message=f"创建音频分离任务失败: {err}", status_code=500)


@separator_router.get("/voices-list")
async def view_get_separator_voices():
    try:
        state, data = SeparatorCRUD().separator_task_list()
        return BaseResponse(data=data, message="获取分离音频成功")
    except Exception as err:
        logger.exception(err)
        return BaseResponse(data=[], message=f"获取分离音频失败：{err}", status_code=500)


@separator_router.delete("/voices/{task_id}")
async def view_delete_separator_voices(task_id: str):
    try:
        state, data = SeparatorCRUD().delete_separator_voice(task_id)
        if not state:
            return BaseResponse(message=data, status_code=400)
        return BaseResponse(message="删除分离音频成功")
    except Exception as err:
        logger.exception(err)
        return BaseResponse(message=f"删除分离音频失败：{err}", status_code=500)


@separator_router.get("/tracks/{task_id}")
async def view_get_separator_tracks(task_id):
    try:
        state, data = SeparatorCRUD().get_tracks_by_task(task_id)
        return BaseResponse(data=data, message="获取分离音频成功")
    except Exception as err:
        logger.exception(err)
        return BaseResponse(data=[], message=f"获取分离音频失败：{err}", status_code=500)


@separator_router.get("/voices/download/{file_id}")
async def view_voices_download(file_id):
    try:
        file_data = SeparatorCRUD().get_file_by_id(file_id)
        if not file_data:
            return BaseResponse(message=f"索引ID有误", status_code=404)
        file_path = file_data.file_path or ""
        file_name = file_data.file_name
        if not os.path.exists(file_path):
            return BaseResponse(message=f"未找到音频文件", status_code=404)
        _, file_ext = os.path.splitext(file_path)
        return FileResponse(file_path, media_type='audio/mpeg', filename=f"{file_name}{file_ext}")
    except Exception as err:
        logger.exception(err)
        return BaseResponse(message=f"下载分离音频失败：{err}", status_code=500)