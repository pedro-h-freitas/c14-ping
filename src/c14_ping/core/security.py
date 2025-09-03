from datetime import timedelta
from typing import Any, List

from c14_ping.schemas import RefreshTokenPayload


def create_access_token(
    subject: str | Any,
    roles: List[str] | Any,
    expires_delta: timedelta
) -> str:
    pass


def create_refresh_token(
    subject: str | Any,
    expires_delta: timedelta
) -> str:
    pass


def decode_refresh_token(token: str) -> RefreshTokenPayload:
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass


def get_password_hash(password: str) -> str:
    pass
