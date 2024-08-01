import hashlib
import logging

logger = logging.getLogger(__name__)


def hash_password(plain_text: str):
    hash_object = hashlib.sha256(plain_text.encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex


def verify_password(
    plain_password: str,
    admin_password: str
) -> bool:
    return admin_password == hash_password(plain_password)
