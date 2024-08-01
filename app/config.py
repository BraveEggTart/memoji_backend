import logging
from pathlib import Path

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Infomation
    TITLE: str = "Memoji Backend"
    DESCRIPTION: str = "Memoji Backend"
    VERSION: str = "0.1.0"

    # CORS
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # project path
    PROJECT_ROOT: Path = Path(__file__).resolve().parent
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # datetime format
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"
    DATETIME_TIMEZONE: str = "Asia/Shanghai"

    # openssl rand -hex 32
    SECRET_KEY: str = ""
    PREFIX: str = "/api"
    RATE_LIMIT_MINUTES: int = 1
    RATE_LIMIT: int = 100

    # Database
    DB_URL: str = ""
    DB_NAME: str = ""

    # REDIS
    REDIS_URL: str = ""
    REDIS_PORT: str = ""
    REDIS_DB: str = ""
    REDIS_PASSWORD: str = ""

    # OSS
    IMAGES_URL: str = ""
    IMAGES_USERNAME: str = ""
    IMAGES_PASSWORD: str = ""

    # init_data
    DATA_URL: str = ""

    # jwt
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_MINUTES: int = 60 * 2
    JWT_TOKEN_EXPIRE_LONG_MINUTES: int = 60 * 24 * 30

    # Mail Config
    MAIL_USER: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 0
    MAIL_SERVER: str = ""

    DEBUGGER: bool = False
    LOG_LEVEL: int = logging.INFO

    class Config:
        env_file = ".env"


settings = Settings()
