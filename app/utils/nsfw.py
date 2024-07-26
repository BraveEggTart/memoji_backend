from async_lru import alru_cache

from app.models.words import Words


@alru_cache(maxsize=128)
async def check_word(name: str):
    return False if await Words.find_one({"name": name}) is None else True
