import logging
from typing import List

from fastapi import APIRouter, Query

from app.models.memes import Memes
from app.schemas.response import Success, SuccessExtra

logger = logging.getLogger(__name__)
routes = APIRouter()


@routes.get(
    "/random",
    tags=["Memes"],
    summary="获取随机Memes",
    description="获取随机Memes",
    response_model=Success,
)
async def meme_random(
):
    meme = await Memes.get_random_one()
    return Success(
        data=meme.url if meme is not None else ""
    )


@routes.get(
    "/list",
    tags=["Memes"],
    summary="获取Memes",
    description="获取Memes",
    response_model=Success[List[str]],
)
async def meme_list(
    name: str = Query(None, description="名称", example="安排"),
    type: str = Query(None, description="类型", example="小恐龙"),
    tag: List[str] = Query([], description="标签", example=["猫猫"]),
    size: int = Query(20, description="页面记录数量", example=20),
    page: int = Query(1, description="页码数", example=1),
):
    result = []
    async for record in Memes.find_many({
    }, skip=size*(page-1), limit=size):
        result.append(record.url)
    return SuccessExtra(
        data=result,
        total=30,
        page=page,
        size=size,
        pages=page
    )
