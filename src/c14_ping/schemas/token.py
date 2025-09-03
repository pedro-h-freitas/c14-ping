
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TokenPayload(BaseModel):
    exp: Optional[datetime] = None
    sub: Optional[str] = None


class AccessTokenPayload(TokenPayload):
    roles: Optional[list[str]] = None


class RefreshTokenPayload(TokenPayload):
    pass


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    msg: Optional[str] = None
