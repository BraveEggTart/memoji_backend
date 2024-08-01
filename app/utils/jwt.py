import logging
from datetime import datetime, timedelta
from typing import Dict, Any

import jwt

from app.schemas.jwt import JWTPayloadSchema
from app.config import settings

logger = logging.getLogger(__name__)


def create_access_token(data: JWTPayloadSchema) -> str:
    exp = datetime.now() + timedelta(
        minutes=settings.JWT_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        **data.model_dump(),
        "exp": exp,
    }
    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: JWTPayloadSchema) -> str:
    exp = datetime.now() + timedelta(
        minutes=settings.JWT_TOKEN_EXPIRE_LONG_MINUTES
    )
    payload = {
        **data.model_dump(),
        "exp": exp,
    }
    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decrypt(token: str) -> Dict[str, Any]:
    decode_data = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM]
    )
    return decode_data
