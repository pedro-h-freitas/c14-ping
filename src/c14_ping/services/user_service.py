from uuid import UUID

from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from fastapi import HTTPException, status

from c14_ping.core.security import create_access_token, create_refresh_token, decode_refresh_token, verify_password, get_password_hash
from c14_ping.repositories import UserRepository, RoleRepository
from c14_ping.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsException, OneOrMoreRolesAreInvalid, UserNotFound
from c14_ping.schemas import TokenOut, UserCreate, UserMeOut, UserMeUpdate, UserMeUpdateResponse, UserOut, UserUpdate, UsersResponse
from c14_ping.models import User


class UserService:
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository):
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def login(self, email: str, password: str) -> TokenOut:
        user_on_db = await self.user_repository.get_by_email(email)
        if not user_on_db or not verify_password(password, user_on_db.password):
            raise InvalidCredentialsException

        access_token = create_access_token(
            subject=user_on_db.email,
            roles=user_on_db.role_names,
        )

        refresh_token = create_refresh_token(
            subject=user_on_db.email,
        )

        return TokenOut(
            access_token=access_token,
            refresh_token=refresh_token,
            msg='Login successful'
        )

    async def refresh_token(self, refresh_token: str) -> TokenOut:
        try:
            token_data = decode_refresh_token(refresh_token)
        except (InvalidTokenError, ValidationError):
            raise InvalidCredentialsException()

        user_on_db = await self.user_repository.get_by_email(token_data.sub)

        if not user_on_db:
            raise InvalidCredentialsException()

        access_token = create_access_token(
            subject=user_on_db.email,
            roles=user_on_db.role_names,
        )

        refresh_token = create_refresh_token(
            subject=user_on_db.email,
        )

        return TokenOut(
            access_token=access_token,
            refresh_token=refresh_token,
            msg='Refresh successful'
        )

    async def get_all_users(self) -> UsersResponse:
        users = await self.user_repository.get_all()
        return UsersResponse.from_users(users)

    def get_user_me(self, user: User) -> UserMeOut:
        return UserMeOut.from_user(user)

    async def create_user(self, user_create: UserCreate) -> UserOut:
        existing_user = await self.user_repository.get_by_email(user_create.email)
        if existing_user:
            raise EmailAlreadyRegisteredError()

        user_create.password = get_password_hash(user_create.password)

        roles = await self.role_repository.get_by_names(user_create.roles)
        if len(roles) != len(user_create.roles):
            raise OneOrMoreRolesAreInvalid()

        new_user = await self.user_repository.create(
            User(
                username=user_create.username,
                email=user_create.email,
                password=user_create.password,
                roles=roles,
            )
        )

        return UserOut.from_user(new_user)

    async def __update_user(
        self,
        user_id: UUID,
        user_update: UserUpdate
    ) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound

        if user_update.username is not None:
            user.username = user_update.username

        if user_update.email is not None:
            user.email = user_update.email

        if user_update.password is not None:
            user.password = get_password_hash(user_update.password)

        if user_update.roles is not None:
            roles = await self.role_repository.get_by_names(user_update.roles)
            if len(roles) != len(user_update.roles):
                raise OneOrMoreRolesAreInvalid

            user.roles = roles

        user_updated = await self.user_repository.update_user(user)

        return user_updated

    async def update_user(
        self,
        user_id: UUID,
        user_update: UserUpdate
    ) -> UserOut:
        user_updated = await self.__update_user(user_id, user_update)
        return UserOut.from_user(user_updated)

    async def update_user_me(
        self,
        user_id: UUID,
        user_me_update: UserMeUpdate
    ) -> UserMeUpdateResponse:
        user_update = UserUpdate(
            password=user_me_update.password,
            username=user_me_update.username,
            email=user_me_update.email
        )
        user_updated = await self.__update_user(user_id, user_update)

        access_token = create_access_token(
            subject=user_updated.email,
            roles=user_updated.role_names,
        )

        refresh_token = create_refresh_token(
            subject=user_updated.email
        )

        token_update = TokenOut(
            access_token=access_token,
            refresh_token=refresh_token,
            msg="User updated successfully"
        )

        return UserMeUpdateResponse(
            user_update=UserMeOut.from_user(user_updated),
            token_update=token_update
        )

    async def delete_user(self, user_id: UUID):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await self.user_repository.delete(user)
        return True
