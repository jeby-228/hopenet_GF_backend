import typing as t

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from ..models.user_model import User
from ..settings.database_setting import database_settings


_async_engine = create_async_engine(database_settings.database_url, echo=database_settings.echo)
_async_session_maker = async_sessionmaker(_async_engine, expire_on_commit=False)


async def get_async_session() -> t.AsyncGenerator[AsyncSession, None]:
    async with _async_session_maker() as session:
        yield session


async def create_db_and_tables() -> None:
    async with _async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


SessionDepends = t.Annotated[AsyncSession, Depends(get_async_session)]


async def get_user_db(session: SessionDepends):
    yield SQLAlchemyUserDatabase(session, User)
