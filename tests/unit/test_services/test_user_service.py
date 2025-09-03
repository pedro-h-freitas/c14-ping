from jwt import InvalidTokenError
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from c14_ping.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsException,
    OneOrMoreRolesAreInvalid,
    UserNotFound
)

from tests.constants import USER_SERVICE_PATH
from tests.conftest import DummyModel


# -------------------------
# LOGIN
# -------------------------

@pytest.mark.asyncio
async def test_login_success(user_service, user_repository, fake_user, mock_tokens, mocker):
    user_repository.get_by_email.return_value = fake_user
    mocker.patch(f"{USER_SERVICE_PATH}.verify_password", return_value=True)

    token = await user_service.login("pedro@example.com", "123")
    assert token.access_token == "access"
    assert token.refresh_token == "refresh"


@pytest.mark.asyncio
async def test_login_invalid_user(user_service, user_repository):
    user_repository.get_by_email.return_value = None
    with pytest.raises(InvalidCredentialsException):
        await user_service.login("pedro@example.com", "wrong")


@pytest.mark.asyncio
async def test_login_wrong_password(user_service, user_repository, fake_user):
    user_repository.get_by_email.return_value = fake_user

    with patch(f"{USER_SERVICE_PATH}.verify_password", return_value=False):
        with pytest.raises(InvalidCredentialsException):
            await user_service.login("pedro@example.com", "wrong")


# -------------------------
# REFRESH TOKEN
# -------------------------

@pytest.mark.asyncio
async def test_refresh_token_success(user_service, user_repository, fake_user):
    user_repository.get_by_email.return_value = fake_user

    with patch(f"{USER_SERVICE_PATH}.decode_refresh_token", return_value=MagicMock(sub=fake_user.email)), \
            patch(f"{USER_SERVICE_PATH}.create_access_token", return_value="access"), \
            patch(f"{USER_SERVICE_PATH}.create_refresh_token", return_value="refresh"):
        token = await user_service.refresh_token("valid")
        assert token.access_token == "access"


@pytest.mark.asyncio
async def test_refresh_token_invalid_token_error(user_service):
    with patch(f"{USER_SERVICE_PATH}.decode_refresh_token", side_effect=InvalidTokenError()):
        with pytest.raises(InvalidCredentialsException):
            await user_service.refresh_token("bad")


@pytest.mark.asyncio
async def test_refresh_token_validation_error(user_service):
    def fake_decode(token: str):
        DummyModel.model_validate({})

    with patch(f"{USER_SERVICE_PATH}.decode_refresh_token", side_effect=fake_decode):
        with pytest.raises(InvalidCredentialsException):
            await user_service.refresh_token("bad")


@pytest.mark.asyncio
async def test_refresh_token_user_not_found(user_service, user_repository):
    user_repository.get_by_email.return_value = None
    with patch(f"{USER_SERVICE_PATH}.decode_refresh_token", return_value=MagicMock(sub="pedro@example.com")):
        with pytest.raises(InvalidCredentialsException):
            await user_service.refresh_token("valid")


# -------------------------
# GET USERS / GET ME
# -------------------------

@pytest.mark.asyncio
async def test_get_all_users(user_service):
    with patch(f"{USER_SERVICE_PATH}.UsersResponse.from_users", return_value="mocked_response"):
        result = await user_service.get_all_users()

    assert result == "mocked_response"


def test_get_user_me(user_service, fake_user):
    with patch(f"{USER_SERVICE_PATH}.UserMeOut.from_user", return_value="me"):
        assert user_service.get_user_me(fake_user) == "me"


# -------------------------
# CREATE USER
# -------------------------

@pytest.mark.asyncio
async def test_create_user_success(user_service, user_repository, fake_user):
    user_repository.get_by_email.return_value = None

    with patch(f"{USER_SERVICE_PATH}.get_password_hash", return_value="hashed"), \
            patch(f"{USER_SERVICE_PATH}.UserOut.from_user", return_value="user_out"), \
            patch(f"{USER_SERVICE_PATH}.User", return_value="new_user"):
        result = await user_service.create_user(fake_user)
        assert result == "user_out"


@pytest.mark.asyncio
async def test_create_user_already_registered(user_service, user_repository, fake_user):
    user_repository.get_by_email.return_value = fake_user
    with pytest.raises(EmailAlreadyRegisteredError):
        await user_service.create_user(fake_user)


@pytest.mark.asyncio
async def test_create_user_invalid_roles(user_service, role_repository, fake_user):
    role_repository.get_by_names.return_value = []
    with pytest.raises(OneOrMoreRolesAreInvalid):
        await user_service.create_user(fake_user)


# -------------------------
# UPDATE USER
# -------------------------

@pytest.mark.asyncio
async def test_update_user_success(user_service, fake_user, fake_user_update):
    with patch(f"{USER_SERVICE_PATH}.UserOut.from_user", return_value="user_out"):
        result = await user_service.update_user(fake_user.id, fake_user_update)
        assert result == "user_out"


@pytest.mark.asyncio
async def test_update_user_not_found(user_service, user_repository, fake_user_update):
    user_repository.get_by_id.return_value = None
    with pytest.raises(UserNotFound):
        await user_service.update_user(uuid4(), fake_user_update)


@pytest.mark.asyncio
async def test_update_user_invalid_roles(user_service, role_repository, user_repository, fake_user, fake_user_update):
    role_repository.get_by_names.return_value = []
    fake_user_update.roles = ["invalid"]
    with pytest.raises(OneOrMoreRolesAreInvalid):
        await user_service.update_user(fake_user.id, fake_user_update)


# -------------------------
# UPDATE USER ME
# -------------------------

@pytest.mark.asyncio
async def test_update_user_me_success(user_service, fake_user, fake_user_update):
    with patch(f"{USER_SERVICE_PATH}.UserMeOut.from_user", return_value="me"), \
            patch(f"{USER_SERVICE_PATH}.create_access_token", return_value="access"), \
            patch(f"{USER_SERVICE_PATH}.create_refresh_token", return_value="refresh"), \
            patch(f"{USER_SERVICE_PATH}.UserUpdate", return_value=fake_user_update), \
            patch(f"{USER_SERVICE_PATH}.UserMeUpdateResponse", return_value="mock_response"):
        result = await user_service.update_user_me(fake_user.id, fake_user_update)
        assert result == "mock_response"


@pytest.mark.asyncio
async def test_update_user_me_user_not_found(user_service, user_repository, fake_user_update):
    user_repository.get_by_id.return_value = None
    with pytest.raises(UserNotFound):
        await user_service.update_user_me(uuid4(), fake_user_update)


@pytest.mark.asyncio
async def test_update_user_me_invalid_roles(user_service, role_repository, fake_user, fake_user_update):
    role_repository.get_by_names.return_value = []
    fake_user_update.roles = ["role_test"]

    with patch(f"{USER_SERVICE_PATH}.UserUpdate", return_value=fake_user_update):
        with pytest.raises(OneOrMoreRolesAreInvalid):
            await user_service.update_user_me(fake_user.id, fake_user_update)


# -------------------------
# DELETE USER
# -------------------------

@pytest.mark.asyncio
async def test_delete_user_success(user_service, user_repository, fake_user):
    user_repository.get_by_id.return_value = fake_user
    result = await user_service.delete_user(fake_user.id)
    assert result is True
    user_repository.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_user_not_found(user_service, user_repository):
    user_repository.get_by_id.return_value = None
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        await user_service.delete_user(uuid4())
