import logging
import json
import time
from uuid import uuid4

import requests
from PIL import Image
from imagehash import average_hash
from fastapi import APIRouter

from app.config import settings
from app.models.emoji import Emoji
from app.schemas.response import Success
from app.utils.upload import upload_image_to_s3

logger = logging.getLogger(__name__)
routes = APIRouter()

@routes.post(
    "/refresh_bqb",
    tags=["Admin"],
    summary="更新表情包",
    description="更新表情包",
    response_model=Success,
)
async def refresh_bqb(
    token: str,
):
    if token != settings.SECRET_KEY:
        return Success
    types = []
    count = 0
    for _dir in (settings.BASE_DIR/'images').iterdir():
        if _dir.is_file():
            continue
        logger.info(f"当前位于文件夹 {_dir.name}")
        for _file in _dir.iterdir():
            if _file.suffix not in ['.gif', ".jpg", ".png", ".jpeg", ".JPG", ".GIF", ".webp"]:
                continue
            logger.info(f"上传表情包 {_file.name}")
            object_name = upload_image_to_s3(str(_file), "memoji")
            record = Emoji(
                key=str(uuid4()),
                name=_file.name,
                type=_dir.name,
                image_hash=average_hash(Image.open(str(_file))).hash.tolist(),
                url=f"https://oss.just4dream.club/memoji/{object_name}",
                tags=[],
                likes=0,
                dislikes=0,
            )
            await Emoji.insert(record)
            count += 1
            logger.info(f"当前已处理 {count} 个图片")
    print(types)
    return Success()
