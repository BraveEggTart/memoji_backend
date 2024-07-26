import logging

from fastapi import APIRouter

from app.schemas.response import Success
from app.utils.nsfw import check_word

logger = logging.getLogger(__name__)
routes = APIRouter()


@routes.get(
    "/check"
)
async def check(
    word: str
):
    return Success(data= await check_word(word))
