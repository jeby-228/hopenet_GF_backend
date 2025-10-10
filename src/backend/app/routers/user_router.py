import typing as t

from fastapi import APIRouter
from fastapi import Form

from ..dependencies.user_dependency import CurrentActiveUserDepends
from ..dependencies.user_dependency import bearer_jwt_auth_backend
from ..dependencies.user_dependency import cookie_jwt_auth_backend
from ..dependencies.user_dependency import fastapi_users
from ..schemas.user_schema import UserCreate
from ..schemas.user_schema import UserRead
from ..schemas.user_schema import UserUpdate


user_router = APIRouter()


user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),  # register
    prefix='/auth',
    tags=['auth'],
)
user_router.include_router(
    fastapi_users.get_register_router(  # register
        UserRead,
        t.Annotated[UserCreate, Form()],  # pyright: ignore[reportArgumentType]
    ),
    prefix='/auth_form',
    tags=[
        'auth',
        '!form',  # TODO
    ],
)


user_router.include_router(
    fastapi_users.get_auth_router(cookie_jwt_auth_backend),  # login / logout
    prefix='/auth/cookie-jwt',
    tags=[
        'auth',
        '!form',  # TODO
    ],
)
user_router.include_router(
    fastapi_users.get_auth_router(bearer_jwt_auth_backend),  # login / logout
    prefix='/auth/jwt',
    tags=['auth'],
)


user_router.include_router(
    fastapi_users.get_reset_password_router(),  # forgot / reset
    prefix='/auth',
    tags=['auth'],
)
user_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix='/auth',
    tags=['auth'],
)


@user_router.get('/authenticated-route', tags=['auth'])
async def authenticated_route(user: CurrentActiveUserDepends):
    return {'message': f'Hello {user.email}!'}


user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)
