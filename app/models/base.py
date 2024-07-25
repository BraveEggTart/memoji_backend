from datetime import datetime
from random import randint
from typing import Optional, List

from beanie import Document, Indexed
from pydantic import AnyUrl
from pydantic.fields import Field


class Base(Document):
    key: Indexed(str, unique=True)  # type: ignore[valid-type]
    name: str = Field(..., description="名称", examples=["Meme"])
    type: str = Field(..., description="类型", examples=["Dog"])
    url: AnyUrl = Field(..., description="访问链接", examples=["https://a.b.c/xx"])
    tags: List[str] = Field([], description="标签", examples=["欢乐"])
    likes: int = Field(0, description="点赞数", examples=[999])
    dislikes: int = Field(0, description="讨厌数", examples=[0])
    created_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    async def get_random_one(cls) -> Optional["Base"]:
        return await cls.find_one(skip=randint(0, await cls.count()-1))

    class Settings:
        name = "base"
