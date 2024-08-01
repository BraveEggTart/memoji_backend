from pydantic import Field, BaseModel


class LoginSchema(BaseModel):
    account: str = Field(
        ...,
        description="账号",
        examples=['a@b.c', ]
    )
    password: str = Field(
        ...,
        description="登陆密码",
        examples=["123456", ]
    )
    captcha: str = Field(
        ...,
        description="验证码",
        examples=["12", ]
    )
    remember: bool = Field(
        False,
        description="自动登录",
        examples=[False]
    )


class LoginEmailSchema(BaseModel):
    email: str = Field(
        ...,
        description="邮箱地址",
        examples=['a@b.c', ]
    )
    code: str = Field(
        ...,
        description="验证码",
        examples=["123456", ]
    )
    remember: bool = Field(
        False,
        description="自动登录",
        examples=[False]
    )
