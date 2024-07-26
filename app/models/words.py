from beanie import Document
from pydantic.fields import Field


class Words(Document):
    name: str = Field(..., description="名称", examples=["Meme"])

    class Settings:
        name = "words"
