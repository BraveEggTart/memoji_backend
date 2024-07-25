import logging

import requests
from fastapi import APIRouter

from app.config import settings
from app.models.emojis import Emojis
from app.schemas.response import Success
from app.utils.auth import get_token

logger = logging.getLogger(__name__)
routes = APIRouter()


@routes.get(
    "/random",
    tags=["Emojis"],
    summary="获取随机Emojis",
    description="获取随机Emojis",
    response_model=Success,
)
async def emoji_random(
):
    meme = await Emojis.get_random_one()
    return Success(
        data=meme.url if meme is not None else ""
    )



@routes.post(
    "/upload",
    tags=["Emojis"],
    summary="上传Emojis",
    description="上传Emojis至图床",
    response_model=Success,
)
async def emoji_upload(
):
    token = await get_token()
    records = []
    for _dir in (settings.BASE_DIR/'images').iterdir():
        if _dir.name not in ["狗狗"]:
            continue
        for _file in _dir.iterdir():
            res = requests.post(
                url=f"{settings.IMAGES_URL}/upload",
                headers={
                    'Accept': 'application/json',
                    'Authorization': f"Bearer {token}",
                },
                files={
                    "file": open(_file, 'rb'),
                }
            )
            if res.status_code != 200:
                print(res.json())
                continue
            res = res.json().get("data", {})
            records.append(Emojis(
                key=res["key"],
                name=_file.name,
                type=_dir.name,
                url=res["links"]["url"],
                tags=[],
                likes=0,
                dislikes=0,
            ))
            logger.info(f"上传成功 {_file.name}")
    await Emojis.insert_many(records)
    return Success()


@routes.delete(
    "/delete",
    tags=["Emojis"],
    summary="删除Emojis",
    description="删除Emojis",
    response_model=Success,
)
async def emoji_delete():
    token = await get_token()
    async for meme in Emojis.all():
        requests.delete(
            url=f"https://images.just4dream.club/api/v1/images/{meme.key}",
            headers={
                'Accept': 'application/json',
                'Authorization': f"Bearer {token}",
            }
        )
        await meme.delete()
    return Success()
