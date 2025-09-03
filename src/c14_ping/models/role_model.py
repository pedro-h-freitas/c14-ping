from uuid import UUID
from typing import TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from .user_model import User


class Role(BaseModel):
    id: int
    name: str
    users: list["User"]
