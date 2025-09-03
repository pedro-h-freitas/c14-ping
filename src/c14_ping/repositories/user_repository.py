
from typing import Optional, List
from uuid import UUID

from c14_ping.models.user_model import User


class UserRepository:
    async def create(self, obj: User) -> User:
        pass

    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    async def get_all(self) -> List[User]:
        pass

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    async def update_user(self, user: User) -> User:
        pass

    async def delete(self, obj: User) -> None:
        pass
