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
    DATETIME_TIMEZONE: str = "Asia/Shanghai"

    # openssl rand -hex 32
    SECRET_KEY: str = ""
    PREFIX: str = "/api"

    # Database
    DB_URL: str = ""
    DB_NAME: str = ""

    # OSS
    IMAGES_URL: str = ""
    IMAGES_USERNAME: str = ""
    IMAGES_PASSWORD: str = ""

    # init_data
    DATA_URL: str = ""

    DEBUGGER: bool = False
    LOG_LEVEL: int = logging.INFO

    class Config:
        env_file = ".env"


settings = Settings()
