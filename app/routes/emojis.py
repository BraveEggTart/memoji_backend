import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, Query

from app.models.bqb import BQB
from app.models.siteviewer import SiteViewer
from app.schemas.response import Success, SuccessExtra, Fail
from app.utils.nsfw import check_word
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
async def bqb_list(
    name: str = Query(None, description="名称", example="困"),
    page: int = Query(1, description="页码数", example=1),
    size: int = Query(20, description="页面记录数量", example=20),
):
    if name is not None and await check_word(name):
        return Fail(msg="请输入文明用语")
    filter = {} if name is None else {
        "$or": [
            {"name": {"$regex": name}},
            {"type": {"$regex": name}}
        ]
    }

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
    async for record in BQB.find_many(filter, skip=size*(page-1), limit=size):
        result.append({
            "key": record.key,
            "url": record.url,
            "likes": record.likes,
            "dislikes": record.dislikes,
        })
    return SuccessExtra(
        data=result,
        total=30,
        page=page,
        size=size,
        pages=page
    )


@routes.get(
    "/like",
    tags=["BQB"],
    summary="点赞BQB",
    description="点赞BQB",
    response_model=Success,
)
async def bqb_likes(
    key: str = Query(..., description="Key", example="abdcef"),
):
    record = await BQB.find_one({"key": key})
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
async def bqb_dislikes(
    key: str = Query(..., description="Key", example="abdcef"),
):
    record = await BQB.find_one({"key": key})
    if record is None:
        return Fail(msg="投票失败")
    record.dislikes += 1
    await record.save()
    return Success(msg="投票成功")
