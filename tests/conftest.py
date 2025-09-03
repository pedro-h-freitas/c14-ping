from pydantic import BaseModel
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from c14_ping.services import UserService
from tests.constants import USER_SERVICE_PATH


@pytest.fixture
def fake_user():
    user = MagicMock()
    user.id = uuid4()
    user.email = "pedro@example.com"
    user.password = "hashed"
    user.roles = ["user"]
    user.role_names = ["user"]
    return user


@pytest.fixture
def fake_user_update():
    user_update = MagicMock()
    user_update.username = "new"
    user_update.email = None
    user_update.password = None
    user_update.roles = None
    return user_update


@pytest.fixture
def user_repository(fake_user):
    repo = AsyncMock()
    repo.get_by_email.return_value = None
    repo.get_by_id.return_value = fake_user
    repo.create.return_value = fake_user
    repo.update_user.return_value = fake_user
    repo.get_all.return_value = [fake_user]
    return repo


@pytest.fixture
def role_repository():
    repo = AsyncMock()
    repo.get_by_names.return_value = ["user"]
    return repo


@pytest.fixture
def user_service(user_repository, role_repository):
    return UserService(user_repository, role_repository)


class DummyModel(BaseModel):
    field: str


@pytest.fixture
def mock_tokens(mocker):
    mocker.patch(
        f"{USER_SERVICE_PATH}.create_access_token", return_value="access"
    )
    mocker.patch(
        f"{USER_SERVICE_PATH}.create_refresh_token", return_value="refresh"
    )
