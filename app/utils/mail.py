import logging
from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import settings

logger = logging.getLogger(__name__)
mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USER,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
)
mail = FastMail(mail_conf)


async def send_email(
    title: str,
    content: str,
    receivers: List[str],
):
    message = MessageSchema(
        subject=title,
        recipients=receivers,
        body=content,
        subtype=MessageType.html
    )

    await mail.send_message(message)
