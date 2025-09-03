
from c14_ping.models import Role


class RoleRepository:
    async def get_by_names(self, names: list[str]) -> list[Role]:
        pass
