import logging

from fastapi import APIRouter, FastAPI, Depends

from app.dependences.ratelimit import rate_limit
from app.routes.health import routes as health_routes
from app.routes.emojis import routes as emojis_routes
from app.routes.captcha import routes as captcha_routes
from app.routes.login import routes as login_routes
from app.routes.admin import routes as admin_routes
from app.routes.nsfw import routes as nsfw_routes

logger = logging.getLogger(__name__)
api_router = APIRouter(
    responses={
        400: {
            "model": str,
            "description": "test description",
        },
        401: {
            "model": str,
            "description": "test description",
        },
        500: {
            "model": str,
            "description": "test description",
        },
    }
)

api_router.include_router(
    router=health_routes,
)
api_router.include_router(
    router=captcha_routes,
    dependencies=[Depends(rate_limit)],
)
api_router.include_router(
    router=login_routes,
    dependencies=[Depends(rate_limit)],
)
api_router.include_router(
    prefix="/emoji",
    router=emojis_routes,
    dependencies=[Depends(rate_limit)],
)
api_router.include_router(
    prefix="/nsfw",
    router=nsfw_routes,
    dependencies=[Depends(rate_limit)],
)

def register_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)
    # app.include_router(admin_routes, prefix=prefix)
