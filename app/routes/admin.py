import logging
import json
import time
from uuid import uuid4

import requests
from fastapi import APIRouter

from app.config import settings
from app.models.emojis import Emojis
from app.models.memes import Memes
from app.models.words import Words
from app.models.bqb import BQB
from app.schemas.response import Success
from app.utils.auth import get_token

logger = logging.getLogger(__name__)
routes = APIRouter()


@routes.get(
    "/init",
    tags=["Admin"],
    summary="nsfw",
    description="nsfw",
    response_model=Success,
)
async def init():
    with open(settings.BASE_DIR/'words.json') as f:
        data = json.load(f)
    records = []
    for word in data.keys():
        records.append(Words(name=word))
    await Words.insert_many(records)
    return Success()


@routes.post(
    "/upload",
    tags=["Admin"],
    summary="上传",
    description="上传至图床",
    response_model=Success,
)
async def upload(
):
    # records = []
    token = await get_token()
    for _dir in (settings.BASE_DIR/'images').iterdir():
        if _dir.is_file():
            continue
        model = Emojis if _dir.name != 'meme' else Memes
        for _file in _dir.iterdir():
            if _file.name == ".DS_Store":
                continue
            res = requests.post(
                url=f"{settings.IMAGES_URL}/upload",
                headers={
                    'Accept': 'application/json',
                    'Authorization': f"Bearer {token}",
                },
                files={
                    "file": open(_file, 'rb'),
                }
            ).json()
            if not res["status"]:
                # records.append(_file)
                logger.info(_file)
                logger.info(res)
                continue
            record = model(
                key=res["data"]["key"],
                name=_file.name,
                type=_dir.name,
                url=res["data"]["links"]["url"],
                tags=[],
                likes=0,
                dislikes=0,
            )
            await model.insert(record)
            time.sleep(1)
    return Success()


@routes.delete(
    "/delete",
    tags=["Admin"],
    summary="删除",
    description="清理图床",
    response_model=Success,
)
async def delete():
    token = await get_token()
    async for obj in Emojis.all():
        requests.delete(
            url=f"https://images.just4dream.club/api/v1/images/{obj.key}",
            headers={
                'Accept': 'application/json',
                'Authorization': f"Bearer {token}",
            }
        )
        await obj.delete()
        logger.info(f"删除 Emoji {obj.name} 成功")
    async for obj in Memes.all():
        requests.delete(
            url=f"https://images.just4dream.club/api/v1/images/{obj.key}",
            headers={
                'Accept': 'application/json',
                'Authorization': f"Bearer {token}",
            }
        )
        await obj.delete()
        logger.info(f"删除 Memes {obj.name} 成功")
    return Success()


@routes.post(
    "/init_bqb",
    tags=["Admin"],
    summary="上传",
    description="上传至图床",
    response_model=Success,
)
async def init_bqb(
):
    res = requests.get(
        url=settings.DATA_URL
    ).json()
    records = []
    for index, line in enumerate(res["data"]):
        records.append(BQB(
            key=str(uuid4()),
            name=line["name"],
            type=line["category"],
            url=line["url"],
            tags=[],
            likes=0,
            dislikes=0,
        ))
        logger.info(f"已处理第 {index} 个表情包 {line['name']}")
    await BQB.insert_many(records)
    return Success()
