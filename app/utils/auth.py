import requests
from async_lru import alru_cache

from app.config import settings


@alru_cache(ttl=7200)
async def get_token():
    res = requests.post(
        url=f"{settings.IMAGES_URL}/tokens",
        params={
            "email": settings.IMAGES_USERNAME,
            "password": settings.IMAGES_PASSWORD,
        }
    )
    return res.json().get("data", {}).get("token")
