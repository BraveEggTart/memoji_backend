import logging

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from redis import Redis

from app.db.redis import get_redis
from app.models.users import Users
from app.schemas.response import Success, Fail
from app.schemas.login import LoginSchema, LoginEmailSchema
from app.schemas.jwt import JWTPayloadSchema, JWTOutSchema
from app.utils.crypto import verify_password
from app.utils.jwt import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)
routes = APIRouter()


@routes.get(
    "/login",
    tags=["General"],
    summary="登陆",
    description="登陆后可以上传表情包",
    response_model=Success[JWTOutSchema],
)
async def login(
    request: Request,
    data: LoginSchema,
    redis_client: Redis = Depends(get_redis),
):
    captcha_key = f"captcha-{request.state.ip}"
    check_code = redis_client.get(captcha_key)

    if check_code is None or check_code != data.captcha:
        return Fail(msg="验证码错误")

    user = await Users.find_one({"account": data.account})
    if user is not None and verify_password(data.password, user.password):
        payload = JWTPayloadSchema(id=user.pk)
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload) if data.remember else ""
        redis_client.delete(captcha_key)
        return Success(
            data=JWTOutSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer ",
            )
        )
    return Fail(msg="用户名或密码错误")


@routes.post(
    "/login_email",
    tags=["General"],
    summary="登陆",
    description="登陆后可以上传表情包",
    response_model=Success[JWTOutSchema],
)
async def login_email(
    data: LoginEmailSchema,
    redis_client: Redis = Depends(get_redis),
):
    captcha_key = f"email-code-{data.email}"
    check_code = redis_client.get(captcha_key)

    if check_code is None or check_code != data.code:
        return Fail(msg="邮箱地址或验证码错误")

    payload = JWTPayloadSchema(id=data.email)
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload) if data.remember else ""
    redis_client.delete(captcha_key)
    return Success(
        data=JWTOutSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer ",
        )
    )
