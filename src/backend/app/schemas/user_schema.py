import uuid

from fastapi_users import schemas


# TODO


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass
    # name: str | None
    # phone: str | None


class UserCreate(schemas.BaseUserCreate):
    pass
    # name: str | None = None
    # phone: str | None = None


class UserUpdate(schemas.BaseUserUpdate):
    pass
    # name: str | None = None
    # phone: str | None = None
