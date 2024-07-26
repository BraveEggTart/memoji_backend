import logging

from fastapi import APIRouter, FastAPI

from app.routes.health import routes as health_routes
from app.routes.memes import routes as memes_routes
from app.routes.emojis import routes as emojis_routes
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
    prefix="/meme",
    router=memes_routes
)
api_router.include_router(
    prefix="/emoji",
    router=emojis_routes
)
# api_router.include_router(
#     prefix="/admin",
#     router=admin_routes
# )
api_router.include_router(
    router=nsfw_routes
)


def register_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)
