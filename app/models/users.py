from beanie import Document
from pydantic.fields import Field


class Users(Document):
    account: str = Field(..., description="账号", examples=["a@b.c"])
    password: str = Field(..., description="密码", examples=["a@b.c"])

    class Settings:
        name = "users"
