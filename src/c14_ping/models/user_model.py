from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field


if TYPE_CHECKING:
    from .role_model import Role


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    email: str
    password: str
    roles: list["Role"]

    @property
    def role_names(self) -> list[str]:
        return [role.name for role in self.roles]
