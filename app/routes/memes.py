import logging

import requests
from fastapi import APIRouter

from app.config import settings
from app.models.memes import Memes
from app.schemas.response import Success
from app.utils.auth import get_token

logger = logging.getLogger(__name__)
routes = APIRouter()


@routes.get(
    "/random",
    tags=["Memes"],
    summary="获取随机memes",
    description="获取随机memes",
    response_model=Success,
)
async def meme_random(
):
    meme = await Memes.get_random_one()
    return Success(
        data=meme.url if meme is not None else ""
    )



@routes.post(
    "/upload",
    tags=["Memes"],
    summary="上传memes",
    description="上传memes至图床",
    response_model=Success,
)
async def meme_upload(
):
    token = await get_token()
    records = []
    for _file in (settings.BASE_DIR/'images'/'meme').iterdir():
        res = requests.post(
            url=f"{settings.IMAGES_URL}/upload",
            headers={
                'Accept': 'application/json',
                'Authorization': f"Bearer {token}",
            },
            files={
                "file": open(_file, 'rb'),
            }
        ).json().get("data", {})
        records.append(Memes(
            key=res["key"],
            name=_file.name,
            type="meme",
            url=res["links"]["url"],
            tags=[],
            likes=0,
            dislikes=0,
        ))
    await Memes.insert_many(records)
    return Success()


@routes.delete(
    "/delete",
    tags=["Memes"],
    summary="删除memes",
    description="删除memes",
    response_model=Success,
)
async def meme_delete():
    token = await get_token()
    async for meme in Memes.all():
        requests.delete(
            url=f"https://images.just4dream.club/api/v1/images/{meme.key}",
            headers={
                'Accept': 'application/json',
                'Authorization': f"Bearer {token}",
            }
        )
        await meme.delete()
    return Success()
