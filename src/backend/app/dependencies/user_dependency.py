import typing as t
import uuid

from fastapi import Depends
from fastapi import Request
from fastapi_users import BaseUserManager
from fastapi_users import FastAPIUsers
from fastapi_users import UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.authentication import BearerTransport
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase

from ..models.user_model import User
from ..settings.user_setting import user_settings
from .database_dependency import get_user_db


_SECRET = user_settings.secret_key


# Transport


# https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/transports/cookie/#configuration
_cookie_transport = CookieTransport(cookie_max_age=3600)
# TODO

# https://fastapi-users.github.io/fastapi-users/latest/configuration/authentication/transports/bearer/
_bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


# Strategy


def _get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=_SECRET, lifetime_seconds=3600)  # TODO


# Authentication backend


cookie_jwt_auth_backend = AuthenticationBackend(
    name='cookie_jwt', transport=_cookie_transport, get_strategy=_get_jwt_strategy
)
bearer_jwt_auth_backend = AuthenticationBackend(
    name='bearer_jwt', transport=_bearer_transport, get_strategy=_get_jwt_strategy
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = _SECRET
    verification_token_secret = _SECRET

    async def on_after_register(self, user: User, request: t.Optional[Request] = None):
        print(f'User {user.id} has registered.')

    async def on_after_forgot_password(self, user: User, token: str, request: t.Optional[Request] = None):
        print(f'User {user.id} has forgot their password. Reset token: {token}')

    async def on_after_request_verify(self, user: User, token: str, request: t.Optional[Request] = None):
        print(f'Verification requested for user {user.id}. Verification token: {token}')


async def get_user_manager(user_db: t.Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [cookie_jwt_auth_backend, bearer_jwt_auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_superuser_user = fastapi_users.current_user(superuser=True)

CurrentActiveUserDepends = t.Annotated[User, Depends(current_active_user)]
CurrentSuperuserUserDepends = t.Annotated[User, Depends(current_superuser_user)]
