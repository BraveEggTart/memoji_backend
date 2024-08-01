from pydantic import Field, BaseModel


class EmailCodeSchema(BaseModel):
    account: str = Field(
        ...,
        description="账号",
        examples=['a@b.c', ]
    )
    code: str = Field(
        ...,
        description="验证码",
        examples=["123456", ]
    )
