import logging
from datetime import datetime
# from typing import List

import requests
from fastapi import APIRouter, Depends, UploadFile, File
from redis import Redis

from app.db.redis import get_redis
from app.models.siteviewer import SiteViewer
from app.schemas.response import Success, SuccessExtra, Fail
from app.config import settings

logger = logging.getLogger(__name__)
routes = APIRouter()


@routes.post(
    "/word",
    tags=["NSFW"],
    summary="敏感字检查",
    description="敏感字检查",
    response_model=Success,
)
async def check_word(
    name: str,
    redis_client: Redis = Depends(get_redis),
):
    nsfw_word_key = f"word-{name}"
    check_result = redis_client.get(nsfw_word_key)
    if check_result is not None:
        return Success(data=check_result)

    response = requests.post(
        url=f"https://nsfw-production.up.railway.app/check/word?word={name}"
    )
    if response.status_code == 200:
        check_result = response.json().get('data', 'nsfw')
        redis_client.setex(nsfw_word_key, 3600, check_result)
        return Success(data=check_result)
    return Success(data='nsfw')


@routes.post(
    "/image",
    tags=["NSFW"],
    summary="敏感图片检查",
    description="敏感图片检查",
    response_model=Success,
)
async def check_image(
    file: UploadFile = File(...),
):

    # 读取文件内容
    contents = await file.read()

    # 设置要转发的目标接口的 URL
    target_url = "https://vx.link/public/nsfw"

    # 发送文件内容到目标接口
    response = requests.post(target_url, files={"file": (file.filename, contents, file.content_type)})

    if response.status_code == 200:
        check_result = response.json().get('data', {})
        check_result = 'nsfw' if check_result.get('nsfw', 1) >= check_result.get('normal', 0) else 'normal'
        return Success(data=check_result)
    return Success(data='nsfw')
