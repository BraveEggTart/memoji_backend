from typing import List

from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from .logger import LoggerMiddleware
from app.config import settings


def make_middlewares() -> List[Middleware]:
    """
    :param: None
    :return: List[Middleware]
    """
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS
        ),
        Middleware(LoggerMiddleware),
    ]
