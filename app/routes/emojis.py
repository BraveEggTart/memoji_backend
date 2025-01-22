import logging
from datetime import datetime
# from typing import List

import numpy as np
from fastapi import APIRouter, Query, UploadFile, File
from imagehash import average_hash, ImageHash
from PIL import Image

from app.models.emoji import Emoji
from app.models.siteviewer import SiteViewer
from app.schemas.response import Success, SuccessExtra, Fail
# from app.utils.nsfw import check_word
from app.config import settings

logger = logging.getLogger(__name__)
routes = APIRouter()


@routes.get(
    "/list",
    tags=["BQB"],
    summary="获取BQB",
    description="获取BQB",
    # response_model=Success[List[str]],
)
async def emoji_list(
    name: str = Query(None, description="名称", example="困"),
    page: int = Query(1, description="页码数", example=1),
    size: int = Query(10, description="页面记录数量", example=20),
):
    record_time = datetime.now().strftime(settings.DATE_FORMAT)
    hour = datetime.now().hour
    count_record = await SiteViewer.find_one({
        "record_time": record_time,
        "hour": hour
    })
    if count_record is None:
        await SiteViewer.insert(SiteViewer(
            record_time=record_time,
            hour=hour,
            view=1,
        ))
    else:
        count_record.view += 1
        await count_record.save()

    result = []
    # if name is not None and await check_word(name):
    #     return Fail(msg="请输入文明用语")
    if name in ["", None]:
        filter = {}
        records = [await Emoji.get_random_one() for _ in range(size)]
        total = await Emoji.count()
    else:
        filter = {
            "$or": [
                {"name": {"$regex": name}},
                {"type": {"$regex": name}}
            ]
        }
        records = Emoji.find_many(filter)
        total = await records.count()
        records = await records.find_many(
            skip=size*(page-1),
            limit=size,
        ).to_list()

    pages = total // size + 1
    for record in records:
        if record is None:
            continue
        result.append({
            "key": record.key,
            "url": record.url,
            "likes": record.likes,
            "dislikes": record.dislikes,
        })
    return SuccessExtra(
        data=result,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@routes.get(
    "/like",
    tags=["BQB"],
    summary="点赞BQB",
    description="点赞BQB",
    response_model=Success,
)
async def emoji_likes(
    key: str = Query(..., description="Key", example="abdcef"),
):
    record = await Emoji.find_one({"key": key})
    if record is None:
        return Fail(msg="投票失败")
    record.likes += 1
    await record.save()
    return Success(msg="投票成功")


@routes.get(
    "/dislike",
    tags=["BQB"],
    summary="点踩BQB",
    description="点踩BQB",
    response_model=Success,
)
async def emoji_dislikes(
    key: str = Query(..., description="Key", example="abdcef"),
):
    record = await Emoji.find_one({"key": key})
    if record is None:
        return Fail(msg="投票失败")
    record.dislikes += 1
    await record.save()
    return Success(msg="投票成功")


@routes.post(
    "/similar",
    tags=["BQB"],
    summary="相似图片",
    description="获取相似图片",
    response_model=Success,
)
async def emoji_similar(
    file: UploadFile = File(...),
):
    # 读取文件内容
    file_hash = average_hash(Image.open(file.file))

    result = []
    for emoji in await Emoji.all().to_list():
        image_hash = ImageHash(np.array(emoji.image_hash))
        if (file_hash-image_hash) < 10:
            result.append(emoji.url)

    return Success(data=result)
