import re
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from fastapi.routing import APIRoute


from app.config import settings
from app.exceptions import register_exceptions
from app.middlewares import make_middlewares
from app.models import __beanie_models__
from app.routes import register_routers

# 设置日志Level
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def custom_generate_unique_id(route: APIRoute) -> str:
    """openapi operationID 命名规则转变
    由接口路由函数名 下划线转大驼峰小驼峰
    """
    operation_id = re.sub(
        '_([a-zA-Z])',
        lambda m: (m.group(1).upper()),
        route.name.lower()
    )
    return operation_id


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    client = AsyncIOMotorClient(str(settings.DB_URL))
    await init_beanie(
        database=getattr(client, settings.DB_NAME),
        document_models=__beanie_models__,
    )
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        openapi_url="/openapi.json",
        middleware=make_middlewares(),
        generate_unique_id_function=custom_generate_unique_id,
        contact={
            "name": "Brave EggTart",
            "url": "https://just4dream.club",
            "email": "braveeggtart@gmail.com",
        },
        license_info={
            "name": "MIT",
            "url": "https://github.com/BraveEggTart/ \
                    memoji_backend/blob/main/LICENSE",
        },
        lifespan=lifespan,
    )

    # register routes
    register_routers(app=app, prefix=settings.PREFIX)

    # register exception handler
    register_exceptions(app=app)

    return app


app = create_app()
