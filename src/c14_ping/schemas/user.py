from __future__ import annotations
import re
from uuid import UUID
from typing import Optional, Type, List

from pydantic import BaseModel, EmailStr, Field, field_validator

from c14_ping.models import User
from c14_ping.schemas.token import TokenOut


class UserCreate(BaseModel):
    username: str = Field(default=None, min_length=3, max_length=50)
    email: EmailStr = Field(default=None, max_length=100)
    password: str = Field(default=None)
    roles: List[str] = Field(default_factory=lambda: ["user"])


class UserMeUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(default=None, max_length=100)
    password: Optional[str] = Field(default=None)


class UserUpdate(UserMeUpdate):
    roles: Optional[List[str]] = Field(default=None)


class UserMeOut(BaseModel):
    username: str
    email: EmailStr

    @classmethod
    def from_user(cls: Type[UserMeOut], user: User):
        return cls(username=user.username, email=user.email)


class UserOut(UserMeOut):
    id: UUID
    roles: list[str]

    @classmethod
    def from_user(cls: Type[UserOut], user: User):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            roles=user.role_names
        )


class UserMeUpdateResponse(BaseModel):
    user_update: UserMeOut
    token_update: TokenOut


class UsersResponse(BaseModel):
    total: int
    items: list[UserOut]

    @classmethod
    def from_users(cls, users: list[User]):
        return cls(
            total=len(users),
            items=[UserOut.from_user(user) for user in users]
        )
