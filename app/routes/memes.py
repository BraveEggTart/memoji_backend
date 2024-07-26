import logging

from fastapi import APIRouter

from app.models.memes import Memes
from app.schemas.response import Success

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
