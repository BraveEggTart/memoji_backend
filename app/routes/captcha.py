import io
import base64
import logging
from random import choice, randint, choices
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from PIL import Image, ImageDraw, ImageFont
from redis import Redis

from app.db.redis import get_redis
from app.schemas.response import Success, Fail
from app.schemas.captcha import EmailCodeSchema
from app.utils.mail import send_email

logger = logging.getLogger(__name__)
routes = APIRouter()


# 生成图片验证码
@routes.get(
    "/captcha",
    tags=["General"],
    summary="获取验证码",
    description="用于获取验证码",
    response_model=Success[str],
)
async def captcha(
    request: Request,
    redis_client: Redis = Depends(get_redis)
):
    width = 120
    height = 30
    char_length = 6
    font_size = 28
    captcha_key = f"captcha-{request.state.ip}"
    font_file = 'monaco.ttf'
    letters = "0123456789"
    options = "+-"
    code = f"{choice(letters)} {choice(options)} {choice(letters)} = "

    image = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image, mode='RGB')

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i, char in enumerate(code):
        h = randint(0, 4)
        draw.text(
            (i * width / char_length, h),
            char,
            font=font,
            fill=(randint(0, 255), randint(10, 255), randint(64, 255))
        )

    # 将图片保存为字节流
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()

    encoded_image = base64.b64encode(img_byte_array)
    result = encoded_image.decode('utf-8')

    answer = eval(code.replace(" ", "").replace("=", ""))
    redis_client.setex(captcha_key, 300, answer)

    return Success(data=result)


# 验证图片验证码
@routes.get(
    "/validate_captcha/{code}",
    tags=["General"],
    summary="验证验证码",
    description="用于验证验证码",
    response_model=Success[Union[bool, str]],
)
async def validate_captcha(
    request: Request,
    code: str,
    redis_client: Redis = Depends(get_redis)
):
    captcha_key = f"captcha-{request.state.ip}"
    check_code = redis_client.get(captcha_key)
    if check_code is None:
        return Fail(data="操作超时, 请刷新页面后重试")
    elif check_code == code:
        redis_client.delete(captcha_key)
        return Success(data=True)
    else:
        return Fail(data="验证码错误")


# 生成随机验证码
@routes.get(
    "/email_code/{email}",
    tags=["General"],
    summary="获取邮箱验证码",
    description="用于获取邮箱验证码",
    response_model=Success[str],
)
async def email_code(
    email: str,
    redis_client: Redis = Depends(get_redis)
):
    captcha_key = f"email-code-{email}"
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    code = ''.join(choices(letters, k=6))
    title = "Welcome to Memoji"
    body = f"""
    <html>
        <body>
        欢迎登陆Memoji，您的验证码为： {code}，有效期30分钟
        </body>
    </html>
    """
    await send_email(title, body, receivers=[email])
    redis_client.setex(captcha_key, 1800, code)
    return Success


# 验证图片验证码
@routes.post(
    "/validate_code",
    tags=["General"],
    summary="验证验证码",
    description="用于验证验证码",
    response_model=Success[Union[bool, str]],
)
async def validate_code(
    data: EmailCodeSchema,
    redis_client: Redis = Depends(get_redis)
):
    captcha_key = f"email-code-{data.account}"
    check_code = redis_client.get(captcha_key)
    if check_code is None:
        return Fail(data="操作超时, 请刷新页面后重试")
    elif check_code == data.code:
        redis_client.delete(captcha_key)
        return Success(data=True)
    else:
        return Fail(data="验证码错误")
