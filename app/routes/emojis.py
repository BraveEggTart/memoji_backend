import logging

from fastapi import APIRouter

from app.models.emojis import Emojis
from app.schemas.response import Success

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
